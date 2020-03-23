"""
Main file
This is a program which scrapes the Coronavirus confirmed cases, deaths and recovered from various countries health ministry websites
"""

from selenium import webdriver

from novelscraper import *
from nordic_scrapers import *

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

    for country in data:
        print(country)

    browser.quit()

def single_test():
    #browser = webdriver.Firefox()
    browser = None

    scraper = NovelScraperIE()
    data = scraper.scrape(browser)

    print(data)

    #browser.quit()

def main():
    test()
    #single_test()
