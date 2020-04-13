"""
Main file
This is a program which scrapes the Coronavirus confirmed cases, deaths and recovered from various countries health ministry websites
"""
import interface
from threading import Thread
import time
import datetime
import queue
import os
import logging
import ast

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from novelscraper import *
from manual_scrapers import *
from commands import *
from country_templates import *
import bot
import utils
import config

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
Czech Republic (CZ)
Romania (RO)
Belarus (BY) (CoronaCloud)
Ukarine (UA) (CoronaCloud)
Greece (GR) (CoronaCloud)

Andorra
Albania
Bosnia and Herzegovina
Bulgaria
Croatia
Cyprus
Hungary
Holy-see
Kosovo
Liechtenstein
Luxembourg
Malta
Moldova
Monaco
Montenegro
North Macedonia
San Marino
Slovenia
Serbia
Slovakia
"""

log = logging.getLogger("MAIN")

discord_bot = bot.InvestigatorBot()

def add_command(triggers : list, function, commands):
    """Add a command to the global players dictionary"""
    if isinstance(triggers, str):
        commands[triggers] = function
    else:
        for trigger in triggers:
            commands[trigger] = function

def add_scheduled_command(command: str, time: datetime, scheduled_commands):
    scheduled_commands.append([command, time])

def parse(input_list : list) -> dict:
    """Parse the flags of a written line into dictionary representing the flags

    The outputted dict is in the form of {FLAG:value, ...}, where value is
    Union[str, int, list]. Note that the preceeding '-' is removed from flag dict key. 
    The default arguments (with no flag, connecting directly to the command) are stored under
    the flag 'default'
    """
    flags = {}
    #Combine items marked in "" into one item
    new_input_list = []
    combine = False
    for i in input_list:
        if i.startswith("\""):
            new_input_list.append(i + " ")
            combine = True
        elif i.endswith("\""):
            combine = False
            new_input_list[-1] += i + " "
        else:
            if combine:
                new_input_list[-1] += i + " "
            else:
                new_input_list.append(i)

    input_list = new_input_list
        
    if len(input_list) > 1:
        i = 1
        while i < len(input_list) and not (input_list[i][0] == '-' and input_list[i][1].isalpha()):
            flags.setdefault("default", [])
            if isinstance(input_list[i], str):
                if input_list[i].startswith("\""):
                    input_list[i] = input_list[i][1:-2]
                else:
                    if input_list[i].lower() in country_aliases:
                        input_list[i] = country_aliases[input_list[i].lower()]
                    else:
                        input_list[i] = input_list[i].lower()
            flags["default"].append(input_list[i])
            i += 1
        flag = ''
        for value in input_list[i:]:
            if value[0] == '-':
                flag = value[1:]
                flags[flag] = []
            elif value[0] == "\"":
                flags[flag].append(value[1:-2])
            else:
                flags[flag].append(value)

    for flag, args in flags.items():
        if len(args) == 0: 
            flags[flag] = None
        elif len(args) == 1: 
            flags[flag] = args[0]

    #Convert dictionary strings to actual dictionaries
    for flag, args in flags.items():
        if isinstance(args, str) and "{" in args and "}" in args and ":" in args:
            str_dict = ast.literal_eval(args.strip()) #Safer than normal eval
            flags[flag] = str_dict
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
    def __init__(self, queue, flags, bot, browser, args=(), kwargs=None):
        Thread.__init__(self, args=(), kwargs=None)
        self.commands = {}
        self.queue = queue
        self.scheduled_commands = []
        self.discord_bot = bot
        self.browser = browser
        self.setup_schedule()

    def setup_schedule(self):
        #t = datetime.datetime(year=2020, month=1, day=1, hour=13, minute=14, second=0)
        #add_scheduled_command("scrape latvia", t, self.scheduled_commands)
        pass

    def run(self):
        add_command(["scrape", "sc"], lambda: cmd_scrape(country_classes, self.flags, self.discord_bot, self.browser), self.commands)
        add_command(["screenshot", "ss"], lambda: cmd_screenshot(country_classes, self.flags, self.discord_bot, self.browser), self.commands)
        add_command(["train", "tr"], lambda: cmd_train(country_classes, self.flags, self.discord_bot, self.browser), self.commands)
        while True:
            # Scheduling
            timenow = datetime.datetime.now()
            for command in self.scheduled_commands:
                if time_is_approximate_equal(command[1], timenow):
                    #Execute command
                    command_list = command[0].split()
                    self.flags = parse(command_list)
                    log.info("{}: Executing scheduled command: {}".format(command[1], command[0]))
                    self.commands[command_list[0]]()
                    print("\nnvlscrpr: ", end =" ")
            time.sleep(2)
            # Go through external commands
            while not self.queue.empty():
                command = self.queue.get()
                command_list = command.split()
                self.flags = parse(command_list)
                log.info("Executing external command: {}".format(command))
                self.commands[command_list[0]]()
                print("\nnvlscrpr: ",end =" ")

def init_browser():
    if config.SELENIUM_BROWSER_ALWAYS_ON:
        options = Options()
        if config.SELENIUM_FIREFOX_HEADLESS:
            options.headless = True
        browser = webdriver.Firefox(options=options)
    else:
        browser = None
    return browser

def main():
    commands = {}
    browser = init_browser()

    flags = {}

    add_command(["scrape", "sc"], lambda: cmd_scrape(country_classes, flags, discord_bot, browser), commands)
    add_command(["train", "tr"], lambda: cmd_train(country_classes, flags, discord_bot, browser), commands)
    add_command(["screenshot", "ss"], lambda: cmd_screenshot(country_classes, flags, discord_bot, browser), commands)
    add_command(["chat", "ch"], lambda: cmd_discord_chat(country_classes, flags, discord_bot), commands)
    add_command(["help", "h"], lambda: cmd_help(country_classes, flags), commands)
    add_command(["exit", "close", "quit"], lambda: cmd_exit(country_classes, flags, discord_bot, browser), commands)

    init_europe_scrapers()
    init_us_scrapers()
    init_canada_scrapers()
    create_country_aliases()
    command_queue = queue.Queue()

    scheduling_thread = SchedulingThread(command_queue, flags, discord_bot, browser)
    scheduling_thread.start()

    # Start discord bot
    if config.DISCORD_BOT_ENABLED:
        discord_bot.set_command_queue(command_queue)
        if not discord_bot.active:
            discord_bot.start()
            time.sleep(5)
        else:
            log.info("Discord Bot already initiated, skipping startup")

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