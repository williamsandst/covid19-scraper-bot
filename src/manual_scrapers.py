from bs4 import BeautifulSoup
import html5lib
from selenium import webdriver

import requests
import time
import re

import dataobject
from stringhelpers import *
from novelscraper import *

class NovelScraperDK(NovelScraperHopkins):
    """Denmark Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.group_name = "Europe"
        self.province_name = "Denmark"
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
        self.has_hopkins = True
        self.has_default = True
        self.wait_time = 4
        self.scroll_height = None
        self.adjust_scraped_recovery_from_sheet = True
        self.adjust_scraped_deaths_from_sheet = False

    def scrape(self, browser, date = datetime.datetime.now()):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self, date)
        soup = get_html(self.source_website)

        #saveToFile(soup.prettify(), "output.txt")
        result.screenshot_path = self.screenshot(browser)

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

class NovelScraperNY(NovelScraperCovidTracking):
    """United States, New York Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.group_name = "Europe"
        self.province_name = "New-York"
        self.country_name = "United States"
        self.iso_code = "NY"
        #Source has plain html for cases
        self.source_website = "https://covid19tracker.health.ny.gov/views/NYS-COVID19-Tracker/NYSDOHCOVID-19Tracker-Map?%3Aembed=yes&%3Atoolbar=no&%3Atabs=n"
        self.source2_website = "https://covid19tracker.health.ny.gov/views/NYS-COVID19-Tracker/NYSDOHCOVID-19Tracker-Fatalities?%3Aembed=yes&%3Atoolbar=no&%3Atabs=n"
        self.report_website = None
        self.javascript_required = True
        self.training_data = None
        self.has_covidtracking = True
        self.has_hopkins = False
        self.has_default = True
        self.website_height = 900
        self.website_width = 900
        self.wait_time = 4
        self.scroll_height = None
        self.adjust_scraped_recovery_from_sheet = True
        self.adjust_scraped_deaths_from_sheet = False
        self.javascript_required = True

    def scrape(self, browser, date = datetime.datetime.now()):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self, date)
        soup = get_parsed_javascript_html(self.source_website, browser)
        #save_to_file(soup.prettify(), "output.txt", )

        #objects = soup.find("td", text=re.compile("Geografsk område")).parent.parent.find_all("td")
        #table = [i.text for i in objects]

        #result.cases = denmark_cases + faraoe_cases + greenland_cases
        #result.deaths = denmark_deaths + faraoe_deaths + greenland_deaths
        #result.tested = denmark_tested + faraoe_tested + greenland_tested

        #soup = get_parsed_javascript_html(self.source2_website, browser)

        return result

class NovelScraperFR(NovelScraperHopkins):
    """France Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "France"
        self.iso_code = "FR"
        self.source_website = "https://www.santepubliquefrance.fr/maladies-et-traumatismes/maladies-et-infections-respiratoires/infection-a-coronavirus/articles/infection-au-nouveau-coronavirus-sars-cov-2-covid-19-france-et-monde"
        self.has_hopkins = True

    def scrape(self, browser, date = datetime.datetime.now()):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self, date)
        soup = get_html(self.source_website)

        #saveToFile(soup.prettify(), "output.txt")
        text = soup.find("div", class_="item__layout-inner").text
        result.cases = clean_number(match(text, "{} cas de COVID-19 ont été diagnostiqués"))
        result.deaths = -1
        #result.deaths = clean_number(match(text, "incluant {} décès survenus"))
        #result.hospitalised = clean_number(match(text, "{} cas de COVID-19 étaient hospitalisés"))
        #result.intensive_care = clean_number(match(text, "dont {} en"))
        
        return result

class NovelScraperHU(NovelScraperHopkins):
    """Hungary Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Hungary"
        self.province_name = "Hungary"
        self.iso_code = "HU"
        self.source_website = "https://koronavirus.gov.hu/"
        self.source2_website = "https://koronavirus.gov.hu/elhunytak"
        self.scroll_height = 1400
        self.has_auto = True
        self.report_website = None
        self.javascript_required = False
        self.training_data = None
        self.website_height = 900
        self.website_width = 1200
        self.has_covidtracking = False
        self.has_hopkins = True
        self.wait_time = 4
        self.adjust_scraped_recovery_from_sheet = True
        self.adjust_scraped_deaths_from_sheet = False

    def scrape(self, browser, date = datetime.datetime.now()):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self, date)

        result.screenshot_path = self.screenshot(browser)

        soup = get_html(self.source_website)
        # Cases - Fertőzött
        result.cases = clean_number(soup.find("span", class_="label", text=re.compile("Fertőzött")).parent.find("span", class_="number").text)
        # Recovered - Gyógyult
        result.recovered = clean_number(soup.find("span", class_="label", text=re.compile("Gyógyult")).parent.find("span", class_="number").text)
        # Tested - Mintavétel
        result.tested = clean_number(soup.find("span", class_="label", text=re.compile("Mintavétel")).parent.find("span", class_="number").text)
        
        soup = get_html(self.source2_website)
        result.deaths = clean_number(soup.find("tbody").find("tr").find("td").text)

        return result

class NovelScraperHR(NovelScraperHopkins):
    """Croatia Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Croatia"
        self.province_name = "Croatia"
        self.iso_code = "HR"
        self.source_website = "https://www.koronavirus.hr/"
        self.has_auto = True
        self.report_website = None
        self.javascript_required = True
        self.training_data = None
        self.website_height = 900
        self.website_width = 900
        self.has_covidtracking = False
        self.has_hopkins = True
        self.wait_time = 4
        self.adjust_scraped_recovery_from_sheet = True
        self.adjust_scraped_deaths_from_sheet = False
        self.scroll_height = None

    def scrape(self, browser, date = datetime.datetime.now()):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self, date)

        result.screenshot_path = self.screenshot(browser)

        soup = get_parsed_javascript_html(self.source_website, browser)

        result.cases = clean_number(soup.find("div", class_="counter-title", text=re.compile("Slučajevi")).parent.find("strong").text)
        result.recovered = clean_number(soup.find("div", class_="counter-title", text=re.compile("Izliječeni")).parent.find("strong").text)
        result.deaths = clean_number(soup.find("div", class_="counter-title", text=re.compile("Preminuli")).parent.find("strong").text)

        return result