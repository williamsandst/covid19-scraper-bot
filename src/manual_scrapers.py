from bs4 import BeautifulSoup
import html5lib
from selenium import webdriver

import requests
import time
import re

import dataobject
from stringhelpers import *
from novelscraper import *

class NovelScraperDK(NovelScraper):
    """Denmark Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Denmark"
        self.iso_code = "DK"
        #Source has plain html for cases
        self.source_website = "https://politi.dk/coronavirus-i-danmark/foelg-smittespredningen-globalt-regionalt-og-lokalt"
        self.report_website = None

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = get_html(self.source_website)

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