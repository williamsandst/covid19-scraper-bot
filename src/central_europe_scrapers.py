from bs4 import BeautifulSoup
import html5lib
from selenium import webdriver

import requests
import time
import re

import dataobject
from stringhelpers import *
from novelscraper import *

class NovelScraperDE(NovelScraper):
    """Germany Coronavirus Scraper. Javascript parsing needed"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Germany"
        self.iso_code = "DE"
        self.source_website = "https://interaktiv.morgenpost.de/corona-virus-karte-infektionen-deutschland-weltweit-teaser/"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = getParsedJavaScriptHTML(self.source_website, browser)

        result.cases = clean_number(soup.find("div", class_="cases-item cases-item--confirmed").find("div", class_="cases-number").string)
        result.deaths = clean_number(soup.find("div", class_="cases-item cases-item--deaths").find("div", class_="cases-number").string)
        result.recovered = clean_number(soup.find("div", class_="cases-item cases-item--recovered").find("div").next)

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
        soup = getHTML(self.source_website)

        #saveToFile(soup.prettify(), "output.txt")
        text = soup.find("div", class_="item__layout-inner").text
        result.cases = clean_number(match(text, "{} cas COVID-19 ont été confirmés,"))
        result.deaths = clean_number(match(text, "incluant {} décès survenus"))
        result.hospitalised = clean_number(match(text, "{} cas de COVID-19 étaient hospitalisés"))
        result.intensive_care = clean_number(match(text, "dont {} en"))
        
        return result

class NovelScraperES(NovelScraper):
    """Spain Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Spain"
        self.iso_code = "ES"
        self.source_website = "https://www.rtve.es/noticias/20200323/mapa-del-coronavirus-espana/2004681.shtml"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = getHTML(self.source_website)

        text = soup.find("div", class_="artBody", itemprop="articleBody").text

        result.cases = clean_number(match(text, "{} casos de contagio en España,"))
        result.deaths = clean_number(match(text, "muerte de {} personas"))
        result.recovered = clean_number(match(text, "{} pacientes recuperados,"))
        result.intensive_care =  clean_number(match(text, "{} personas están ingresadas en la UCI,"))

        return result

class NovelScraperIT(NovelScraper):
    """Italy Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Italy"
        self.iso_code = "IT"
        self.source_website = "https://datastudio.google.com/u/0/reporting/91350339-2c97-49b5-92b8-965996530f00/page/RdlHB"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = getParsedJavaScriptHTML(self.source_website, browser, 5)

        result.cases = clean_number(soup.find("div", class_="kpi-label ng-binding", text=re.compile("Total Cases")).parent.find("div", class_="valueLabel").string)
        result.deaths = clean_number(soup.find("div", class_="kpi-label ng-binding", text=re.compile("Deaths")).parent.find("div", class_="valueLabel").string)
        result.recovered = clean_number(soup.find("div", class_="kpi-label ng-binding", text=re.compile("Recovered")).parent.find("div", class_="valueLabel").string)
        result.intensive_care = clean_number(soup.find("div", class_="kpi-label ng-binding", text=re.compile("Intensive Care")).parent.find("div", class_="valueLabel").string)
        result.hospitalised = clean_number(soup.find("div", class_="kpi-label ng-binding", text=re.compile("Hospitalized")).parent.find("div", class_="valueLabel").string)
        result.tested = clean_number(soup.find("div", class_="kpi-label ng-binding", text=re.compile("Tests")).parent.find("div", class_="valueLabel").string)

        return result

class NovelScraperPT(NovelScraper):
    """Portugal Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Portugal"
        self.iso_code = "PT"
        #Embeded source in https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/
        self.source_website = "https://esriportugal.maps.arcgis.com/apps/opsdashboard/index.html#/e9dd1dea8d1444b985d38e58076d197a"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = getParsedJavaScriptHTML(self.source_website, browser, 5)

        elem = soup.find("div", class_="dock-container ember-view").find("text", text=re.compile("Casos Confirmados")).parent.parent.parent.parent.parent
        result.cases = clean_number(match(elem.text, "Casos Confirmados {}"))
        elem = soup.find("div", class_="dock-container ember-view").find("text", text=re.compile("Total de Óbitos")).parent.parent.parent.parent.parent
        result.deaths = clean_number(match(elem.text, "Total de Óbitos {}"))
        elem = soup.find("div", class_="dock-container ember-view").find("text", text=re.compile("Total de Recuperados")).parent.parent.parent.parent.parent
        result.recovered = clean_number(match(elem.text, "Total de Recuperados {}"))
        elem = soup.find("div", class_="dock-container ember-view").find("text", text=re.compile("Casos Suspeitos")).parent.parent.parent.parent.parent
        result.suspected_cases = clean_number(match(elem.text, "Casos Suspeitos {}"))

        return result

class NovelScraperNL(NovelScraper):
    """Netherlands Coronavirus Scraper. Plain HTML"""
    def __init__(self):
        """Initializes class members to match the country the class is designed for"""
        self.country_name = "Netherlands"
        self.iso_code = "NL"
        #Embeded source in https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/
        self.source_website = "https://esriportugal.maps.arcgis.com/apps/opsdashboard/index.html#/e9dd1dea8d1444b985d38e58076d197a"

    def scrape(self, browser):
        """ Scrape function. Returns a data object with the reported cases. Uses Selenium and Beautifulsoup to extract the data """ 
        result = dataobject.DataObject(self)
        soup = getParsedJavaScriptHTML(self.source_website, browser, 5)

        #saveToFile(soup.prettify(), "output.txt")

        return result
