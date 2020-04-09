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
        self.javascript_required = False
        self.training_data = None
        self.website_height = 900
        self.website_width = 1200
        self.has_covidtracking = False
        self.has_hopkins = False
        self.has_default = True
        self.wait_time = 4
        self.scroll_height = None

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = get_html(self.source_website)

        #saveToFile(soup.prettify(), "output.txt")

        objects = soup.find("td", text=re.compile("Geografsk område")).parent.parent.find_all("td")
        table = [i.text for i in objects]

        denmark_cases = clean_number(table[7])
        denmark_deaths = clean_number(table[9])
        denmark_tested = clean_number(table[6])

        faraoe_cases = clean_number(table[12])
        faraoe_deaths = clean_number(table[14])
        faraoe_tested = clean_number(table[11])

        greenland_cases = clean_number(table[17])
        greenland_deaths = clean_number(table[19])
        greenland_tested = clean_number(table[16])

        result.cases = denmark_cases + faraoe_cases + greenland_cases
        result.deaths = denmark_deaths + faraoe_deaths + greenland_deaths
        result.tested = denmark_tested + faraoe_tested + greenland_tested

        return result

class NovelScraperFR(NovelScraper):
    """France Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "France"
        self.iso_code = "FR"
        self.source_website = "https://www.santepubliquefrance.fr/maladies-et-traumatismes/maladies-et-infections-respiratoires/infection-a-coronavirus/articles/infection-au-nouveau-coronavirus-sars-cov-2-covid-19-france-et-monde"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = get_html(self.source_website)

        #saveToFile(soup.prettify(), "output.txt")
        text = soup.find("div", class_="item__layout-inner").text
        result.cases = clean_number(match(text, "{} cas de COVID-19 ont été diagnostiqués"))
        result.deaths = -1
        #result.deaths = clean_number(match(text, "incluant {} décès survenus"))
        #result.hospitalised = clean_number(match(text, "{} cas de COVID-19 étaient hospitalisés"))
        #result.intensive_care = clean_number(match(text, "dont {} en"))
        
        return result