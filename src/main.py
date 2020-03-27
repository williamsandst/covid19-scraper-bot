"""
Main file
This is a program which scrapes the Coronavirus confirmed cases, deaths and recovered from various countries health ministry websites
"""

from selenium import webdriver

from novelscraper import *
from nordic_scrapers import *
from central_europe_scrapers import *
from eastern_europe_scrapers import *

""" 
Countries with working scraping:
Norway (NO)
Sweden (SE)
Denmark (DK)
Finland (FI)
Iceland (IS)
Estonia (EE)
Lativa (LV)
Lithuania (LI)
Germany (DE)
France (FR)
Spain (ES)
Italy (IT)
Portugal (PT)
Netherlands (NL)
Belgium (BE)
Switzerland (CH)
Austria (AT)
Russia (RU)
Poland (PL)
Czechia (CZ)
Romania (RO)
Belarus (BY) (CoronaCloud)
Ukarine (UA) (CoronaCloud)
Greece (GR) (CoronaCloud)
"""

country_classes = {}
results = {}

def train():
    browser = webdriver.Firefox()

    print("Starting training...")
    for country in country_classes:
        train_country(country, browser)
    print("Training complete!")
    browser.quit()

def train_country(country, browser):
    print(country, "{}: Training recognition model...")
    country_classes[country].train(browser)
    print(country, "{}: Training complete!")

def scrape():
    browser = webdriver.Firefox()

    for country in country_classes:
        results[country] = scrape_country(country, browser)

    for country, result in results.items():
        print(result)

    browser.quit()

def scrape_country(country: str, browser):
    print(country, "{}: Scraping...")
    result = country_classes[country].scrape(browser)
    print(country, "{}: Scraping complete!")
    return result

def init_countries():
    #Norway
    scraper = NovelScraperAuto()
    scraper.country_name = "Norway" 
    scraper.iso_code = "NO"
    scraper.javascript_required = True
    scraper.source_website = "https://www.vg.no/spesial/2020/corona/"
    #scraper.training_data = 
    country_classes[scraper.country_name] = scraper

def main():
    init_countries()
    #report_all()
    scrape()