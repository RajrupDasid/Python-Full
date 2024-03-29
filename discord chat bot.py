Python 3.7.8 (tags/v3.7.8:4b47a5b6ba, Jun 28 2020, 08:53:46) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


client = discord.Client()
sad_words = ["I am sad","sad","Depressed","not feeling well","angry","depressing"]
starter_encouragement = ["Cheer Up!","Hang on there","you are a great person","Don't be sad ","Everything will be fine soon"]


if "responding" not in db.keys():
  db ["responding"] = True

def get_quote():
  response = requests.get ("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + "-"+ json_data[0]['a']
  return (quote)
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db ["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db ["encouragements"] = [encouraging_message] 
def delete_encouragement(index):
  encouragements = db ["encouragements"]
  if len(encouragements)>index:
    del encouragements[index]
    db ["encouragements"] = encouragements

@client.event 
async def on_ready():
  print ('We have logged in as {0.user}'.format(client))


@client.event 
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content
  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  if db["responding"]:
    options = starter_encouragement
    if "encouragements" in db.keys():
      options = options + db ["encouragements"]

    if  any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")
  if msg.startswith("$del"):
    encouragements =[]
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = db ["encouragements"]
      await message.channel.send(encouragements)
  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db ["encouragements"]
      await message.channel.send(encouragements)
  if msg.startswith("$responding"):
    value = msg.split("responding",1)[1]

    if value.lower()== "true":
      db["responding"] = True
      await message.channel.send("Responding Activated.")
    else:
      db["responding"] = False
      await message.channel.send("Responding deactivated")
keep_alive()
client.run(os.getenv('TOKEN'))