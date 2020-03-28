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


class InvestigatorBot():
    def __init__(self):
        load_dotenv()
        self.TOKEN = os.getenv('DISCORD_TOKEN')
        self.GUILD = os.getenv('DISCORD_GUILD')
        self.client = InvestigatorDiscordClient()
        self.client.init(self.GUILD)
        # Thread

    def start(self):
        asyncio.get_child_watcher()

        loop = asyncio.get_event_loop()
        loop.create_task(self.start_client())

        self.thread = Thread(target = self.run, args=(loop,))
        self.thread.start()
        print("Started separate thread for Discord Bot")

    def run(self, loop):
        loop.run_forever()

    async def start_client(self):
        await self.client.start(self.TOKEN)
        #self.client.run(self.TOKEN)

    def stop(self):
        self.thread.join()
        self.client.close()

class InvestigatorDiscordClient(discord.Client):
    def init(self, guild):
        self.GUILD = guild
        self.bot_submission_text = "Beep boop! Submitting my investigations for inspection!"
        self.bot_status_text = "the web for Covid-19"

    async def on_ready(self):
        server = discord.utils.get(self.guilds, name=self.GUILD)
        print(f'{self.user} is connected to the following server:')
        print(f'{server.name}(id: {server.id})')
        channel = discord.utils.get(server.channels, name="general") 
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=self.bot_status_text))
        await channel.send(self.bot_submission_text, file=discord.File('output/sweden-2020-03-27 23:24:44.901708.png'))
        await channel.send('= 3046 209 92 https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/aktuellt-epidemiologiskt-lage/')

        