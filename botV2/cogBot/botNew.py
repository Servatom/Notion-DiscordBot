import discord
from discord.ext import commands
import os
from database import SessionLocal, engine
import models
import json

db = SessionLocal()
models.Base.metadata.create_all(bind=engine)

prefix = ""
prefix_data = {}

try:
    prefix = os.environ["PREFIX"]
except:
    prefix = "%"

try:
    token = os.environ["TOKEN"]
except:
    print("No token found, exiting...")
    exit()

prefix_data = {}

def fillPrefix():
    global prefix_data
    prefix_data = {}
    guilds = db.query(models.Clients).all()
    for guild in guilds:
        prefix_data[str(guild.guild_id)] = guild.prefix

def generateJson():
    # get objects from the database
    guilds = db.query(models.Clients).all()
    # create a dictionary to store the data
    data = {}
    # loop through the guilds
    for guild in guilds:
        data[str(guild.guild_id)] = guild.serialize
    # write the data to a json file
    with open('guild_data.json', 'w') as outfile:
        json.dump(data, outfile)

def get_prefix(client, message):
    global prefix_data
    try:
        prefix = prefix_data[str(message.guild.id)]
    except:
        prefix = "*"
    return prefix

generateJson() 
fillPrefix()

cogs = [
    'cogs.delete',
    'cogs.search',
    'cogs.add'
]

bot = commands.Bot(command_prefix=(get_prefix), help_command=None)

def reload_cogs():
    for cog in cogs:
        bot.reload_extension(cog)

def load_cogs():
    for cog in cogs:
        bot.load_extension(cog)

# TODO: Rupanshi add prefix modification command here and then remember to call reload_cogs function 

# loading all the cogs
load_cogs()
bot.run(token)
