"""
Main file
This is a program which scrapes the Coronavirus confirmed cases, deaths and recovered from various countries health ministry websites
"""

from selenium import webdriver

from novelscraper import *

""" 
Countries with working scraping:
Norway (NO)
"""

def main():
    #retrieveNumbers("")
    browser = webdriver.Firefox()

    scraper = NovelScraperNO()
    data = scraper.scrape(browser)
    print(data)

    browser.quit()
