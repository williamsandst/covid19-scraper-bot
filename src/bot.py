import os

import discord
from dotenv import load_dotenv
from threading import Thread
import asyncio
from queue import Queue
import datetime

import interface

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

country_to_channel_dict = {"czechia": "czech-republic", "united kingdom": "uk"}

channel_to_country_dict = {v: k for k, v in country_to_channel_dict.items()}

channel_blacklist_set = {"welcome", "info", "rules", "general", "lounge", "music", "dev-bot", "bot-suggestions", "sheet-suggestions",
                        "europe", "andorra", "albania", "austria", "belarus", "belgium", "bosnia-and-herzegovina", "bulgaria",
                        "croatia", "cyprus", "czech-republic", "denmark", "estonia", "finland", "france", "germany", "greece", "hungary",
                        "holy-see", "iceland", "ireland", "italy", "kosovo", "latvia", "liechtenstein", "lithuania", "luxembourg", "malta",
                        "moldova", "monaco", "montenegro", "netherlands", "north-macedonia", "norway", "poland", "portugal", "romania", "russia",
                        "san-marino", "slovenia", "spain", "serbia", "slovakia", "sweden", "switzerland", "uk", "ukraine"}

user_whitelist = {"SlipShady", "Wydal"}

role_whitelist = {"staff", "the real slip shady"}

RELEASE_BOT = False

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


class InvestigatorBot():
    def __init__(self):
        load_dotenv()
        if RELEASE_BOT:
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
        print("Started separate thread for Discord Bot")

    def run(self):
        self.asyncio_event_loop.run_forever()

    def submit(self, country, string, screenshot_path):
        if self.active:
            channel = convert_country_to_channel(country)
            self.asyncio_event_loop.create_task(self.client.send_submission(string, channel, screenshot_path))

    async def start_client(self):
        await self.client.start(self.TOKEN)
        #self.client.run(self.TOKEN)

    def stop(self):
        self.asyncio_event_loop.create_task(self.client.close())
        self.asyncio_event_loop.stop()
        self.thread.join()
        print("Discord Bot stopped")

class InvestigatorDiscordClient(discord.Client):
    def init(self, guild):
        self.bot_status_text = "the web for Covid-19"
        self.bot_submission_text = "Beep boop! Submitting my investigations for inspection!"
        self.GUILD = guild

    async def on_ready(self):
        self.server = discord.utils.get(self.guilds, name=self.GUILD)
        self.novel_bot_id = discord.utils.get(self.server.members, name="Wydal").id
        print(f'{self.user} is connected to the following server:')
        print(f'{self.server.name}(id: {self.server.id})')
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=self.bot_status_text))

    async def send_submission(self, string, channel_input, screenshot_path):
        channel = discord.utils.get(self.server.channels, name=channel_input)
        if channel != None: 
            if screenshot_path != None:
                await channel.send(self.bot_submission_text, file=discord.File(screenshot_path))
            else:
                await channel.send(self.bot_submission_text)
            await channel.send(string)
        else:
            print("Bot: Cannot find channel {}".format(channel_input))

    async def send_check(self, channel): #Send check
        channel = discord.utils.get(self.server.channels, name=channel) 
        await channel.send("chk")

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
        # we do not want the bot to reply to itself

        if (message.author == self.user or str(message.channel) in channel_blacklist_set or message.author.name not in user_whitelist):
            return
        has_permission = False
        for role in message.author.roles:
            if role.name.lower() in role_whitelist:
                has_permission = True
        if not has_permission:
            return

        """if message.author.id == self.novel_bot_id: #Read check and save it
            country = convert_channel_to_country(str(message.channel))
            channel = message.channel
            interface.process_check(country, str(message.content))
            await channel.send("Praise the Creator")
            return"""

        if message.content.startswith('!scrape'):
            channel = message.channel
            country = convert_channel_to_country(str(message.channel))
            country = country[0].upper() + country[1:]

            words = message.content.split()
            if len(words) >= 2 and (words[1] == "covidtracker" or words[1] == "covidtracking" or words[1] == "ct"): 
                time = datetime.datetime.now()
                date = interface.convert_datetime_to_string(time)
                if len(words) >= 3: #Date argument
                    date = words[2]
                    if len(words) > 5:
                        print("!scrape date incorrectly formatted")
                        return
                    date = words[2]
                    

                await channel.send("Beep boop! Investigating Covid-19 cases in {}, please stand by...".format(country))
                if str(channel) == "usa":
                    self.command_queue.put("scrape all covidtracking -d -disp -t {}".format(date))
                else:
                    self.command_queue.put("scrape {} ct -d -disp -t {}".format(country, date))
        
        #if message.content.startswith('check'):
            #channel = message.channel
            #await self.fake_check(channel)