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
    """Russia Coronavirus Scraper. Javascript parsing needed"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Russia"
        self.iso_code = "RU"
        #Link used for Worldometer.
        self.source_website = "https://xn--80aesfpebagmfblc0a.xn--p1ai//#"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = get_parsed_javascript_html(self.source_website, browser)

        result.cases = clean_number(soup.find("span", class_="d-map__indicator d-map__indicator_sick").parent.find("h3").next)
        result.recovered = clean_number(soup.find("span", class_="d-map__indicator d-map__indicator_healed").parent.find("h3").next)
        result.deaths = clean_number(soup.find("span", class_="d-map__indicator d-map__indicator_die").parent.find("h3").next)

        result.source_update_date = date_formatter(soup.find("small", text=re.compile("По состоянию на")).string + " 2020")

        return result

class NovelScraperBY(NovelScraperCoronaCloudTemplate):
    """Belarus Coronavirus Scraper. Plain HTML. Inherits scraper from template as it it uses CoronaCloud"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Belarus"
        self.iso_code = "BY"
        #There is no primary online source. Newspaper articles seem to be the standard. Therefore secondary
        self.source_website = "https://www.corona.cloud/belarus"


class NovelScraperPL(NovelScraper):
    """Poland Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Poland"
        self.iso_code = "PL"
        self.source_website = "https://koronawirusunas.pl/"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = get_html(self.source_website)

        elem = soup.find("div", class_="col-lg-8")
        result.cases = clean_number(elem.find("span", class_="badge badge-danger").text)
        result.deaths = clean_number(elem.find("span", class_="badge badge-dark").text)
        result.hospitalised = clean_number(match(elem.text, "{} hospitalizacja"))
        result.tested = clean_number(match(elem.text, "{} wykonane testy"))
        result.source_update_date = date_formatter(elem.find("span", class_="badge badge-light").text)

        return result

class NovelScraperUA(NovelScraperCoronaCloudTemplate):
    """Ukraine Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Ukraine"
        self.iso_code = "UA"
        #The primary source uses facebook, which is hard to scrape. Therefore secondary source
        self.source_website = "https://www.corona.cloud/ukraine"



class NovelScraperGR(NovelScraperCoronaCloudTemplate):
    """Greece Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Greece"
        self.iso_code = "GR"
        self.source_website = "https://www.corona.cloud/greece"

class NovelScraperCZ(NovelScraper):
    """Czechia Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Czechia"
        self.iso_code = "CZ"
        self.source_website = "https://onemocneni-aktualne.mzcr.cz/covid-19"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = get_html(self.source_website)

        result.source_update_date = date_formatter(soup.find("p", id="last-modified-datetime").text) #Minute is off
        result.tested = clean_number(soup.find("p", id="count-test").text)
        result.cases = clean_number(soup.find("p", id="count-sick").text)
        result.recovered = clean_number(soup.find("p", id="count-recover").text)
        result.deaths = clean_number(soup.find("p", id="count-dead").text)

        return result

class NovelScraperRO(NovelScraper):
    """Romania Coronavirus Scraper. Requires Javascript parsing"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Romania"
        self.iso_code = "RO"
        #Linked from Official Gov Health Deparment Site
        self.source_website = "https://instnsp.maps.arcgis.com/apps/opsdashboard/index.html#/5eced796595b4ee585bcdba03e30c127"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = get_parsed_javascript_html(self.source_website, browser)

        result.source_update_date = date_formatter(soup.find("strong").text)

        result.cases = clean_number(match(soup.text, "Total cazuri confirmate {}"))
        result.deaths = clean_number(match(soup.text, "Persoane decedate {}"))

        return result