# bot.py
import os
import discord
import asyncio
from dotenv import load_dotenv
import time
import DataScrapeTheTenzing
import datetime
from discord import Webhook as wh
from discord import RequestsWebhookAdapter
# d 
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

WH_TOKEN = os.getenv('SPIDEY_BOT_WEBHOOK_TOKEN')
WH_ID = os.getenv('SPIDEY_BOT_WEBHOOK_ID')

client = discord.Client()
webhook = wh.partial(WH_ID, WH_TOKEN, adapter=RequestsWebhookAdapter())

"""
async def background_scrape_timer():
    print("in bg task")
    await client.wait_until_ready()
    counter = 0
    channel = discord.Object(id=GUILD)
    while not client.is_closed:
        print("in while")
        counter += 1
        await webhook.send("The Tenzing 3 Bedroom Availability:")
        await asyncio.sleep(60) # sleep to stop loop after first iteration in the minute
        print("asleep")
"""

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n -'.join([member.name for member in guild.members])
    print('\n Guild Members:\n -' + members)
    print(str(client.user.name) + " is connected!") 

# @client.command
# async def mention(self, ctx, member : discord.Member):
#     await ctx.send(f"{member}")  

@client.event
async def on_message(message):

    
    if message.author == client.user:
        return

    if message.content == "Hello" or message.content == "hello":
        greeting = "Hello!"
        await message.channel.send(greeting)
    
    if message.content == "Availability" or message.content == "availability":
        stats = DataScrapeTheTenzing.ScrapeWebpage()
        webhook.send("The Tenzing 3 Bedroom Availability:" + 
                        "\nFloor Plan: " + stats[0] + 
                        "\nBed/Bath: " + stats[1] +
                        "\nRent: " + stats[3] + stats[4] + 
                        "\n" +stats[5])
   

_loop = asyncio.get_event_loop()

async def my_background_task():
    rent = ""
    while True:
        if datetime.datetime.now().minute % 15 == 0: 
            stats = DataScrapeTheTenzing.ScrapeWebpage()
            webhook.send("__________________________________")
            webhook.send("The Tenzing 3 Bedroom Availability:" + 
                        "\nFloor Plan: " + stats[0] + 
                        "\nBed/Bath: " + stats[1] +
                        "\nRent: " + stats[3] + stats[4] + 
                        "\n" +stats[5])

            # webhook.send("Floor Plan: " + stats[0])
            # webhook.send("Bed/Bath: " + stats[1])
            # webhook.send("Rent: " + stats[3] + stats[4])
            # webhook.send(stats[5])

            time.sleep(60)

            if rent != stats[3] + stats[4] and rent != "":
                myid = os.getenv('RGCAM')
                webhook.send("<@" + myid + "> rent has changed!")

            else:
                continue

            rent = stats[3] + stats[4]
        else: 
            continue
        time.sleep((15 - datetime.datetime.now().minute % 15) * 60)


# client.loop.create_task(background_scrape_timer())
client.loop.create_task(my_background_task())
client.run(TOKEN)
# time.wait(5)

