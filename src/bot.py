import os

import discord
from dotenv import load_dotenv
from threading import Thread
import asyncio
from queue import Queue
import datetime
import logging
import config
import utils

import interface
import country_templates
from bot_data import *

# What should it do?
# Send submission messages to any channel (text and images)
# Read data from check

# How should the entire system work?
# I want a command line interface where I can give commands
# command -> scrape() -> bot
# The bot should always be on in a separate thread
# I then send a result object to the bot, containing the screenshot path as well
# The bot then figures out where to publish the submission, compares with check and so forth
# Despite the command line input I should still be able to schedule automatic scrapes, so
# scheduling -> scrape() -> bot

# Read the check. 

log = logging.getLogger("DBOT")

country_to_channel_dict = {}

channel_to_country_dict = {v: k for k, v in country_to_channel_dict.items()}

staff_user_whitelist = {"SlipShady", "Wydal"}

staff_role_whitelist = {"staff", "the real slip shady"}

normal_role_whitelist = {"interpol"}

def convert_country_to_channel(country):
    if country in country_to_channel_dict:
        return country_to_channel_dict[country]
    else:
        return country

def convert_channel_to_country(channel):
    if channel in channel_to_country_dict:
        return channel_to_country_dict[channel]
    else:
        return channel

def convert_country_index_to_channel(country_index):
    if country_index in country_templates.country_aliases_extended_reverse:
        return country_templates.country_aliases_extended_reverse[country_index]
    else:
        return country_index

def create_dict_from_message(message):
    d = {}
    for pair in message:
        key, value = pair.split("=")
        d[key] = value
    return d

class InvestigatorBot():
    def __init__(self):
        load_dotenv()
        if config.RELEASE_BOT:
            self.TOKEN = os.getenv('DISCORD_TOKEN')
            self.GUILD = os.getenv('DISCORD_GUILD')
        else:
            self.TOKEN = os.getenv('DISCORD_DEV_TOKEN')
            self.GUILD = os.getenv('DISCORD_DEV_GUILD')
        self.client = InvestigatorDiscordClient()
        self.client.init(self.GUILD)
        self.asyncio_event_loop = asyncio.get_event_loop()
        self.thread = Thread(target = self.run)
        self.active = False

    def set_command_queue(self, command_queue: Queue):
        self.command_queue = command_queue
        self.client.command_queue = command_queue

    def start(self):
        self.active = True
        self.asyncio_event_loop.create_task(self.start_client())
        self.thread.start()
        log.info("Started Discord Bot Thread")

    def run(self):
        self.asyncio_event_loop.run_forever()

    def submit(self, country, string, screenshot_path, additional_data = None):
        if self.active:
            split_string = string.split()
            channel = convert_country_index_to_channel(country)
            if len(split_string) <= 1 or split_string[1] == "-1":
                self.asyncio_event_loop.create_task(self.client.send_error_message("Bad submission format", channel))
            else:
                log.info("Sent Discord submission to {}".format(channel))
                self.asyncio_event_loop.create_task(self.client.send_submission(string, channel, screenshot_path, additional_data))

    def send_screenshot(self, country, screenshot_path, source):
        channel = convert_country_index_to_channel(country)
        date = screenshot_path.split("|")[1][:-4]
        country_formatted = country[0].upper() + country[1:] 
        message = "Screenshot of {}, taken at {} from <{}>".format(country_formatted, date, source)
        self.asyncio_event_loop.create_task(self.client.send_image(message, screenshot_path, channel))

    def send_message(self, message, channel):
        channel = convert_country_index_to_channel(channel)
        self.asyncio_event_loop.create_task(self.client.send_message(message, channel))

    def send_error(self, reason, channel):
        channel = convert_country_index_to_channel(channel)
        self.asyncio_event_loop.create_task(self.client.send_error_message(reason, channel))

    async def start_client(self):
        await self.client.start(self.TOKEN)
        #self.client.run(self.TOKEN)

    def stop(self):
        self.asyncio_event_loop.create_task(self.client.close())
        self.asyncio_event_loop.stop()
        self.thread.join()
        log.info("Discord Bot and thread stopped")

class InvestigatorDiscordClient(discord.Client):
    def init(self, guild):
        self.bot_status_text = "the web for Covid-19"
        self.bot_submission_text = "Beep boop! Submitting my investigations for inspection!"
        self.bot_error_text = "Tzzzt! My investigations failed due to"
        self.GUILD = guild

    async def on_ready(self):
        self.server = discord.utils.get(self.guilds, name=self.GUILD)
        self.novel_bot_id = discord.utils.get(self.server.members, name="Wydal").id
        log.info(f'{self.user} is connected to the following server:')
        log.info(f'{self.server.name}(id: {self.server.id})')
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=self.bot_status_text))

    async def send_submission(self, string, channel_input, screenshot_path, additional_data = None):
        channel = discord.utils.get(self.server.channels, name=channel_input)
        if channel != None: 
            if additional_data != None:
                await channel.send(additional_data)
            if screenshot_path != None:
                await channel.send(self.bot_submission_text, file=discord.File(screenshot_path))
            else:
                await channel.send(self.bot_submission_text)
            await channel.send(string)
        else:
            log.warning("Bot: Cannot find channel {}".format(channel_input))

    async def send_error_message(self, reason, channel_input):
        channel = discord.utils.get(self.server.channels, name=channel_input)
        if channel != None: 
            await channel.send("{}: `{}`".format(self.bot_error_text, reason))
        else:
            log.warning("Bot: Cannot find channel {}".format(channel_input))

    async def send_message(self, message, channel_input):
        channel = discord.utils.get(self.server.channels, name=channel_input, type=discord.ChannelType.text)
        if channel != None: 
            await channel.send(message)
        else:
            log.warning("Bot: Cannot find channel {}".format(channel_input))

    async def send_image(self, message, path, channel_input):
        channel = discord.utils.get(self.server.channels, name=channel_input, type=discord.ChannelType.text)
        if channel != None: 
            if path != None:
                await channel.send(message, file=discord.File(path))
        else:
            log.warning("Bot: Cannot find channel {}".format(channel_input))

    async def send_check(self, channel): #Send check
        channel = discord.utils.get(self.server.channels, name=channel) 
        await channel.send("chk")

    def is_staff(self, user):
        staff = False
        if user.name in staff_user_whitelist:
            for role in user.roles:
                if role.name.lower() in staff_role_whitelist:
                    staff = True
                    break
        return staff

    def is_normal_user(self, user):
        normal_user = False
        for role in user.roles:
            if role.name.lower() in normal_role_whitelist:
                normal_user = True
                break
        return normal_user

    async def fake_check(self, channel):
        total_cases = 1000
        total_recovered = 9
        total_deaths = 10

        embed = discord.Embed(title="🇦🇩 __{}__ 🇦🇩 Growth Rate: `D: 1.50` || `D-1: 1.50\n`".format(str(channel.name)), color=0x6ed010)
        embed.add_field(name="`Cases`", value="Total: {} `|` Active: {}\n🆕 +{} `|`🔺 {}".format(total_cases,900,400,161), inline=True)
        embed.add_field(name="`Deaths`", value="Total: {}\n🆕 +{} `|`🔺 {}".format(total_deaths, 10, -6), inline=True)
        embed.add_field(name="`Recovered`", value="Total: {}\n🆕 +{} `|`🔺 {}".format(total_recovered, 0, 0), inline=True)
        embed.add_field(name="`Deaths/Cases`", value="Total: {}% `|` Active: {}%".format(1.32,1.32), inline=True)
        embed.add_field(name="`Deaths/(Deaths+Recovered)`", value="{}%".format(1.32), inline=True)
        embed.add_field(name="`Recovered/Cases`", value="{}%".format(1.32), inline=True)
        embed.add_field(name="`Total Pop`", value="10,078,802", inline=True)
        embed.add_field(name="`% Cases`", value="1.32", inline=True)
        embed.add_field(name="`% Deaths`", value="1.32", inline=True)
        embed.timestamp = datetime.datetime.now()

        await channel.send(embed=embed)

    async def on_message(self, message):
        """ 
        Open to all:
        !scrape
        !screenshot
        !worldometer
        !covidtracking
        !hopkins
        !coronacloud
        Admin only:
        !train CASES DEATHS RECOVERED
        !scrape (in Europe!)
        !disabletracker
        """

        """if message.author.id == self.novel_bot_id: #Read check and save it
            country = convert_channel_to_country(str(message.channel))
            channel = message.channel
            interface.process_check(country, str(message.content))
            await channel.send("Praise the Creator")
            return"""
        # we do not want the bot to reply to itself

        if (message.author == self.user or str(message.channel) in other_channels):
            return

        user_is_staff = self.is_staff(message.author)
        user_is_normal =  self.is_normal_user(message.author)

        words = message.content.split()  
        channel = message.channel
        country = convert_channel_to_country(str(message.channel))
        country = country[0].upper() + country[1:]

        if user_is_normal or user_is_staff: #Normal user commands
            if message.content.startswith('!screenshot'):    
                await channel.send("Beep boop! Taking a screenshot, please stand by...")
                if len(words) > 1 and (words[1] == "s" or words[1] == "slow"):
                    self.command_queue.put("screenshot {} -d".format(country))
                else:
                    self.command_queue.put("screenshot {} -d -f".format(country))

        if user_is_staff: #Staff only commands
            if message.content.startswith('!scrape'):
                if len(words) >= 2:
                    no_check = False
                    if words[1] == "covidtracker" or words[1] == "covidtracking" or words[1] == "ct": 
                        scrape_type = "covidtracking"
                    elif words[1] == "hopkins" or words[1] == "johnhopkins" or words[1] == "john"  or words[1] == "jh":
                        scrape_type = "hopkins"
                    elif words[1] == "auto" or words == [1] == "a":
                        scrape_type = ""
                    else:
                        await self.send_error_message("Incorrect scrape type", channel.name)
                        return
                        
                    if scrape_type == "covidtracking" and str(channel) not in us_channels:
                        await self.send_error_message("Covidtracking.com only has data on US states", channel.name)
                        return
                    if scrape_type == "hopkins" and (str(channel) not in europe_channels or str(channel) == "europe") and str(channel) not in canada_channels:
                        await self.send_error_message("John Hopkins has no data on this country/state", channel.name)
                        return

                    time = datetime.datetime.now()
                    date = interface.convert_datetime_to_string(time)
                    if len(words) >= 3: #Date argument
                        if words[2] == "nocheck" or words[2] == "nc":
                            no_check = True
                        else:
                            date = words[2]
                            if len(words) > 5:
                                log.warning("!scrape date incorrectly formatted")
                                return
                            date = words[2]
                            if len(words) >= 4:
                                if words[3] == "nocheck" or words[3] == "nc":
                                    no_check = True
                        
                    if "-" in date: #Range
                        date = "-r " + date
                    else:
                        date = "-t " + date

                    if no_check:
                        await channel.send("Beep boop! Investigating Covid-19 cases in {}, please stand by... (NOTE: ERROR CHECKING IS DISABLED!)".format(country))
                    else:
                        await channel.send("Beep boop! Investigating Covid-19 cases in {}, please stand by...".format(country))
                    no_check_str = "-nocheck" if no_check else ""
                    self.command_queue.put("scrape {} {} -d -disp {} {}".format(country, scrape_type, date, no_check_str))
            elif message.content.startswith('!abort'): #Reset the command queue
                log.info("Recieved Discord abort command, killing program...")
                self.command_queue = Queue()
                await channel.send("Initiating abort, shutting everything down...")
                exit()
            elif message.content.startswith('!log'):
                if len(words) > 1:
                    amount_of_lines = int(words[1])
                await channel.send("Beep boop! Sending the last {} lines of logging".format(amount_of_lines))
                logs = utils.tail("log_file.log", amount_of_lines)
                await channel.send(logs)
            elif message.content.startswith('!train'):
                command = words[1:]
                if len(command) > 0 and "=" not in command[0] and len(command) <= 3:
                    command = ' '.join(command)
                elif len(command) > 0 and "=" in command[0]:
                    command = "\"{}\"".format(str(create_dict_from_message(command)))
                self.command_queue.put("train {} -d -data {}".format(country, command))
                await channel.send("Beep boop! Training recognition model...")
                


 
        #if message.content.startswith('check'):
            #channel = message.channel
            #await self.fake_check(channel)