from bs4 import BeautifulSoup
import html5lib
from selenium import webdriver
    
import requests
import time
import re

import dataobject
from stringhelpers import *

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
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight/4);") 
        time.sleep(2)

    return BeautifulSoup(browser.page_source, "html5lib")

def getHTML(website):
    if PRINT_PROGRESS:
        print("Scraping website for plain HTML: {}".format(website))
    
    page = requests.get(website)

    if PRINT_PROGRESS:
        print("Scraping website complete")

    return BeautifulSoup(page.content, "html5lib")

def saveToFile(string, filename):
    print("Saving to file {}...".format(filename))
    text_file = open(filename, "w")
    text_file.write(string)
    text_file.close()
    print("Saved to file {}".format(filename))


class NovelScraper:
    """Parent class to be inherited for all countries. Defines two needed functions: scrape and __init__"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "N/A (BASE CLASS)"
        self.iso_code = "N/A (BASE CLASS)"
        self.source_website = "N/A (BASE CLASS)"

    def scrape(self, browser):
        """ Template for scrape function. Returns a data object containing the cases"""
        result = dataobject.DataObject(self)
        return result

class NovelScraperNO(NovelScraper):
    """Norway Coronavirus Scraper. Javascript parsing needed"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Norway"
        self.iso_code = "NO"
        #Source has javascript components for cases
        self.source_website = "https://www.vg.no/spesial/2020/corona/"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = getParsedJavaScriptHTML(self.source_website, browser)

        result.cases = clean_number(soup.find("span", class_="absolute confirmed").contents[0])
        result.deaths = clean_number(soup.find("span", class_="absolute dead").contents[0])
        hospital_cases = soup.find_all("a", class_="content", href="#norge-innlagt-paa-sykehus")
        result.hospitalised = clean_number(hospital_cases[0].find("span", class_="deadNorway").text)
        result.intensive_care = clean_number(hospital_cases[1].find("span", class_="deadNorway").text)
        result.tested = clean_number(soup.find("a", class_="content", href="#norge-testet").find("span", class_="deadNorway").text)

        return result

class NovelScraperSE(NovelScraper):
    """Sweden Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Sweden"
        self.iso_code = "SE"
        #Source has plain html for cases
        self.source_website = "https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/aktuellt-epidemiologiskt-lage/"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = getHTML(self.source_website)

        text = soup.find("p", text=re.compile("Totalt har"))
        result.cases = int(match(text.get_text(), "Totalt har {} personer"))
        result.deaths = int(match(text.get_text(), "Nationellt har {} av fallen"))

        return result


class NovelScraperDK(NovelScraper):
    """Denmark Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Denmark"
        self.iso_code = "DK"
        #Source has plain html for cases
        self.source_website = "https://politi.dk/coronavirus-i-danmark/foelg-smittespredningen-globalt-regionalt-og-lokalt"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = getHTML(self.source_website)

        #saveToFile(soup.prettify(), "output.txt")

        objects = soup.find("td", text=re.compile("Geografisk område")).parent.parent.find_all("td")
        table = [i.text for i in objects]

        denmark_cases = clean_number(table[6])
        denmark_deaths = clean_number(table[7])
        denmark_tested = clean_number(table[5])

        faraoe_cases = clean_number(table[10])
        faraoe_deaths = clean_number(table[11])
        faraoe_tested = clean_number(table[9])

        greenland_cases = clean_number(table[14])
        greenland_deaths = clean_number(table[15])
        greenland_tested = clean_number(table[13])

        result.cases = denmark_cases + faraoe_cases + greenland_cases
        result.deaths = denmark_deaths + faraoe_deaths + greenland_deaths
        result.tested = denmark_tested + faraoe_tested + greenland_tested

        return result

class NovelScraperFI(NovelScraper):
    """Finland Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Finland"
        self.iso_code = "FI"
        #Source has plain html for cases
        self.source_website = "https://korona.kans.io/"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = getHTML(self.source_website)

        title = soup.find("title", text=re.compile("Suomen koronavirus-tartuntatilanne - Tartunnat")).string
        title_words = title.split()
        result.cases = title_words[5]
        result.recovered = title_words[8]
        result.deaths = title_words[11]

        return result


class NovelScraperIS(NovelScraper):
    """Iceland Coronavirus Scraper. Javascript parsing needed"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Iceland"
        self.iso_code = "IS"
        #Source has javascript. Link is embedded data from https://www.covid.is/tolulegar-upplysingar
        self.source_website = "https://e.infogram.com/7327507d-28f5-4e3c-b587-c1680bd790e6?src=embed"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = getParsedJavaScriptHTML(self.source_website, browser, 6, True)

        elem = soup.find("div", class_="igc-textual-fact", text=re.compile("staðfest smit"))
        result.cases = clean_number(elem.previous)

        elem = soup.find("div", class_="igc-textual-fact", text=re.compile("á sjúkrahúsi"))
        result.hospitalised = clean_number(elem.previous)

        elem = soup.find("div", class_="igc-textual-fact", text=re.compile("batnað"))
        result.recovered = clean_number(elem.previous)

        elem = soup.find("div", class_="igc-textual-fact", text=re.compile("sýni"))
        result.tested = clean_number(elem.previous)

        return result

class NovelScraperEE(NovelScraper):
    """Estonia Coronavirus Scraper. Javascript parsing needed"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Estonia"
        self.iso_code = "EE"
        #Source is used in the official health department site https://www.terviseamet.ee/et/koroonaviirus/koroonakaart
        self.source_website = "https://www.koroonakaart.ee/en"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = getParsedJavaScriptHTML(self.source_website, browser)


        result.cases = clean_number(soup.find("h5", text=re.compile("Confirmed cases")).parent.nextSibling.string)
        result.hospitalised = clean_number(soup.find("h5", text=re.compile("In treatment")).parent.nextSibling.string)
        result.deaths = clean_number(soup.find("h5", text=re.compile("Deaths")).parent.nextSibling.string)
        result.recovered = clean_number(soup.find("h5", text=re.compile("Recovered")).parent.nextSibling.string)
        result.tested = clean_number(soup.find("h5", text=re.compile("Tests administered")).parent.nextSibling.string)

        return result

class NovelScraperLV(NovelScraper):
    """Latvian Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Latvia"
        self.iso_code = "LV"
        #Source is used in the official health department site https://www.terviseamet.ee/et/koroonaviirus/koroonakaart
        self.source_website = "https://arkartassituacija.gov.lv/"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = getHTML(self.source_website)

        paragraph = soup.find("span", style="font-family:inherit", text=re.compile("Iepriekšējā")).string

        result.tested = clean_number(match(paragraph, "Latvijā kopā veikti {} izmeklējumi"))
        result.cases = clean_number(match(paragraph, "apstiptināti {} saslimšanas gadījumi"))

        return result

class NovelScraperLI(NovelScraper):
    """Lithuania Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Lithuania"
        self.iso_code = "LI"
        #Source is used in the official health department site https://www.terviseamet.ee/et/koroonaviirus/koroonakaart
        self.source_website = "https://sam.lrv.lt/lt/naujienos/koronavirusas"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = getHTML(self.source_website)

        paragraph = soup.find("div", class_="text").text


        result.cases = clean_number(match(paragraph, "atvejų: {}"))
        result.deaths = clean_number(match(paragraph, "koronaviruso skaičius: {}"))
        result.recovered = clean_number(match(paragraph, "Pasveikusiųjų skaičius: {}"))
        result.tested = clean_number(match(paragraph, "įtariamo koronaviruso: {}"))

        #Sometimes they add an extra update. Then grab those numbers instead
        if "Atnaujinta" in paragraph:
            index = paragraph.find("Atnaujinta")
            paragraph = paragraph[index:]
            result.cases = clean_number(match(paragraph, "atvejų: {}"))

        return result


#saveToFile(soup.prettify(), "output.txt")
