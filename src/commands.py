import time
import copy
import logging

from selenium import webdriver

import interface
from novelscraper import *
import bot

log = logging.getLogger("MAIN")

def train(country_classes):
    browser = webdriver.Firefox()

    log.info("Starting training...")
    for country in country_classes:
        if country_classes[country].training_data != None:
            train_country(country, browser, country_classes)
        else:
            log.warning("{}: Missing training data".format(country_classes[country].get_pretty_name()))
    log.info("Training complete!")
    browser.quit()

def train_country(country, browser, country_classes):
    country_name = country_classes[country].get_pretty_name()
    log.info("{}: Training recognition model...".format(country_name))
    country_classes[country].train(browser)
    log.info("{}: Training complete!".format(country_name))

def scrape(country_classes, scrape_type="default", date=datetime.datetime.now(), browser=None, country_group=None):

    results = {}

    create_browser = (browser == None)
    
    if scrape_type == "default" or scrape_type == "d":
        if create_browser:
            browser = webdriver.Firefox()

        for country in country_classes:
            if country_classes[country].has_auto and (country_group == None or country_classes[country].group_name == country_group):
                results[country] = scrape_country_auto(country, browser, country_classes)
        if create_browser:
            browser.quit()

    elif scrape_type == "covidtracking" or scrape_type == "ct" or scrape_type == "covidtracker":
        for country in country_classes:
            if country_classes[country].has_covidtracking and (country_group == None or country_classes[country].group_name == country_group):
                results[country] = scrape_country_coronatracking(country, country_classes, date)

    elif scrape_type == "hopkins" or scrape_type == "johnhopkins" or scrape_type == "john" or scrape_type == "jh":
        for country in country_classes:
            if country_classes[country].has_hopkins and (country_group == None or country_classes[country].group_name == country_group):
                results[country] = scrape_country_hopkins(country, country_classes, date)


    return results


def scrape_country_auto(country: str, browser, country_classes):
    country_name = country_classes[country].get_pretty_name()
    log.info("{}: Scraping...".format(country_name))
    result = country_classes[country].scrape(browser)
    log.info("{}: Scraping complete!".format(country_name))
    return result

def scrape_country_coronatracking(country: str, country_classes, date):
    country_name = country_classes[country].get_pretty_name()
    log.info("{}: Scraping from Covidtracking.com...".format(country_name))
    result = country_classes[country].scrape_covidtracking(date)
    log.info("{}: Scraping complete!".format(country_name))
    return result

def scrape_country_hopkins(country: str, country_classes, date):
    country_name = country_classes[country].get_pretty_name()
    log.info("{}: Scraping from John Hopkins Github...".format(country_name))
    result = country_classes[country].scrape_hopkins(date)
    log.info("{}: Scraping complete!".format(country_name))
    return result


def screenshot_country(country, browser, country_classes):
    return country_classes[country].screenshot(browser)


lenient_on_recovery = True

def are_results_valid(result, country, date, ignore_cache_timeout = False):
    # Compare with current data in the sheet
    sheet_data = downloader.check_from_sheet(country, "SE", date, ignore_cache_timeout)
    if sheet_data.data_validity == "OK":
        """if sheet_data.cases > result.cases:
            result.data_validity = "Scraped cases are lower than the sheet value for {}".format(date)
            return False
        if sheet_data.deaths > result.deaths:
            result.data_validity = "Scraped deaths are lower than the sheet value for {}".format(date)
            return False
        if not lenient_on_recovery:
                if sheet_data.recovered > result.recovered:
                    result.data_validity = "Scraped recovered are lower than the sheet value for {}".format(date)
                    return False"""
        #else:
        if config.ALLOW_RECOVERY_SHEET_ADJUSTMENT and result.use_sheet_recovered  and result.recovered < sheet_data.recovered:
            log.info("Data validation: Doing recovery adjustment from sheet data")
            result.recovered = max(result.recovered, sheet_data.recovered)
        if config.ALLOW_DEATH_SHEET_ADJUSTMENT and result.use_sheet_deaths and result.deaths < sheet_data.deaths:
            log.info("Data validation: Doing death adjustment from sheet data")
            result.deaths = max(result.deaths, sheet_data.deaths)
    # Other checks
    if result.cases < result.deaths:
        result.data_validity = "Scraped cases are less than scraped deaths"
        return False
    return True

    
    

#List of commands
command_list = """List of commands for Novel-Scraper:
help                                Lists commands for Novel-Scraper
exit                                Exit Novel-Scraper
scrape <country/ALL> [-f]           Scrape a selected country, or 'ALL' for all of them. -f to save submissions to file
train <country> [train_dict]        Train a country with their internal training dictionary or supply one as argument
"""

scraping_types = {"default", "d", "covidtracking", "covidtracker", "ct", "hopkins", "johnhopkins", "john", "jh"}

def cmd_scrape(country_classes: dict, flags: dict, discord_bot: bot.InvestigatorBot, browser):
    if "default" not in flags or (not isinstance(flags["default"], str) and len(flags["default"]) > 2):
        error_message("The required arguments are missing or are incorrectly formated")
        return
    if 'r' in flags: #Multiple days, do a secondary call
        dayrange = flags['r']
        new_flags = copy.deepcopy(flags)
        new_flags.pop('r', None)
        dayrange = dayrange.split("-")
        start_day = interface.convert_string_to_datetime(dayrange[0])
        end_day = interface.convert_string_to_datetime(dayrange[1])
        date_range = interface.get_date_range(start_day, end_day)
        log.info("Performing scrape on date range {} - {}".format(start_day, end_day))
        for date in date_range:
            date_str = interface.convert_datetime_to_string(date)
            new_flags['t'] = date_str
            cmd_scrape(country_classes, new_flags, discord_bot, browser)
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
    if country.lower() == "europe":
        #Scraping all registered countries
        results = scrape(country_classes, scraping_type, date, browser, "Europe")
    elif country.lower() == "usa":
        results = scrape(country_classes, scraping_type, date, browser, "USA")
    elif country.lower() == "canada":
        results = scrape(country_classes, scraping_type, date, browser, "Canada")
    elif country in country_classes:
        class_dict = {country: country_classes[country]}
        results = scrape(class_dict, scraping_type, date, browser)
    else:
        error_message("The specified country {} is not registered".format(country))
        return

    if not 'nocheck' in flags and not config.DISABLE_SHEET_ERROR_CHECKING: #Check validity of scraped data
        log.info("Checking scrape result validity...")
        for result_country, result in results.items():
            country_sheet_name = bot.convert_country_index_to_channel(result_country)
            if not are_results_valid(result, country_sheet_name, date, 'cacheonly' in flags):
                log.warning("Detected bad data for " + result.pretty_country_name)
        

    if 'nodisp' not in flags:
        for country, result in results.items():
            if result.data_validity != "OK":
                log.warning("Error: " + result.data_validity)
            log.info(result)

    if 'f' in flags:
        submission_string = interface.create_submissions(results)
        save_to_file(submission_string, "output/submissions.txt")
    
    if 'd' in flags:
        for country, result in results.items():
            if result.data_validity == "OK":
                if result.cases > 0:
                    submission_string = interface.convert_dataobject_to_submission(result)
                    submission_additional_data_str = None
                    if config.SUBMIT_ADDITIONAL_DATA:
                        submission_additional_data_str = interface.convert_dataobject_to_additional_data_string(result)
                    discord_bot.submit(country, submission_string, result.screenshot_path, submission_additional_data_str)
                else:
                    discord_bot.send_message("Zero cases reported on the date {} for {}, omitting submission".format(interface.convert_datetime_to_string(date), result.pretty_country_name), country)
                    log.info("Omitted submission to Discord due to zero cases")
            else:
                submission_string = interface.convert_dataobject_to_submission(result)
                log.warning("Submission data is bad due to: {}".format(result.data_validity))
                discord_bot.send_error("{} (resulting in submission: {})".format(result.data_validity, submission_string),country)
            time.sleep(2)

def cmd_train(country_classes: dict, flags: dict, discord_bot: bot.InvestigatorBot, browser):
    if "default" not in flags or not isinstance(flags["default"], str):
        error_message("The required arguments are missing or are incorrectly formated")
        return

    country = flags["default"]

    if "data" in flags: #Assigned data from command
        training_data = {}
        if isinstance(flags["data"], dict):
            for label in flags["data"]:
                flags["data"][label] = str(flags["data"][label])
            training_data = flags["data"]
        elif isinstance(flags["data"], list):
            training_data["cases"] = flags["data"][0]
            training_data["deaths"] = flags["data"][1]
            if len(flags["data"]) > 2:
                training_data["recovered"] = flags["data"][2]
        elif isinstance(flags["data"], str):
            training_data["cases"] = flags["data"]
        country_classes[country].training_data = training_data

    create_browser = (browser == None)
    if create_browser:
        browser = webdriver.Firefox()
    train_country(country.lower(), browser, country_classes)
    if create_browser:
        browser.quit()

    if "d" in flags:
        discord_bot.send_message("Trained a recognition model for {} based on provided data".format(country_classes[country].get_pretty_name()), country)

def cmd_screenshot(country_classes: dict, flags: dict, discord_bot: bot.InvestigatorBot, browser):
    if "default" not in flags or not isinstance(flags["default"], str):
        error_message("The required arguments are missing or are incorrectly formated")
        return
    country = flags["default"]
    pretty_country_name = country_classes[country].get_pretty_name()

    create_browser = (browser == None)

    saved_wait_time = country_classes[country].wait_time
    if 'f' in flags and not country_classes[country].javascript_required: #Flag for decreasing wait time for faster screenshots
        country_classes[country].wait_time = 0

    if country_classes[country].source_website != None:
        if create_browser:
            browser = webdriver.Firefox()
        path = screenshot_country(country.lower(), browser, country_classes)
        if create_browser:
            browser.quit()    
        if 'nodisp' not in flags:
            log.info("Took screenshot of {}, saved at {}".format(pretty_country_name, path))
            
    if 'd' in flags:
        source = country_classes[country].report_website if country_classes[country].report_website != None else country_classes[country].source_website
        if source != None:
            discord_bot.send_screenshot(pretty_country_name, path, source)
        else:
            discord_bot.send_error("This country does not yet have a source specified", pretty_country_name)

    country_classes[country].wait_time = saved_wait_time

def cmd_help(country_classes: dict, flags: dict):
    """cmd: help. Print the help string, containing command descriptions"""
    print(command_list)

def cmd_exit(country_classes: dict, flags: dict, discord_bot: bot.InvestigatorBot, browser):
    """cmd: exit. Exit the program"""
    log.info("Exiting Novel-Scraper... This can take a few seconds.")
    if browser != None:
        browser.quit()
        log.info("Stopped Webdriver")
    discord_bot.stop()
    log.info("Stopped Discord bot")
    config.REBOOT_ON_CRASH = False
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