import requests
import json
import time
from datetime import datetime
import asyncio
import aiohttp
import os
import discord
from discord.utils import get

client = discord.Client()

# get non public strings
# MAPQUEST key
f=open("mapquest_token.txt","r")
if f.mode == 'r':
    api_key = f.read()

# start address    
f=open("start_address.txt","r")
if f.mode == 'r':
    start_addr = f.read()

# end address    
f=open("end_address.txt","r")
if f.mode == 'r':
    end_addr = f.read()

enabled = False
done = False

# ========================
# Create Message Function
# ========================
def create_message(direction, text_body, api_key, start_addr, end_addr):

  traveltime = -444
  newtime = -444
  roundedTime = -444
  time_int = -444

  # JSON get

  # Direction = 1 From Home to Work
  # Direction = 2 From Work to Home
  if direction == 1:
    response = requests.get("https://www.mapquestapi.com/directions/v2/route?key=" + api_key + start_addr)
  elif direction == 2:
    response = requests.get("https://www.mapquestapi.com/directions/v2/route?key=" + api_key + end_addr)
  else:
    return None
  # JSON load
  try:
    body = json.loads(response.content)
  except:
    print("Response Failed :" + str(response.status_code))
    return

  # read travel time
  traveltime = (body["route"]["realTime"])

  # convert to minutes
  newtime = traveltime / 60
  
  # round value
  roundedTime = round(newtime)

  #cut off all decimals
  time_int = int(roundedTime)

  #concat message text with results if greater than slow time
  if direction == 1:
    text_body = text_body + " to work is " + str(time_int) + " min."
  elif direction == 2:
    text_body = text_body + " to home is " + str(time_int) + " min."
  else:
    text_body = ''

  return (time_int,text_body)

async def mainloop(manual):
  global done
  # init variables
  text_body = "Estimated travel time"
  post_time = 0
  slow_time = 30

  # get date and time info
  now = datetime.now()
  dayofweek = now.weekday()
  hour = now.hour
  minute = now.minute

  # is today a weekday
  if dayofweek != 5 and dayofweek != 6:
    weekday = True
  else:
    weekday = False

  # is now morning or afternoon
  if hour < 10 and hour >= 7:
    # home to work
    direction = 1
  elif hour < 19 and hour >= 16:
    # work to home
    direction = 2
  else:
    direction = 0

  channel = client.get_channel(872238015420981318)
    
  if manual == 1 and enabled:
    message = create_message(direction, text_body, api_key, start_addr, end_addr)
    if message != None:
      if int(message[0]) < 9999:
        await channel.send(message[1])
      else:
        pass


  if weekday == True and direction != 0 and enabled:
    if manual == 0:
      message = create_message(direction, text_body, api_key, start_addr, end_addr)
      if message != None:
        if int(message[0]) >= slow_time and int(message[0] < 9999):
          await channel.send(message[1])
        else:
          pass

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
      await mainloop(0)
    async def looping_function(self):
        while True:
            await self.do_stuff()
            await asyncio.sleep(10*60)

@client.event
async def on_message(message):

  if str(message.channel) == "traffic":

    if str(message.author) != "TrafficBot#5586":

      if message.content == "clear" or message.content == "Clear":
        messages = await message.channel.history(limit=123).flatten()
        await messages.delete()
      else:
        await message.delete()
        await mainloop(1)



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

# get discord token
f=open("discord_token.txt","r")
if f.mode == 'r':
    discordToken = f.read()

client.run(discordToken)
