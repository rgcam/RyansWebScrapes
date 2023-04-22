# botbot.py
import asyncio
from dotenv import load_dotenv
import DataScrapeTheTenzing
import datetime
import discord
from discord import Webhook as wh
from discord import RequestsWebhookAdapter
from discord.ext.commands import Bot
import os
from discord.ext.tasks import loop
import time

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_GENERAL = os.getenv('DISCORD_GENERAL')
CHANNEL_LOG = os.getenv('DISCORD_LOG')

SPIDEY_TOKEN = os.getenv('SPIDEY_BOT_WEBHOOK_TOKEN')
SPIDEY_ID = os.getenv('SPIDEY_BOT_WEBHOOK_ID')

LOG_TOKEN = os.getenv('LOGGERHEAD_WEBHOOK_TOKEN')
LOG_ID = os.getenv('LOGGERHEAD_WEBHOOK_ID')

client = discord.Client()

webhook_general = wh.partial(SPIDEY_ID, SPIDEY_TOKEN, adapter=RequestsWebhookAdapter())
webhook_log  = wh.partial(LOG_ID, LOG_TOKEN, adapter=RequestsWebhookAdapter())

_loop = asyncio.get_event_loop()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == CHANNEL_GENERAL:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n -'.join([member.name for member in guild.members])
    print('\n Guild Members:\n -' + members)
    print(str(client.user.name) + " is connected!") 

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "Hello" or message.content == "hello":
        greeting = "Hello!"
        await message.channel.send(greeting)
    if message.content == "Availability" or message.content == "availability":
        stats = DataScrapeTheTenzing.ScrapeTenzing()
        webhook_general.send("The Tenzing 3 Bedroom Availability:" + 
                        "\nFloor Plan: " + stats[0] + 
                        "\nBed/Bath: " + stats[1] +
                        "\nRent: " + stats[3] + stats[4] + 
                        "\n" +stats[5])

@loop(seconds=60)
async def Scrapes():
    rent = ""
    await client.wait_until_ready()
    while client.is_closed:
        check_time = datetime.datetime.now()
        current_hour = int(check_time.strftime('%H'))
        current_min = int(check_time.strftime('%M'))
        if current_hour >= 11 and current_hour < 19:
            t = datetime.datetime.now()
            stats = DataScrapeTheTenzing.ScrapeTenzing()
            if current_hour < 11 and current_hour >= 19:
                break
            elif rent != stats[3] + stats[4]:
                myid = os.getenv('RGCAM')
                webhook_general.send("The Tenzing 3 Bedroom Availability:" + 
                        "\n<@" + myid + ">" +
                        "\nFloor Plan: " + stats[0] + 
                        "\nBed/Bath: " + stats[1] +
                        "\nRent: " + stats[3] + stats[4] + 
                        "\n" +stats[5])
                #webhook_general.send("<@" + myid + "> rent has changed!")
                rent = stats[3] + stats[4]
            print("Scraped at " + t.strftime('%I:%M %p'))
            webhook_log.send("Scraped at " + t.strftime('%I:%M %p'))
            time.sleep(60)
        else:
            print("Complex is closed.")
            webhook_log.send("Complex is closed.")
            if current_hour <= 11:
                hour_adjust = 0
            if current_hour >=7:
                hour_adjust = 11
            hours_in_seconds = (23 - current_hour + hour_adjust) * 3600
            minutes_in_seconds = (60 - current_min) * 60
            sleeptime = hours_in_seconds + minutes_in_seconds
            webhook_log.send("Sleeping for " + str((sleeptime/60)/60) + " hours.")
            time.sleep(sleeptime)


Scrapes.start()
client.run(TOKEN)
