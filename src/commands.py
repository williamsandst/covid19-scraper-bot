from selenium import webdriver
import interface
from novelscraper import *

def train(country_classes):
    browser = webdriver.Firefox()

    print("Starting training...")
    for country in country_classes:
        if country_classes[country].training_data != None:
            train_country(country, browser, country_classes)
        else:
            print("{}: Missing training data".format(country))
    print("Training complete!")
    browser.quit()

def train_country(country, browser, country_classes):
    country_name = country_classes[country].country_name
    print("{}: Training recognition model...".format(country_name))
    country_classes[country].train(browser)
    print("{}: Training complete!".format(country_name))

def scrape(country_classes):
    browser = webdriver.Firefox()

    results = {}

    for country in country_classes:
        results[country] = scrape_country(country, browser, country_classes)

    browser.quit()

    return results

def scrape_country(country: str, browser, country_classes):
    country_name = country_classes[country].country_name
    print("{}: Scraping...".format(country_name))
    result = country_classes[country].scrape(browser)
    print("{}: Scraping complete!".format(country_name))
    return result

#List of commands
command_list = """List of commands for Novel-Scraper:
help                                Lists commands for Novel-Scraper
exit                                Exit Novel-Scraper
scrape <country/ALL> [-f]           Scrape a selected country, or 'ALL' for all of them. -f to save submissions to file
train <country> [train_dict]        Train a country with their internal training dictionary or supply one as argument
"""

def cmd_scrape(country_classes: dict, flags: dict):
    if "default" not in flags or not isinstance(flags["default"], str):
        error_message("The required arguments are missing or are incorrectly formated")
        return
    country = flags["default"]
    results = {}
    if country.lower() == "all":
        #Scraping all registered countries
        results = scrape(country_classes)
    elif country in country_classes:
        browser = webdriver.Firefox()
        results[country] = scrape_country(country, browser, country_classes)
        browser.quit()
    else:
        error_message("The specified country {} is not registered".format(country))
        return

    for country, result in results.items():
        print(result)

    if 'f' in flags:
        submission_string = interface.create_submissions(results)
        save_to_file(submission_string, "output/submissions.txt")


def cmd_train(country_classes: dict, flags: dict):
    if "default" not in flags or not isinstance(flags["default"], str):
        error_message("The required arguments are missing or are incorrectly formated")
        return
    country = flags["default"]


def cmd_help(country_classes: dict, flags: dict):
    """cmd: help. Print the help string, containing command descriptions"""
    print(command_list)

def cmd_exit(country_classes: dict, flags: dict):
    """cmd: exit. Exit the program"""
    print("Exiting Novel-Scraper...")
    exit()

def error_message(reason):
    """Support function for logging error messages related to functions"""
    print("Command failure: {}. Please try again.".format(reason))