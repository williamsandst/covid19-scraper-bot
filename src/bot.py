import os

import discord
from dotenv import load_dotenv

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
# I also want to support a few commands, like:
# !scrape, which scrapes the selected channel/country and then does a submission
# So that would be bot -> command -> scrape() -> bot
# Commands supported:
# scrape [COUNTRY/ALL]
# train  [COUNTRY] [TRAIN_DICT]
# schedule [ON/OFF]
# quit
# help

def test():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')

    class InvestigatorClient(discord.Client):
        async def on_ready(self):
            server = discord.utils.get(self.guilds, name=GUILD)
            print(f'{self.user} is connected to the following guild:\n')
            print(f'{server.name}(id: {server.id})')
            channel = discord.utils.get(server.channels, name="general") 
            await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the web for Covid-19"))
            await channel.send("Beep boop! Submitting my investigations for inspection!",file=discord.File('output/sweden-2020-03-27 23:24:44.901708.png'))
            await channel.send('= 3046 209 92 https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/aktuellt-epidemiologiskt-lage/')

    client = InvestigatorClient()
    client.run(TOKEN)