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
discordToken = "NjE3OTIyMTU3MTA4MDAyODE2.XWyOag.I73zCWedHYBFf-t54QczV19DSjE"
enabled = False
done = False

# ========================
# Create Message Function
# ========================
def createMessage(direction, textBody):

  traveltime = -444
  newtime = -444
  roundedTime = -444
  time_int = -444

  # MAPQUEST key
  key = "09YpJEQitPjYEwu5rY9ANn2sqb8tUVjp"

  # JSON get

  # Direction = 1 From Home to Work
  # Direction = 2 From Work to Home
  if direction == 1:
    response = requests.get("https://www.mapquestapi.com/directions/v2/route?key=" + key + "&from=3550+heron's+landing+drive%2C+reno+NV+80502&to=1+Electric+Avenue%2C+sparks+NV+89434&outFormat=json&ambiguities=ignore&routeType=fastest&doReverseGeocode=false&enhancedNarrative=false&avoidTimedConditions=false")
  elif direction == 2:
    response = requests.get("https://www.mapquestapi.com/directions/v2/route?key=" + key + "&from=1+Electric+Avenue%2C+sparks+NV+89434&to=3550+heron's+landing+drive%2C+reno+NV+80502&outFormat=json&ambiguities=ignore&routeType=fastest&doReverseGeocode=false&enhancedNarrative=false&avoidTimedConditions=false")
  else:
    return None
  # JSON load
  body = json.loads(response.content)

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
    textBody = textBody + " to work is " + str(time_int) + " min."
  elif direction == 2:
    textBody = textBody + " to home is " + str(time_int) + " min."
  else:
    textBody = ''

  return (time_int,textBody)

async def mainloop(manual):
  global done
  # init variables
  textBody = "Estimated travel time"
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
    
  if manual == 1 and enabled:
    message = createMessage(direction, textBody)
    if int(message[0]) < 9999:
      await client.send_message(client.get_channel('534045914227277847'), message[1])
    else:
      pass


  if weekday == True and direction != 0 and enabled:
    if manual == 0:
      message = createMessage(direction, textBody)
      if int(message[0]) >= slow_time and int(message[0] < 9999):
        await client.send_message(client.get_channel('534045914227277847'), message[1])
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
        await client.delete_messages(messages)
      else:
        await client.delete_message(message)
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

client.run(discordToken)
