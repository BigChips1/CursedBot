import discord
import os
import requests
import random
from replit import db 
from alive import keep_alive

sad_words = ["sad", "depressed", "miserable"]
curse_words = []

if 'responding' not in db.keys():
  db['responding'] = True

def get_insult():
  response = requests.get('https://evilinsult.com/generate_insult.php?lang=en&type=json')
  return response.json()['insult']

def update_curses(curse):
  if 'curses' in db.keys():
    temp = db['curses']
    temp.append(curse)
    db['curses'] = temp
  else:
    db['curses'] = [curse]

def delete_curses(index):
  if len(db['curses']) > index:
    del db['curses'][index]
    return True
  else:
    return False

client = discord.Client() 

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$insult'):
    x = get_insult()
    await message.channel.send(x)
  
  if db["responding"]:
    options = curse_words 
    if 'curses' in db.keys():
      new_list = [word for word in db['curses']]
      options = options + new_list

    for word in sad_words:
      if word in message.content.lower():
        await message.channel.send(random.choice(options))
        break

  if message.content.startswith('$new'):
    curse = message.content.split('$new ', 1)[1].strip()
    update_curses(curse)
    await message.channel.send('Curse words updated')
  
  if message.content.startswith('$show curses'):
    await message.channel.send(options)

  if message.content.startswith('$del'):
    index = message.content.split('$del ', 1)[1].strip()
    try:
      index = int(index)
    except:
      await message.channel.send('Please enter valid index')
    if delete_curses(index):
      await message.channel.send("Successfully deleted")
    else:
      await message.channel.send("Index out of range")
    
  if message.content.startswith('$responding'):
    response = message.content.split('$responding ', 1)[1].strip()
    if response.lower() == 'true':
      db['responding'] = True
      await message.channel.send('Responding is on')
    elif response.lower() == 'false':
      db['responding'] = False
      await message.channel.send('Responding is off')
    else:
      await message.channel.send('Please write either true or false')
    
keep_alive()
client.run(os.getenv('TOKEN'))