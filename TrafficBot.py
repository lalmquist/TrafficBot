import requests
import json
from datetime import datetime
import asyncio
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

# ========================
# Create Message Function
# ========================
def create_message(direction, text_body, api_key, start_addr, end_addr):

  # init value to default error
  traveltime = -444

  # JSON get

  # Direction = 1 From Home to Work
  # Direction = 2 From Work to Home
  if direction == 1:
    response = requests.get("https://www.mapquestapi.com/directions/v2/route?key=" + api_key + start_addr)
  elif direction == 2:
    response = requests.get("https://www.mapquestapi.com/directions/v2/route?key=" + api_key + end_addr)
  else:
    return(-444,"invalid direction")
  
  # JSON load
  try:
    body = json.loads(response.content)
  except:
    print("Response Failed :" + str(response.status_code))
    return(-444,"API Response Failed")

  # read travel time
  traveltime = (body["route"]["realTime"])

  # convert to minutes and round
  traveltime = int(round(traveltime / 60))
  
  #concat message text with results if greater than slow time
  if direction == 1:
    text_body = text_body + " to work is " + str(traveltime) + " min."
  elif direction == 2:
    text_body = text_body + " to home is " + str(traveltime) + " min."

  return (traveltime,text_body)

async def mainloop(manual):
  # init variables
  text_body = "Estimated travel time"
  
  # auto post traffic times if longer than this
  slow_time = 30

  # 9999 is an error/invalid response from API
  invalidresponse = 9999

  # get date and time info
  dt = datetime.now()
  hour = dt.hour

  # is today a weekday
  if dt.weekday() < 5:
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
  elif manual:
    # default home to work for manual trigger outside range
    direction = 1

  # get "traffic" channel in personal server
  channel = client.get_channel(872238015420981318)

  if direction > 0 and enabled:
    if manual or weekday:
      message = create_message(direction, text_body, api_key, start_addr, end_addr)
    else:
      return
    
    if manual:
        # always send message for manual trigger unless invalid response
        if message[0] < invalidresponse:
          await channel.send(message[1])

    elif weekday:
        # only send auto message if traffic detected
        if message[0] >= slow_time and message[0] < invalidresponse:
          await channel.send(message[1])

  else:
    print("invalid direction or bot not loaded yet")

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
      await mainloop(False)
    async def looping_function(self):
        while True:
            await self.do_stuff()
            await asyncio.sleep(10*60)

@client.event
async def on_message(message):
  # only look at messages in traffic channel from users
  if str(message.channel) == "traffic":
    if str(message.author) != "TrafficBot#5586":
      message_lower = message.content.lower()
      # Clear command
      if message_lower == "clear":
        messages = await message.channel.history(limit=50).flatten()
        for message in messages:
          await message.delete()
      # Anything else, trigger response
      else:
        await message.delete()
        await mainloop(True)

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