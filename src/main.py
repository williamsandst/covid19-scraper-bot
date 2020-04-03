"""
Main file
This is a program which scrapes the Coronavirus confirmed cases, deaths and recovered from various countries health ministry websites
"""

import interface
from threading import Thread
import time
import datetime
import queue

from novelscraper import *
from manual_scrapers import *
from commands import *
import bot

""" 
Countries with working automated scraping:
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
Left:
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
scheduled_commands = []
results = {}
discord_bot = bot.InvestigatorBot()

DISCORD_BOT_ENABLED = False

def init_europe_scrapers():
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

    # Sweden
    scraper = NovelScraperAuto()
    scraper.country_name = "Sweden"
    scraper.iso_code = "SE"
    scraper.javascript_required = True
    scraper.wait_time = 10
    scraper.optimize_min_max_index_ratio = 0.1
    scraper.source_website = "https://fohm.maps.arcgis.com/apps/opsdashboard/index.html#/68d4537bf2714e63b646c37f152f1392"
    scraper.report_website = "https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/aktuellt-epidemiologiskt-lage/"
    #scraper.training_data = {"cases": "3046", "deaths": "92", "intensive_care": "209"}
    country_classes[scraper.country_name.lower()] = scraper

    # Denmark
    # Cases are divided up by regions, can't be parsed with auto
    scraper = NovelScraperDK()
    country_classes[scraper.country_name.lower()] = scraper

    # Iceland
    scraper = NovelScraperAuto()
    scraper.country_name = "Iceland"
    scraper.iso_code = "IS"
    scraper.javascript_required = True
    scraper.website_scroll = 6
    scraper.source_website = "https://e.infogram.com/7327507d-28f5-4e3c-b587-c1680bd790e6?src=embed"
    scraper.report_website = "https://www.covid.is/tolulegar-upplysingar"
    #scraper.training_data = {"cases": "890", "recovered": "97", "hospitalised":"18", "intensive_care":"6", "tested":"13613"}
    country_classes[scraper.country_name.lower()] = scraper

    # Finland
    scraper = NovelScraperAuto()
    scraper.country_name = "Finland"
    scraper.iso_code = "FI"
    scraper.javascript_required = True
    scraper.source_website = "https://korona.kans.io/"
    #scraper.training_data = {"cases": "1056", "deaths": "7", "recovered": "10"}
    country_classes[scraper.country_name.lower()] = scraper

    # Estonia
    scraper = NovelScraperAuto()
    scraper.country_name = "Estonia" 
    scraper.iso_code = "EE"
    scraper.source_website = "https://www.koroonakaart.ee/en"
    #scraper.training_data = {"cases": "640",  "deaths": "1", "recovered":"20", "tested":"9364", "hospitalised": "48"}
    country_classes[scraper.country_name.lower()] = scraper

    # Lithuania
    scraper = NovelScraperAuto()
    scraper.country_name = "Lithuania" 
    scraper.iso_code = "LI"
    scraper.source_website = "https://sam.lrv.lt/lt/naujienos/koronavirusas"
    scraper.scroll = 7
    scraper.training_data = {"cases": "382",  "deaths": "5", "recovered":"1", "tested":"6900"}
    country_classes[scraper.country_name.lower()] = scraper

    # Latvia
    scraper = NovelScraperAuto()
    scraper.country_name = "Latvia" 
    scraper.iso_code = "LV"
    scraper.source_website = "https://arkartassituacija.gov.lv/"
    #scraper.training_data = {"cases": "280", "tested":"11702", "hospitalised": "21"}
    country_classes[scraper.country_name.lower()] = scraper

    # Central Europe
    # The United Kingdom
    scraper = NovelScraperAuto()
    scraper.country_name = "United-Kingdom"
    scraper.iso_code = "GB"
    scraper.javascript_required = True
    scraper.report_link = "https://www.gov.uk/government/publications/covid-19-track-coronavirus-cases"
    scraper.source_website = "https://www.arcgis.com/apps/opsdashboard/index.html#/f94c3c90da5b4e9f9a0b19484dd4bb14"
    #scraper.training_data = {"cases": "17089", "recovered":"135", "deaths": "1019"}
    country_classes[scraper.country_name.lower()] = scraper

    # Ireland
    scraper = NovelScraperAuto()
    scraper.country_name = "Ireland"
    scraper.iso_code = "IE"
    scraper.javascript_required = True
    scraper.source_website = "https://www.gov.ie/en/news/7e0924-latest-updates-on-covid-19-coronavirus/"
    #scraper.training_data = {"cases": "2415", "deaths": "36"}
    country_classes[scraper.country_name.lower()] = scraper

    # Germany
    scraper = NovelScraperAuto()
    scraper.country_name = "Germany"
    scraper.iso_code = "DE"
    scraper.javascript_required = True
    scraper.source_website = "https://interaktiv.morgenpost.de/corona-virus-karte-infektionen-deutschland-weltweit-teaser/"
    #scraper.training_data = {"cases": "54268", "deaths": "398", "recovered":"3781"}
    country_classes[scraper.country_name.lower()] = scraper

    # France
    """# Can't scrape images. Should probably do a custom one
    scraper = NovelScraperAuto()
    scraper.country_name = "France"
    scraper.iso_code = "FR"
    scraper.javascript_required = True
    scraper.source_website = "https://www.santepubliquefrance.fr/maladies-et-traumatismes/maladies-et-infections-respiratoires/infection-a-coronavirus/articles/infection-au-nouveau-coronavirus-sars-cov-2-covid-19-france-et-monde"
    #scraper.training_data = {"cases": "54268", "deaths": "398", "recovered":"3781"}
    country_classes[scraper.country_name.lower()] = scraper
    """

    # Spain
    scraper = NovelScraperAuto()
    scraper.country_name = "Spain"
    scraper.iso_code = "ES"
    scraper.javascript_required = True
    scraper.optimize_min_max_index_ratio = 0.1
    scraper.source_website = "https://www.rtve.es/noticias/20200328/mapa-del-coronavirus-espana/2004681.shtml"
    #scraper.training_data = {"cases": "73235", "deaths": "5982", "recovered":"12285", "intensive_care":"4575"}
    country_classes[scraper.country_name.lower()] = scraper

    # Italy
    scraper = NovelScraperAuto()
    scraper.country_name = "Italy"
    scraper.iso_code = "IT"
    scraper.javascript_required = True
    scraper.optimize_min_max_index_ratio = 0.05
    scraper.source_website = "https://datastudio.google.com/u/0/reporting/91350339-2c97-49b5-92b8-965996530f00/page/RdlHB"
    #scraper.training_data = {"cases": "92472", "deaths": "10023", "recovered":"12384", "intensive_care":"3856", "hospitalsied":"30532", "tested":"429526"}
    country_classes[scraper.country_name.lower()] = scraper

    # Portugal
    scraper = NovelScraperAuto()
    scraper.country_name = "Portugal"
    scraper.iso_code = "PT"
    scraper.javascript_required = True
    scraper.report_website = "https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/"
    scraper.source_website = "https://esriportugal.maps.arcgis.com/apps/opsdashboard/index.html#/e9dd1dea8d1444b985d38e58076d197a"
    #scraper.training_data = {"cases": "5170", "deaths": "100", "recovered":"43"}
    country_classes[scraper.country_name.lower()] = scraper

    # The Netherlands
    scraper = NovelScraperAuto()
    scraper.country_name = "Netherlands"
    scraper.iso_code = "NL"
    scraper.optimize_min_max_index_ratio = 0.2
    scraper.source_website = "https://www.rivm.nl/nieuws/actuele-informatie-over-coronavirus"
    #scraper.training_data = {"cases": "9762", "deaths": "639", "hospitalised":"2954"}
    country_classes[scraper.country_name.lower()] = scraper

    # Belgium
    scraper = NovelScraperAuto()
    scraper.country_name = "Belgium"
    scraper.iso_code = "BE"
    scraper.optimize_min_max_index_ratio = 0.2
    scraper.source_website = "https://www.info-coronavirus.be/fr/2020/03/24/526-nouvelles-infections-au-covid-19/"
    #scraper.training_data = {"cases": "4269", "deaths": "122", "recovered":"410", "hospitalised":"1859", "intensive_care":"381"}
    country_classes[scraper.country_name.lower()] = scraper


    # Switzerland
    scraper = NovelScraperAuto()
    scraper.country_name = "Switzerland"
    scraper.iso_code = "CH"
    scraper.optimize_min_max_index_ratio = 0.2
    scraper.source_website = "https://www.bag.admin.ch/bag/en/home/krankheiten/ausbrueche-epidemien-pandemien/aktuelle-ausbrueche-epidemien/novel-cov/situation-schweiz-und-international.html"
    #scraper.training_data = {"cases": "13213", "deaths": "235"}
    country_classes[scraper.country_name.lower()] = scraper

    # Austria
    scraper = NovelScraperAuto()
    scraper.country_name = "Austria"
    scraper.iso_code = "AT"
    scraper.optimize_min_max_index_ratio = 0.2
    scraper.website_scroll = 5
    scraper.source_website = "https://www.sozialministerium.at/Informationen-zum-Coronavirus/Neuartiges-Coronavirus-(2019-nCov).html"
    #scraper.training_data = {"cases": "7995", "deaths": "68", "tested":"42750"}
    country_classes[scraper.country_name.lower()] = scraper

def init_us_scrapers():
    # Alabama
    scraper = NovelScraperAuto()
    scraper.country_name = "Alabama" 
    scraper.iso_code = "AL"
    scraper.has_covidtracking = True
    country_classes[scraper.country_name.lower()] = scraper


def add_command(triggers : list, function, commands=commands):
    """Add a command to the global players dictionary"""
    if isinstance(triggers, str):
        commands[triggers] = function
    else:
        for trigger in triggers:
            commands[trigger] = function

def add_scheduled_command(command: str, time: datetime):
    scheduled_commands.append([command, time])

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

ENABLE_EXTERNAL_COMMANDS = True

def time_is_approximate_equal(time1: datetime.datetime, time2: datetime.datetime):
    allowed_offset = 2
    seconds1 = time1.hour*3600 + time1.minute*60 + time1.second
    seconds2 = time2.hour*3600 + time2.minute*60 + time2.second
    if (seconds1 + allowed_offset) > seconds2 and (seconds1 - allowed_offset) < seconds2:
        return True
    return False

class SchedulingThread(Thread):
    def __init__(self, queue, flags, args=(), kwargs=None):
        Thread.__init__(self, args=(), kwargs=None)
        self.commands = {}
        self.queue = queue

    def run(self):
        add_command(["scrape", "sc"], lambda: cmd_scrape(country_classes, self.flags, discord_bot), self.commands)
        while True:
            # Scheduling
            timenow = datetime.datetime.now()
            for command in scheduled_commands:
                if time_is_approximate_equal(command[1], timenow):
                    #Execute command
                    command_list = command[0].split()
                    self.flags = parse(command_list)
                    print("{}: Executing scheduled command: {}".format(command[1], command[0]))
                    self.commands[command_list[0]]()
            time.sleep(2)
            # Go through external commands
            while not self.queue.empty():
                command = self.queue.get()
                command_list = command.split()
                self.flags = parse(command_list)
                print("Executing external command: {}".format(command))
                self.commands[command_list[0]]()

def main():
    flags = {}
    t = datetime.datetime(year=2020, month=1, day=1, hour=13, minute=14, second=0)
    add_scheduled_command("scrape latvia", t)

    add_command(["scrape", "sc"], lambda: cmd_scrape(country_classes, flags, discord_bot))
    add_command(["train", "tr"], lambda: cmd_train(country_classes, flags, discord_bot))
    add_command(["help", "h"], lambda: cmd_help(country_classes, flags))
    add_command(["exit", "close"], lambda: cmd_exit(country_classes, flags, discord_bot))

    init_europe_scrapers()
    init_us_scrapers()
    command_queue = queue.Queue()

    scheduling_thread = SchedulingThread(command_queue, flags)
    scheduling_thread.start()

    # Start discord bot
    if (DISCORD_BOT_ENABLED):
        print("Starting the Investigator Discord Bot")
        discord_bot.set_command_queue(command_queue)
        discord_bot.start()
        time.sleep(5)
        print("Bot started")

    # Main input loop. Grab input, parse and execute command
    while True:
        input_list = input("\nnvlscrpr: ").split()
        flags = parse(input_list)
        #scheduling_thread.queue.put("scrape latvia")
        if len(input_list) > 0:
            command = input_list[0]
            if command in commands:
                commands[command]()
            else:
                print("The command was not recognized. Type 'help' for a list of commands")
        else:
            print("The command was not recognized. Type 'help' for a list of commands")