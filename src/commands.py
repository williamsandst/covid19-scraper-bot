from selenium import webdriver
import interface
from novelscraper import *
import bot
import time

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

def scrape(country_classes, scrape_type="default", date=datetime.datetime.now()):

    results = {}

    if scrape_type == "default" or scrape_type == "d":
        browser = webdriver.Firefox()

        for country in country_classes:
            if country_classes[country].has_default:
                results[country] = scrape_country_default(country, browser, country_classes)

        browser.quit()

    elif scrape_type == "covidtracking" or scrape_type == "ct" or scrape_type == "covidtracker":
        for country in country_classes:
            if country_classes[country].has_covidtracking:
                results[country] = scrape_country_coronatracking(country, country_classes, date)

    return results


def scrape_country_default(country: str, browser, country_classes):
    country_name = country_classes[country].country_name
    print("{}: Scraping...".format(country_name))
    result = country_classes[country].scrape(browser)
    print("{}: Scraping complete!".format(country_name))
    return result

def scrape_country_coronatracking(country: str, country_classes, date):
    country_name = country_classes[country].country_name
    print("{}: Scraping from Covidtracking.com...".format(country_name))
    result = country_classes[country].scrape_covidtracking(date)
    print("{}: Scraping complete!".format(country_name))
    return result

def screenshot_country(country, browser, country_classes):
    return country_classes[country].screenshot(browser)


#List of commands
command_list = """List of commands for Novel-Scraper:
help                                Lists commands for Novel-Scraper
exit                                Exit Novel-Scraper
scrape <country/ALL> [-f]           Scrape a selected country, or 'ALL' for all of them. -f to save submissions to file
train <country> [train_dict]        Train a country with their internal training dictionary or supply one as argument
"""

scraping_types = {"default", "d", "covidtracking", "covidtracker", "ct"}

def cmd_scrape(country_classes: dict, flags: dict, discord_bot: bot.InvestigatorBot):
    if "default" not in flags or (not isinstance(flags["default"], str) and len(flags["default"]) > 2):
        error_message("The required arguments are missing or are incorrectly formated")
        return
    scraping_type = "default"
    if len(flags["default"]) == 2: #Second argument, specifies scraping type
        if flags["default"][1] not in scraping_types:
            error_message("The scraping type is incorrect")
            return
        scraping_type = flags["default"][1]
        country = flags["default"][0]
    else:
        country = flags["default"]

    if 't' in flags and isinstance(flags["t"], str):
        date = interface.convert_string_to_datetime(flags['t'])
    else:
        date = datetime.datetime.now()

    results = {}
    if country.lower() == "all":
        #Scraping all registered countries
        results = scrape(country_classes, scraping_type, date)
    elif country in country_classes:
        class_dict = {country: country_classes[country]}
        results = scrape(class_dict, scraping_type, date)
    else:
        error_message("The specified country {} is not registered".format(country))
        return

    if 'nodisp' not in flags:
        for country, result in results.items():
            print(result)

    if 'f' in flags:
        submission_string = interface.create_submissions(results)
        save_to_file(submission_string, "output/submissions.txt")
    
    if 'd' in flags:
        for country, result in results.items():
            submission_string = interface.convert_dataobject_to_submission(result)
            discord_bot.submit(country, submission_string, result.screenshot_path)
            print("Sent submission to Discord")
            time.sleep(1)

def cmd_train(country_classes: dict, flags: dict, discord_bot: bot.InvestigatorBot):
    if "default" not in flags or not isinstance(flags["default"], str):
        error_message("The required arguments are missing or are incorrectly formated")
        return
    country = flags["default"]
    browser = webdriver.Firefox()
    train_country(country.lower(), browser, country_classes)
    browser.quit()

def cmd_screenshot(country_classes: dict, flags: dict, discord_bot: bot.InvestigatorBot):
    if "default" not in flags or not isinstance(flags["default"], str):
        error_message("The required arguments are missing or are incorrectly formated")
        return
    country = flags["default"]

    saved_wait_time = country_classes[country].wait_time
    if 'f' in flags: #Flag for decreasing wait time for faster screenshots
        country_classes[country].wait_time = 0

    if country_classes[country].source_website != None:
        browser = webdriver.Firefox()
        path = screenshot_country(country.lower(), browser, country_classes)
        browser.quit()    
        if 'nodisp' not in flags:
            print("Took screenshot of {}, saved at {}".format(country, path))
            
    if 'd' in flags:
        source = country_classes[country].report_website if country_classes[country].report_website != None else country_classes[country].source_website
        if source != None:
            discord_bot.send_screenshot(country, path, source)
        else:
            discord_bot.send_error("This country does not yet have a source specified", country)

    country_classes[country].wait_time = saved_wait_time

def cmd_help(country_classes: dict, flags: dict):
    """cmd: help. Print the help string, containing command descriptions"""
    print(command_list)

def cmd_exit(country_classes: dict, flags: dict, discord_bot: bot.InvestigatorBot):
    """cmd: exit. Exit the program"""
    print("Exiting Novel-Scraper... This can take a few seconds.")
    discord_bot.stop()
    exit()

def cmd_discord_chat(country_classes, flags, discord_bot: bot.InvestigatorBot):
    if "default" not in flags or not isinstance(flags["default"], list) or len(flags["default"]) != 2:
        error_message("The required arguments are missing or are incorrectly formated")
        return
    message = flags["default"][0]
    channel = flags["default"][1]
    discord_bot.chat(message, channel)

def error_message(reason):
    """Support function for logging error messages related to functions"""
    print("Command failure: {}. Please try again.".format(reason))