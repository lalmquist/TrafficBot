import requests
import json
from twilio.rest import Client
import time
from datetime import datetime
import asyncio
import aiohttp
import os
import discord
from discord.utils import get

client = discord.Client()
discordToken = "NjE4MTcwNDU0MTEyMjA2ODU2.XW2KDQ.dAyxi8LtHGgqZ2qUHyvSKhQsSNM"
enabled = False
TempProbe = "28-051760d567ff"

def read(i):
    location = '/sys/bus/w1/devices/'+i+'/w1_slave'
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    celcius = temperature / 1000
    farenheit = (celcius * 1.8) + 32
    return farenheit

# ========================
# Create Message Function
# ========================

async def mainloop():
    global enabled

    if enabled == True:
        message = read(TempProbe)
        await client.send_message(client.get_channel('618116119848288276'), message)


class MyCog(object):
    def __init__(self,bot):
        self.bot = bot
        self.looped_task = bot.create_task(self.looping_function())
        self.data = {}
    
    def __unload(self):
        try:
            self.looped_task.cancel()
        except (AttributeError, asyncio.CancelledError):
            pass
    
    async def do_stuff(self):
      await mainloop()
    async def looping_function(self):
        while True:
            await self.do_stuff()
            await asyncio.sleep(10)



@client.event
async def on_message(message):

  if str(message.channel) == "temperature":

    if str(message.author) != "TemperatureBot#0960":
      await client.delete_message(message)
      await mainloop()

@client.event
async def on_ready():
    global enabled
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    enabled = True



loop = asyncio.get_event_loop()
Daily_Poster = MyCog
Daily_Poster(loop)

client.run(discordToken)
