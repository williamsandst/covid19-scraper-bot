"""Main file """

from bs4 import BeautifulSoup
import html5lib
import time

from selenium import webdriver

def main():
    print("Scraping https://www.vg.no/spesial/2020/corona/...")
    browser = webdriver.Firefox()
    browser.get('https://www.vg.no/spesial/2020/corona/')
    time.sleep(4)
    page = browser.page_source
    browser.quit()

    soup = BeautifulSoup(page, "html5lib")
    print("Finished scraping website")

    confirmed = soup.find("span", class_="absolute confirmed").contents[0]
    dead = soup.find("span", class_="absolute dead").contents[0]
    print("Confirmed cases {}".format(confirmed))
    print("Confirmed dead {}".format(dead))


    """text_file = open("output.txt", "w")
    text_file.write(soup.prettify())
    text_file.close()"""
    #print(soup.find_all("span", class_="deadNorway").prettify())
    #print(soup.find_all("2 540"))
