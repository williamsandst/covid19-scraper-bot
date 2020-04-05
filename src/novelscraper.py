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
import covidtracking_downloader

# Constants
PRINT_PROGRESS = True
ALLOW_SCREENSHOTS = True

# How many words should we use surrounding the number for the learning model?
SURROUNDING_WORD_COUNT = 5

def get_parsed_javascript_html(website, browser, wait_time = 4, scroll = False):
    """Returns the parsed javascript HTML source code for a website"""
    if PRINT_PROGRESS:
        print("Scraping website with Selenium: {}".format(website))
    
    browser.get(website)
    time.sleep(wait_time)

    if PRINT_PROGRESS:
        print("Scraping website complete")

    if scroll: #Scroll down page to load in potential deferred javascript elements
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight/{});".format(scroll)) 
        time.sleep(2)

    return BeautifulSoup(browser.page_source, "html5lib")

def get_screenshot(website, browser, screenshot_path, viewport_width=1200, viewport_height=900, wait_time = 4, scroll_height = None):
    browser.set_window_size(viewport_width, viewport_height) 
    browser.get(website)
    time.sleep(wait_time)
    if scroll_height != None: #Scroll on page
        browser.execute_script("window.scrollTo(0, {})".format(scroll_height)) 
        time.sleep(0.3)
    if ALLOW_SCREENSHOTS and screenshot_path != None:
        browser.save_screenshot(screenshot_path)

def get_visible_text(website, browser, viewport_width=1200, viewport_height=900, wait_time = 4, screenshot = False, parse_javscript = False, scroll_height = None):
    # extract text
    browser.set_window_size(viewport_width, viewport_height) 
    browser.get(website)
    if (parse_javscript):
        time.sleep(wait_time)
    else:
        time.sleep(0.5)

    if scroll_height != None: #Scroll on page
        browser.execute_script("window.scrollTo(0, {})".format(scroll_height)) 
        time.sleep(0.3)

    if ALLOW_SCREENSHOTS and screenshot != None:
        browser.save_screenshot('screenshots/{}.png'.format(screenshot))

    root = html.document_fromstring(browser.page_source)
    Cleaner(kill_tags=['noscript'], style=True)(root) # lxml >= 2.3.1
    text = " ".join(etree.XPath("//text()")(root))

    if PRINT_PROGRESS:
        print("Retrieved website with Selenium: {}".format(website))
        
    return text # extract text

def get_html(website):
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

def save_to_file(string, filename):
    print("Saving to file {}...".format(filename))
    text_file = open(filename, "w")
    text_file.write(string)
    text_file.close()
    print("Saved to file {}".format(filename))

def save_dict_to_file(d: dict, filename: str):
    jsondata = json.dumps(d)
    f = open(filename + ".json","w")
    f.write(jsondata)
    f.close()

def load_dict_from_file(filename: str) -> dict:
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
        self.source_website = None
        self.report_website = None
        self.javascript_required = False
        self.training_data = None
        self.website_height = 900
        self.website_width = 1200
        self.has_covidtracking = False
        self.has_hopkins = False
        self.has_default = True
        self.wait_time = 4
        self.scroll_height = None

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

    def screenshot(self, browser):
        if self.source_website == None:
            return None
        time = datetime.datetime.now()
        time = time.replace(microsecond=0)
        screenshot_path = "screenshots/{}|{}.png".format(self.country_name.lower(), time.__str__())
        get_screenshot(self.source_website, browser, screenshot_path, self.website_width, self.website_height, self.wait_time, self.scroll_height)
        return screenshot_path



class NovelScraperCoronaCloud(NovelScraper):
    def scrape(self, browser):
        """ Template for Coronacloud function. Returns a data object containing the cases"""
        result = dataobject.DataObject(self)
        soup = get_html(self.source_website)

        text = soup.find("div", class_="card border-left-danger h-100 py-2").parent.parent.text
        words = text.split('e')
        result.cases = clean_number(words[1])
        result.deaths = clean_number(words[2])
        result.recovered = clean_number(words[5])

        #Date needs javascript.

        return result

class NovelScraperCovidTracking(NovelScraper):
    def scrape_covidtracking(self, time = datetime.datetime.now()):
        result = dataobject.DataObject(self)

        result = covidtracking_downloader.scrape(self.iso_code, result, time)

        result.source_website = "https://covidtracking.com/"
        result.report_website = "https://covidtracking.com/"
        return result

class NovelScraperWorldOMeter(NovelScraper):
    pass

class LearnedData():
    def __init__(self, filename="none.txt"):
        self.data = dict()
        self.indices = dict()

    def save(self, country: str):
        """ Save data to file """
        filename = "data/rm_{}".format(country.lower())
        save_data = {"register": self.data, "indices": self.indices}
        save_dict_to_file(save_data, filename)

    def load(self, country: str):
        """ Load data from file """
        filename = "data/rm_{}".format(country.lower())
        loaded_data = load_dict_from_file(filename)
        self.data = loaded_data["register"]
        self.indices = loaded_data["indices"]


class NovelScraperAuto(NovelScraperCovidTracking):
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
        self.source_website = None
        self.report_website = None
        self.javascript_required = False
        self.learned_data = LearnedData()
        self.training_data = None
        self.website_height = 900
        self.website_width = 1200
        self.wait_time = 4
        self.optimize_min_max_index_ratio = 0.3
        self.has_covidtracking = False
        self.has_coronacloud = False
        self.has_worldometer = False
        self.has_default = True
        self.scroll_height = None

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
        context_words = get_surrounding_words(words, number_index, SURROUNDING_WORD_COUNT)
        for i, word in enumerate(context_words): #Compute distance value from center, ascending
            context_words[i] = (word, abs(SURROUNDING_WORD_COUNT-i) + (i >= SURROUNDING_WORD_COUNT))
        #Eval function: distance * similarity * constant
        #Filter out dates and various unneccessary components

        self.learned_data.data[label] = {}
        for word in context_words:
            self.learned_data.data[label][word[0]] = SURROUNDING_WORD_COUNT - word[1] 

    def train(self, browser):
        """ Train the model to find the numbers specified in data """
        text = self.retrieve_text(self.source_website, browser)
        for label, number in self.training_data.items():
            self.learn(text, number, label)
        self.learned_data.save(self.country_name)

    def retrieve_text(self, website, browser, screenshot = None):
        return get_visible_text(self.source_website, browser, self.website_width, self.website_height, self.wait_time, screenshot, self.javascript_required, self.scroll_height)

    def evaluate(self, words, register, ratio): #Ratio is % of way through word
        """ Give a score to a list of words based on how good a fit it is to the learned model """
        ldistancecutoff = 0.65
        score = 0
        for word in words:
            for rword in register:
                ldistance = 1 - stringdist.levenshtein_norm(rword, word)
                if ldistance >= ldistancecutoff: #Similar enough
                  score += register[rword]/SURROUNDING_WORD_COUNT + ratio*3
        return score

    def apply(self, text, register, index):
        """ Apply the learned model to the text to find the asked for number """
        text = clean_text(text)
        words = text.split()
        words = combine_separate_numbers(words)
        words = divide_numbers(words)
        words = clean_if_number(words)

        if self.optimize_min_max_index_ratio != 1: #Optimizing at potential loss of number
            offset = int(len(words)*self.optimize_min_max_index_ratio)
            start = max(0, index - offset)
            end = min(len(words), index + offset)
            words = words[start:end+1]

        #Find all numbers
        previousMaxScore = 0
        previousMaxNumber = -1
        for i, word in enumerate(words):
            if word.isdigit() and not is_time(word):
                sur_words = get_surrounding_words(words, i, SURROUNDING_WORD_COUNT)
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
        screenshot_path = self.country_name.lower() + "-" + result.scrape_date.__str__()
        result.screenshot_path = "output/" + screenshot_path + ".png"
        text = self.retrieve_text(self.source_website, browser, screenshot_path)
        #Scramble testing
        #text = clean_text(text)
        #text = scramble_text(text)
        self.learned_data.load(self.country_name)

        result_dict = {}

        for label, register in self.learned_data.data.items():
            result_dict[label] = self.apply(text, register, self.learned_data.indices[label])
        
        result.update_by_str_dict(result_dict)

        return result

