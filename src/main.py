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
"""

def test():
    """Scrapes numbers for all programmed countries"""
    data = list()

    browser = webdriver.Firefox()

    scraper = NovelScraperNO()
    print("Scraping ", scraper.country_name)
    data.append(scraper.try_scrape(browser))

    scraper = NovelScraperSE()
    print("Scraping ", scraper.country_name)
    data.append(scraper.try_scrape(browser))

    scraper = NovelScraperDK()
    print("Scraping ", scraper.country_name)
    data.append(scraper.try_scrape(browser))

    scraper = NovelScraperFI()
    print("Scraping ", scraper.country_name)
    data.append(scraper.try_scrape(browser))

    scraper = NovelScraperIS()
    print("Scraping ", scraper.country_name)
    data.append(scraper.try_scrape(browser))

    scraper = NovelScraperEE()
    print("Scraping ", scraper.country_name)
    data.append(scraper.try_scrape(browser))

    scraper = NovelScraperLV()
    print("Scraping ", scraper.country_name)
    data.append(scraper.try_scrape(browser))

    scraper = NovelScraperLI()
    print("Scraping ", scraper.country_name)
    data.append(scraper.try_scrape(browser))

    scraper = NovelScraperGB()
    print("Scraping ", scraper.country_name)
    data.append(scraper.try_scrape(browser))

    scraper = NovelScraperIE()
    print("Scraping ", scraper.country_name)
    data.append(scraper.try_scrape(browser))

    scraper = NovelScraperDE()
    print("Scraping ", scraper.country_name)
    data.append(scraper.try_scrape(browser))

    scraper = NovelScraperFR()
    print("Scraping ", scraper.country_name)
    data.append(scraper.try_scrape(browser))

    scraper = NovelScraperES()
    print("Scraping ", scraper.country_name)
    data.append(scraper.try_scrape(browser))

    scraper = NovelScraperIT()
    print("Scraping ", scraper.country_name)
    data.append(scraper.try_scrape(browser))

    scraper = NovelScraperPT()
    print("Scraping ", scraper.country_name)
    data.append(scraper.try_scrape(browser))

    scraper = NovelScraperNL()
    print("Scraping ", scraper.country_name)
    data.append(scraper.try_scrape(browser))

    scraper = NovelScraperBE()
    print("Scraping ", scraper.country_name)
    data.append(scraper.try_scrape(browser))

    scraper = NovelScraperCH()
    print("Scraping ", scraper.country_name)
    data.append(scraper.try_scrape(browser))

    scraper = NovelScraperAT()
    print("Scraping ", scraper.country_name)
    data.append(scraper.try_scrape(browser))

    scraper = NovelScraperRU()
    print("Scraping ", scraper.country_name)
    data.append(scraper.try_scrape(browser))

    scraper = NovelScraperPL()
    print("Scraping ", scraper.country_name)
    data.append(scraper.try_scrape(browser))

    scraper = NovelScraperBY()
    print("Scraping ", scraper.country_name)
    data.append(scraper.try_scrape(browser))

    scraper = NovelScraperUA()
    print("Scraping ", scraper.country_name)
    data.append(scraper.try_scrape(browser))

    scraper = NovelScraperGR()
    print("Scraping ", scraper.country_name)
    data.append(scraper.try_scrape(browser))


    for country in data:
        print(country)
    print("Total cases: {}".format(sum(i.cases for i in data)))

    browser.quit()

def single_test():
    #browser = webdriver.Firefox()
    browser = None

    scraper = NovelScraperGR()
    data = scraper.scrape(browser)

    print(data)

    #browser.quit()

def main():
    #test()
    single_test()
