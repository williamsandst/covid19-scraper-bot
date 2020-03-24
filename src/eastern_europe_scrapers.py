from bs4 import BeautifulSoup
import html5lib
from selenium import webdriver

import requests
import time
import re

import dataobject
from stringhelpers import *
from novelscraper import *

class NovelScraperRU(NovelScraper):
    """Russia Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Russia"
        self.iso_code = "RU"
        #Link used for Worldometer.
        self.source_website = "https://xn--80aesfpebagmfblc0a.xn--p1ai//#"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = getParsedJavaScriptHTML(self.source_website, browser)

        result.cases = clean_number(soup.find("span", class_="d-map__indicator d-map__indicator_sick").parent.find("h3").next)
        result.recovered = clean_number(soup.find("span", class_="d-map__indicator d-map__indicator_healed").parent.find("h3").next)
        result.deaths = clean_number(soup.find("span", class_="d-map__indicator d-map__indicator_die").parent.find("h3").next)

        result.source_update_date = date_formatter(soup.find("small", text=re.compile("По состоянию на")).string + " 2020")

        return result

class NovelScraperBY(NovelScraper):
    """Belarus Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Belarus"
        self.iso_code = "BY"
        self.source_website = "https://sam.lrv.lt/lt/naujienos/koronavirusas"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = getHTML(self.source_website)

        return result


class NovelScraperPL(NovelScraper):
    """Poland Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Poland"
        self.iso_code = "PL"
        self.source_website = "https://sam.lrv.lt/lt/naujienos/koronavirusas"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = getHTML(self.source_website)

        return result

class NovelScraperUA(NovelScraper):
    """Ukraine Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Ukraine"
        self.iso_code = "UA"
        self.source_website = "https://sam.lrv.lt/lt/naujienos/koronavirusas"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = getHTML(self.source_website)

        return result


class NovelScraperGR(NovelScraper):
    """Greece Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Greece"
        self.iso_code = "GR"
        self.source_website = "https://sam.lrv.lt/lt/naujienos/koronavirusas"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = getHTML(self.source_website)

        return result