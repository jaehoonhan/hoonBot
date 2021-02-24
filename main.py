import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = ["sad", 'depressed', 'unhappy', 'pissed', 'angry', 'miserable', 'depressing']
starter_encouragements = [
  'cheer up!',
  'hang in there.',
  'you are a great person!'
]

if 'responding' not in db.keys():
  db['responding'] = True
#request quote from zenquotes api
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " \n-" + json_data[0]['a']
  return quote

def update_encouragements(encouraging_message):
  if 'encouragements' in db.keys():
    encouragements = db['encouragements']
    encouragements.append(encouraging_message)
    db['encouragements'] = encouragements
  else:
    db['encouragements'] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db['encouragements']
  if len(encouragements) > index:
    del encouragements[index]
    db['encouragements'] = encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

#
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content

#test bot alive 
  if msg.startswith('$rualive'):
    await message.channel.send('Yup.')

  #send a quote from zenquotes
  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  #combine starter encouragements with db encouragements
  if db['responding']:
    options = starter_encouragements
    if 'encouragements' in db.keys():
      options = options + db['encouragements']

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))
  
  #add enouragments 
  if msg.startswith('$new'):
    #if there is anything after $new
    if len(msg) > 4:
      encouraging_message = msg.split('$add ',1)[1]
      update_encouragements(encouraging_message)
      await message.channel.send('New encouraging message added.')
  
  #delete enouragementes
  if msg.startswith('$del'):
    encouragements = []
    if 'encouragements' in db.keys():
      index = int(msg.split('$del ',1)[1])
      delete_encouragement(index)
      encouragements = db['encouragements']
    await message.channel.send(encouragements)
  
  #get list of encouragments
  if msg.startswith('$list'):
    encouragements = []
    if 'encouragements' in db.keys():
      encouragements = db['encouragements']
    await message.channel.send(encouragements)

  #turning the bot on and off
  if msg.startswith('$responding'):
    value = msg.split('$responding ', 1)[1]

    if value.lower() == 'on':
      db['responding'] = True
      await message.channel.send('Responding is on.')
    elif value.lower() == 'off':
      db['responding'] = False
      await message.channel.send('Responding is off.') 

keep_alive()
client.run(os.getenv('TOKEN'))

#