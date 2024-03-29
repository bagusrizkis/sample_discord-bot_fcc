import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


client = discord.Client()

sad_words = ['sad', 'depressed', 'unhappy', 'angry', 'depressing']

starter_encouragments = [
  'Cheer up!',
  'Hang in there',
  'You are grate person / bot!'
]

if 'responding' not in db.keys():
  db['responding'] = True

def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return (quote)

def update_encouragments(encouragments_message):
  if 'encouragments' in db.keys():
    encouragments = db['encouragments']
    encouragments.append(encouragments_message)
    db['encouragments'] = encouragments
  else:
    db['encouragments'] = [encouragments_message]

def delete_encouragment(index):
  encouragments = db['encouragments']
  if len(encouragments) > index:
    del encouragments[index]
    db['encouragments'] = encouragments

@client.event
async def on_ready():
  print('We have login as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  msg = message.content
  
  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db['responding']:
    option = starter_encouragments
    if "encouragments" in db.keys():
      option = option + db['encouragments']

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(option))

  if msg.startswith('$new'):
    encouragments_message = msg.split('$new ', 1)[1]
    update_encouragments(encouragments_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith('$del'):
    encouragments = []
    if "encouragments" in db.keys():
      index = int(msg.split('$del', 1)[1])
      delete_encouragment(index)
      encouragments = db['encouragments']
    await message.channel.send(encouragments)

  if msg.startswith('$list'):
    encouragments = []
    if "encouragments" in db.keys():
      encouragments = db['encouragments']
    await message.channel.send(encouragments)

  if msg.startswith("$responding"):
    value = msg.split("$responding ", 1)[1]

    if value.lower() == 'true' or value.lower() == 'on':
      db['responding'] = True
      await message.channel.send("Responding is on.")
    else:
      db['responding'] = False
      await message.channel.send("Responding is off.")

keep_alive()
client.run(os.getenv('TOKEN'))