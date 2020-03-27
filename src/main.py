"""
Main file
This is a program which scrapes the Coronavirus confirmed cases, deaths and recovered from various countries health ministry websites
"""

from selenium import webdriver

from novelscraper import *
from nordic_scrapers import *
from central_europe_scrapers import *
from eastern_europe_scrapers import *
import interface

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
        if country_classes[country].training_data != None:
            train_country(country, browser)
        else:
            print("{}: Missing training data".format(country))
    print("Training complete!")
    browser.quit()

def train_country(country, browser):
    print("{}: Training recognition model...".format(country))
    country_classes[country].train(browser)
    print("{}: Training complete!".format(country))

def scrape():
    browser = webdriver.Firefox()

    for country in country_classes:
        results[country] = scrape_country(country, browser)

    for country, result in results.items():
        print(result)

    submission_string = interface.create_submissions(results)
    save_to_file(submission_string, "output/submissions.txt")

    browser.quit()

def scrape_country(country: str, browser):
    print("{}: Scraping...".format(country))
    result = country_classes[country].scrape(browser)
    print("{}: Scraping complete!".format(country))
    return result

def init_countries():
    """ Initiate the various country classes """
    # Nordic countries:
    # Norway
    scraper = NovelScraperAuto()
    scraper.country_name = "Norway" 
    scraper.iso_code = "NO"
    scraper.javascript_required = True
    scraper.source_website = "https://www.vg.no/spesial/2020/corona/"
    scraper.optimize_min_max_index_ratio = 0.1
    #scraper.training_data = {"cases": "3752", "deaths":"19", "tested":"78036", "hospitalised": "302", "intensive_care":"76"}
    country_classes[scraper.country_name] = scraper

    # Latvia
    scraper = NovelScraperAuto()
    scraper.country_name = "Latvia" 
    scraper.iso_code = "LV"
    scraper.source_website = "https://arkartassituacija.gov.lv/"
    #scraper.training_data = {"cases": "280", "tested":"11702", "hospitalised": "21"}
    country_classes[scraper.country_name] = scraper

    # Sweden
    scraper = NovelScraperAuto()
    scraper.country_name = "Sweden"
    scraper.iso_code = "SE"
    scraper.javascript_required = True
    scraper.optimize_min_max_index_ratio = 0.1
    scraper.source_website = "https://fohm.maps.arcgis.com/apps/opsdashboard/index.html#/68d4537bf2714e63b646c37f152f1392"
    scraper.report_website = "https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/aktuellt-epidemiologiskt-lage/"
    #scraper.training_data = {"cases": "3046", "deaths": "92", "intensive_care": "209"}
    country_classes[scraper.country_name] = scraper

    # Denmark
    # Cases are divided up by regions, can't be parsed with auto
    scraper = NovelScraperDK()
    country_classes[scraper.country_name] = scraper

    # Finland
    scraper = NovelScraperAuto()
    scraper.country_name = "Finland"
    scraper.iso_code = "FI"
    scraper.javascript_required = True
    scraper.source_website = "https://korona.kans.io/"
    #scraper.training_data = {"cases": "1056", "deaths": "7", "recovered": "10"}
    country_classes[scraper.country_name] = scraper

    # Iceland
    scraper = NovelScraperAuto()
    scraper.country_name = "Iceland"
    scraper.iso_code = "IS"
    scraper.javascript_required = True
    scraper.website_scroll = True
    scraper.source_website = "https://e.infogram.com/7327507d-28f5-4e3c-b587-c1680bd790e6?src=embed"
    scraper.report_website = "https://www.covid.is/tolulegar-upplysingar"
    #scraper.training_data = {"cases": "890", "recovered": "97", "hospitalised":"18", "intensive_care":"6", "tested":"13613"}
    country_classes[scraper.country_name] = scraper

def main():
    init_countries()
    #report_all()
    #train()
    scrape()
    #browser = webdriver.Firefox()

    #train_country("Iceland", browser)
    #print(scrape_country("Iceland", browser))

    #browser.quit()