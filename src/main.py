"""
Main file
This is a program which scrapes the Coronavirus confirmed cases, deaths and recovered from various countries health ministry websites
"""

from selenium import webdriver

from novelscraper import *

""" 
Countries with working scraping:
Norway (NO)
Sweden (SE)
Denmark (DK)
"""

def test():
    """Scrapes numbers for all programmed countries"""
    data = list()

    browser = webdriver.Firefox()

    scraper = NovelScraperNO()
    print("Scraping ", scraper.country_name)
    data.append(scraper.scrape(browser))

    scraper = NovelScraperSE()
    print("Scraping ", scraper.country_name)
    data.append(scraper.scrape(browser))

    scraper = NovelScraperDK()
    print("Scraping ", scraper.country_name)
    data.append(scraper.scrape(browser))

    scraper = NovelScraperFI()
    print("Scraping ", scraper.country_name)
    data.append(scraper.scrape(browser))

    scraper = NovelScraperIS()
    print("Scraping ", scraper.country_name)
    data.append(scraper.scrape(browser))

    for country in data:
        print(country)

    browser.quit()

def single_test():
    browser = None#webdriver.Firefox()

    scraper = NovelScraperIS()
    data = scraper.scrape(browser)

    print(data)

    #browser.quit()

def main():
    test()
    #single_test()
