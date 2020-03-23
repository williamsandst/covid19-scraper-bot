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