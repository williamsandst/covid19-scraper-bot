from bs4 import BeautifulSoup
import html5lib
from selenium import webdriver
from lxml import etree
import lxml.html as html
from lxml.html.clean import Cleaner
import stringdist

import json
import requests
import time
import re
import random

import dataobject
from stringhelpers import *

surrounding_word_count = 5

PRINT_PROGRESS = True

def getParsedJavaScriptHTML(website, browser, wait_time = 4, scroll = False):
    """Returns the parsed javascript HTML source code for a website"""
    if PRINT_PROGRESS:
        print("Scraping website with Selenium: {}".format(website))
    
    browser.get(website)
    time.sleep(wait_time)

    if PRINT_PROGRESS:
        print("Scraping website complete")

    if scroll: #Scroll down page to load in potential deferred javascript elements
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight/5);") 
        time.sleep(2)

    return BeautifulSoup(browser.page_source, "html5lib")

def getVisibleText(website, browser, wait_time = 4, screenshot = False, parse_javscript = False):
    # extract text
    if PRINT_PROGRESS:
        print("Scraping website with Selenium: {}".format(website))
    
    browser.get(website)
    if (parse_javscript):
        time.sleep(wait_time)
    else:
        time.sleep(0.5)

    if PRINT_PROGRESS:
        print("Scraping website complete")

    root = html.document_fromstring(browser.page_source)
    Cleaner(kill_tags=['noscript'], style=True)(root) # lxml >= 2.3.1
    text = " ".join(etree.XPath("//text()")(root))
    return text # extract text

def getHTML(website):
    if PRINT_PROGRESS:
        print("Scraping website for plain HTML: {}".format(website))
    
    page = requests.get(website)

    if PRINT_PROGRESS:
        print("Scraping website complete")

    return BeautifulSoup(page.content, "html5lib")

#Scramble variables
wordInsertChance = 0.1
charScrambleChance = 0.5

def scramble_text(string):
    wordlist = list(string)
    for i, char in enumerate(wordlist):
        if random.random() < charScrambleChance and not char.isdigit() and not char == ":" and not char == "." and not char == "," and not char == " ":
            wordlist[i] = "x"
    secondwordlist = []
    for i, char in enumerate(wordlist):
        if random.random() < wordInsertChance and not char.isdigit() and not char == ":" and not char == "." and not char == "," and not char == " ":
            secondwordlist += [" ", "l", "a", "l", "a", "l", "a", " "]
        else:
            secondwordlist.append(char)
    return "".join(wordlist)



def saveToFile(string, filename):
    print("Saving to file {}...".format(filename))
    text_file = open(filename, "w")
    text_file.write(string)
    text_file.close()
    print("Saved to file {}".format(filename))

def saveDictToFile(d: dict, filename: str):
    jsondata = json.dumps(d)
    f = open(filename + ".json","w")
    f.write(jsondata)
    f.close()

def loadDictFromFile(filename: str) -> dict:
    f = open(filename + ".json")
    d = json.load(f)
    f.close()
    return d

class NovelScraper:
    """Parent class to be inherited for all countries. Defines two needed functions: scrape and __init__"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "N/A (BASE CLASS)"
        self.iso_code = "N/A (BASE CLASS)"
        self.source_website = "N/A (BASE CLASS)"
        self.report_website = "N/A (BASE CLASS)"
        self.javascript_required = False

    def try_scrape(self, browser, count = 3):
        for i in range(3):
            try:
                return self.scrape(browser)
            except:
                print("Error on scraping attempt {}. Most likely the javascript did not load in time. Retrying.".format(i))

    def scrape(self, browser):
        """ Template for scrape function. Returns a data object containing the cases"""
        result = dataobject.DataObject(self)
        return result

class NovelScraperCoronaCloudTemplate(NovelScraper):
    def scrape(self, browser):
        """ Template for Coronacloud function. Returns a data object containing the cases"""
        result = dataobject.DataObject(self)
        soup = getHTML(self.source_website)

        text = soup.find("div", class_="card border-left-danger h-100 py-2").parent.parent.text
        words = text.split('e')
        result.cases = clean_number(words[1])
        result.deaths = clean_number(words[2])
        result.recovered = clean_number(words[5])

        #Date needs javascript.

        return result

class LearnedData():
    def __init__(self, filename="none.txt"):
        self.data = dict()
        self.indices = dict()
        self.filename = filename

    def save(self, country):
        """ Save data to file """
        filename = "data/"+country+"/lm"
        save_data = {"register": self.data, "indices": self.indices}
        saveDictToFile(save_data, filename)

    def load(self, country):
        """ Load data from file """
        filename = "data/"+country+"/lm"
        loaded_data = loadDictFromFile(filename)
        self.data = loaded_data["register"]
        self.indices = loaded_data["indices"]




class NovelScraperAuto(NovelScraper):
    """ Automated scraping through a training approach
        #Steps:
        #Learning:
        #1: Clean up text
        #2: Find index for cases, deaths etc given by me
        #3: "Learn" what attributes contribute to these numbers
        
        #Applying
        #1: Clean up text
        #2: Find cases, deaths etc based on learning attributes"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "N/A (BASE CLASS)"
        self.iso_code = "N/A (BASE CLASS)"
        self.source_website = "N/A (BASE CLASS)"
        self.report_website = None
        self.javascript_required = False
        self.learned_data = LearnedData()
        self.training_data = None

    def learn(self, text, number, label):
        """ Learn the data surrounding a number to be able to find it in the future """
        text = clean_text(text)
        words = text.split()
        words = combine_separate_numbers(words)
        words = divide_numbers(words)
        words = clean_if_number(words)
        number_index = find_word_index(words, number)
        if number_index == -1:
            print("Training: Cannot find the specified number", number)
            raise TypeError

        self.learned_data.indices[label] = number_index
        #Get surrounding words and skip the center one
        context_words = get_surrounding_words(words, number_index, surrounding_word_count)
        for i, word in enumerate(context_words): #Compute distance value from center, ascending
            context_words[i] = (word, abs(surrounding_word_count-i) + (i >= surrounding_word_count))
        #Eval function: distance * similarity * constant
        #Filter out dates and various unneccessary components

        self.learned_data.data[label] = {}
        for word in context_words:
            self.learned_data.data[label][word[0]] = surrounding_word_count - word[1] 

    def train(self, browser):
        """ Train the model to find the numbers specified in data """
        text = self.retrieve_text(self.source_website, browser, False)
        for label, number in self.training_data.items():
            self.learn(text, number, label)
        self.learned_data.save(self.country_name)

    def retrieve_text(self, website, browser, screenshot = False):
        return getVisibleText(self.source_website, browser, 5, screenshot, self.javascript_required)

    def evaluate(self, words, register, ratio): #Ratio is % of way through word
        """ Give a score to a list of words based on how good a fit it is to the learned model """
        ldistancecutoff = 0.65
        score = 0
        for word in words:
            for rword in register:
                ldistance = 1 - stringdist.levenshtein_norm(rword, word)
                if ldistance >= ldistancecutoff: #Similar enough
                  score += register[rword]/surrounding_word_count + ratio*3
        return score

    def apply(self, text, register, index):
        """ Apply the learned model to the text to find the asked for number """
        text = clean_text(text)
        words = text.split()
        words = combine_separate_numbers(words)
        words = divide_numbers(words)
        words = clean_if_number(words)
        #Find all numbers
        previousMaxScore = 0
        previousMaxNumber = -1
        for i, word in enumerate(words):
            if word.isdigit() and not is_time(word):
                sur_words = get_surrounding_words(words, i, surrounding_word_count)
                distance_from_index = (index - abs(index - float(i))) / index
                score = self.evaluate(sur_words, register, distance_from_index)
                if score > previousMaxScore:
                    previousMaxNumber = clean_number(word)
                    previousMaxScore = score
                    
        if previousMaxNumber != -1:
            return previousMaxNumber
        else:
            return -1

    def scrape(self, browser):
        """Automated scraping using the saved learned model from train()"""
        result = dataobject.DataObject(self)
        text = self.retrieve_text(self.source_website, browser, True)
        #Scramble testing
        #text = clean_text(text)
        #text = scramble_text(text)
        self.learned_data.load(self.country_name)

        result_dict = {}

        for label, register in self.learned_data.data.items():
            result_dict[label] = self.apply(text, register, self.learned_data.indices[label])
        
        result.update_by_str_dict(result_dict)

        return result


class NovelScraperGB(NovelScraper):
    """United Kingdom Coronavirus Scraper. Javascript parsing needed"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "United Kingdom"
        self.iso_code = "GB"
        self.source_website = "https://www.arcgis.com/apps/opsdashboard/index.html#/f94c3c90da5b4e9f9a0b19484dd4bb14"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = getParsedJavaScriptHTML(self.source_website, browser)

        result.cases = clean_number(soup.find("strong", text=re.compile("Total UK cases")).parent.parent.parent.parent.find("text").string)
        result.deaths = clean_number(soup.find("strong", text=re.compile("Total UK deaths")).parent.parent.parent.parent.find("text").string)
        result.recovered = clean_number(soup.find("strong", text=re.compile("Patients Recovered")).parent.parent.parent.parent.find("text").string)

        return result

class NovelScraperIE(NovelScraper):
    """Ireland Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Ireland"
        self.iso_code = "IE"
        self.source_website = "https://www.gov.ie/en/news/7e0924-latest-updates-on-covid-19-coronavirus/"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = getHTML(self.source_website)


        text = soup.find("div", class_="col-md-8 col-sm-8 padding-top-20 govie-markdown").text

        result.cases = clean_number(match(text, "There are now {}"))
        result.deaths = clean_number(match(text, "There have now been {}"))

        return result

#saveToFile(soup.prettify(), "output.txt")