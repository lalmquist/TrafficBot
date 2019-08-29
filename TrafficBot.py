import requests
import json
from twilio.rest import Client
import time
from datetime import datetime

active = True

# ========================
# Create Message Function
# ========================
def createMessage(direction, textBody):

  # MAPQUEST key
  key = "09YpJEQitPjYEwu5rY9ANn2sqb8tUVjp"

  # JSON get

  # Direction = 1 From Home to Work
  # Direction = 2 From Work to Home
  if direction == 1:
    response = requests.get("https://www.mapquestapi.com/directions/v2/route?key=" + key + "&from=5300+Los+Altos+PkwySparks%2C+NV+89436&to=1+Electric+Ave%2C+Sparks%2C+NV+89434&outFormat=json&ambiguities=ignore&routeType=fastest&doReverseGeocode=false&enhancedNarrative=false&avoidTimedConditions=false")
  elif direction == 2:
    response = requests.get("https://www.mapquestapi.com/directions/v2/route?key=" + key + "&from=1+Electric+Ave%2C+Sparks%2C+NV+89434&to=5300+Los+Altos+PkwySparks%2C+NV+89436&outFormat=json&ambiguities=ignore&routeType=fastest&doReverseGeocode=false&enhancedNarrative=false&avoidTimedConditions=false")

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
    #concat message text with results if greater than 30
    textBody = textBody + " to home is " + str(time_int) + " min."
  else:
    textBody = ''

  return textBody


# =================
#      TWILIO
# =================

def sendMessage(textBody):
  # account info
  account_sid = "AC971886628ee7db10eced8b061317719d"
  auth_token = "bf8e72bb0446e7d45b902d70536099ef"

  # create client
  client = Client(account_sid, auth_token)

  # send message
  client.messages.create(
    to="+16035122895",
    from_="+19782342385",
    body=textBody)


while active:

  # init variables
  textBody = "Estimated travel time"
  
  slow_time = 25

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

  # if not weekday or travel time, exit
  if weekday == False or direction != 0:

    message = createMessage(direction, textBody)

    if message != "":
      sendMessage(message)

    time.sleep(30*60)
