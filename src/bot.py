import os

import discord
from dotenv import load_dotenv
from threading import Thread
import asyncio

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

country_to_channel_dict = {"czechia": "czech-republic"}

class InvestigatorBot():
    def __init__(self):
        load_dotenv()
        self.TOKEN = os.getenv('DISCORD_TOKEN')
        self.GUILD = os.getenv('DISCORD_GUILD')
        self.client = InvestigatorDiscordClient()
        self.client.init(self.GUILD)
        self.asyncio_event_loop = asyncio.get_event_loop()
        self.thread = Thread(target = self.run)

    def start(self):
        self.asyncio_event_loop.create_task(self.start_client())
        self.thread.start()
        print("Started separate thread for Discord Bot")

    def convert_country_to_channel(self, country):
        if country in country_to_channel_dict:
            return country_to_channel_dict[country]
        else:
            return country

    def run(self):
        self.asyncio_event_loop.run_forever()

    def submit(self, country, string, screenshot_path):
        channel = self.convert_country_to_channel(country)
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
        self.GUILD = guild
        self.bot_submission_text = "Beep boop! Submitting my investigations for inspection!"
        self.bot_status_text = "the web for Covid-19"

    async def on_ready(self):
        self.server = discord.utils.get(self.guilds, name=self.GUILD)
        print(f'{self.user} is connected to the following server:')
        print(f'{self.server.name}(id: {self.server.id})')
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=self.bot_status_text))

    async def send_submission(self, string, channel, screenshot_path):
        channel = discord.utils.get(self.server.channels, name=channel) 
        await channel.send(self.bot_submission_text, file=discord.File(screenshot_path))
        await channel.send(string)