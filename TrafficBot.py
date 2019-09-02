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
discordToken = "NjE3OTIyMTU3MTA4MDAyODE2.XWyOag.I73zCWedHYBFf-t54QczV19DSjE"

# ========================
# Create Message Function
# ========================
def createMessage(direction, textBody):

  slow_time = 25

  # MAPQUEST key
  key = "09YpJEQitPjYEwu5rY9ANn2sqb8tUVjp"

  # JSON get

  # Direction = 1 From Home to Work
  # Direction = 2 From Work to Home
  if direction == 1:
    response = requests.get("https://www.mapquestapi.com/directions/v2/route?key=" + key + "&from=5300+Los+Altos+PkwySparks%2C+NV+89436&to=1+Electric+Ave%2C+Sparks%2C+NV+89434&outFormat=json&ambiguities=ignore&routeType=fastest&doReverseGeocode=false&enhancedNarrative=false&avoidTimedConditions=false")
  elif direction == 2:
    response = requests.get("https://www.mapquestapi.com/directions/v2/route?key=" + key + "&from=1+Electric+Ave%2C+Sparks%2C+NV+89434&to=5300+Los+Altos+PkwySparks%2C+NV+89436&outFormat=json&ambiguities=ignore&routeType=fastest&doReverseGeocode=false&enhancedNarrative=false&avoidTimedConditions=false")
  else:
    return None
  # JSON load
  body = json.loads(response.content)

  # read travel time
  traveltime = (body["route"]["realTime"])

  # convert to minutes
  traveltime = traveltime / 60

  # round value
  traveltime = round(traveltime)

  #cut off all decimals
  time_int = int(traveltime)

  if time_int > slow_time:
    #concat message text with results if greater than slow time
    if direction == 1:
      textBody = textBody + " to work is " + str(time_int) + " min."
    elif direction == 2:
      textBody = textBody + " to home is " + str(time_int) + " min."
  else:
    textBody = ''

  return textBody


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

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
        print('test')
        # init variables
        textBody = "Estimated travel time"

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

        if weekday == False or direction != 0:
          message = createMessage(direction, textBody)
          print(message)
          test = 'test'
          await client.send_message(client.get_channel('534045914227277847'), test)

    async def looping_function(self):
        while True:
            await self.do_stuff()
            await asyncio.sleep(3)

loop = asyncio.get_event_loop()
Daily_Poster = MyCog
Daily_Poster(loop)

@client.event
async def on_message(message):
    print(message.channel)


client.run(discordToken)
