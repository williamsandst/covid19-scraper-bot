"""
Main file
This is a program which scrapes the Coronavirus confirmed cases, deaths and recovered from various countries health ministry websites
"""

from novelscraper import *
from nordic_scrapers import *
from commands import *
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
commands = {}
results = {}

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
    country_classes[scraper.country_name.lower()] = scraper

    # Latvia
    scraper = NovelScraperAuto()
    scraper.country_name = "Latvia" 
    scraper.iso_code = "LV"
    scraper.source_website = "https://arkartassituacija.gov.lv/"
    #scraper.training_data = {"cases": "280", "tested":"11702", "hospitalised": "21"}
    country_classes[scraper.country_name.lower()] = scraper

    # Sweden
    scraper = NovelScraperAuto()
    scraper.country_name = "Sweden"
    scraper.iso_code = "SE"
    scraper.javascript_required = True
    scraper.optimize_min_max_index_ratio = 0.1
    scraper.source_website = "https://fohm.maps.arcgis.com/apps/opsdashboard/index.html#/68d4537bf2714e63b646c37f152f1392"
    scraper.report_website = "https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/aktuellt-epidemiologiskt-lage/"
    #scraper.training_data = {"cases": "3046", "deaths": "92", "intensive_care": "209"}
    country_classes[scraper.country_name.lower()] = scraper

    # Denmark
    # Cases are divided up by regions, can't be parsed with auto
    scraper = NovelScraperDK()
    country_classes[scraper.country_name.lower()] = scraper

    # Finland
    scraper = NovelScraperAuto()
    scraper.country_name = "Finland"
    scraper.iso_code = "FI"
    scraper.javascript_required = True
    scraper.source_website = "https://korona.kans.io/"
    #scraper.training_data = {"cases": "1056", "deaths": "7", "recovered": "10"}
    country_classes[scraper.country_name.lower()] = scraper

    # Iceland
    scraper = NovelScraperAuto()
    scraper.country_name = "Iceland"
    scraper.iso_code = "IS"
    scraper.javascript_required = True
    scraper.website_scroll = True
    scraper.source_website = "https://e.infogram.com/7327507d-28f5-4e3c-b587-c1680bd790e6?src=embed"
    scraper.report_website = "https://www.covid.is/tolulegar-upplysingar"
    #scraper.training_data = {"cases": "890", "recovered": "97", "hospitalised":"18", "intensive_care":"6", "tested":"13613"}
    country_classes[scraper.country_name.lower()] = scraper

"""def main():
    init_countries()
    #report_all()
    #train()
    scrape()
    #browser = webdriver.Firefox()

    #train_country("Iceland", browser)
    #print(scrape_country("Iceland", browser))

    #browser.quit()"""

def add_command(triggers : list, function):
    """Add a command to the global players dictionary"""
    if isinstance(triggers, str):
        commands[triggers] = function
    else:
        for trigger in triggers:
            commands[trigger] = function


def parse(input_list : list) -> dict:
    """Parse the flags of a written line into dictionary representing the flags

    The outputted dict is in the form of {FLAG:value, ...}, where value is
    Union[str, int, list]. Note that the preceeding '-' is removed from flag dict key. 
    The default arguments (with no flag, connecting directly to the command) are stored under
    the flag 'default'
    """
    flags = {}
    if len(input_list) > 1:
        i = 1
        while i < len(input_list) and not (input_list[i][0] == '-' and input_list[i][1].isalpha()):
            flags.setdefault("default", [])
            if isinstance(input_list[i], str):
                input_list[i] = input_list[i].lower()
            flags["default"].append(input_list[i])
            i += 1
        flag = ''
        for value in input_list[i:]:
            if value[0] == '-':
                flag = value[1:]
                flags[flag] = []
            else:
                flags[flag].append(value)

    for flag, args in flags.items():
        if len(args) == 0: 
            flags[flag] = None
        elif len(args) == 1: 
            flags[flag] = args[0]

    return flags

def main():
    add_command(["scrape", "sc"], lambda: cmd_scrape(country_classes, flags))
    add_command(["train", "tr"], lambda: cmd_train(country_classes, flags))
    add_command(["help", "h"], lambda: cmd_help(country_classes, flags))
    add_command(["exit", "close"], lambda: cmd_exit(country_classes, flags))

    init_countries()

    # Main input loop. Grab input, parse and execute command
    while True:
        input_list = input("\nnvlscrpr: ").split()
        flags = parse(input_list)
        if len(input_list) > 0:
            command = input_list[0]
            if command in commands:
                commands[command]()
            else:
                print("The command was not recognized. Type 'help' for a list of commands")
        else:
            print("The command was not recognized. Type 'help' for a list of commands")