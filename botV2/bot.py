import discord
from discord.ext import commands
import os
import json
from database import SessionLocal, engine
import models
from utils import *

db = SessionLocal()
models.Base.metadata.create_all(bind=engine)

prefix = ""
token = ""

try:
    prefix = str(os.environ['PREFIX'])
except:
    print("No prefix found, using default: !")
    prefix = "$"
# get token
try:
    token = str(os.environ['TOKEN'])
except:
    print("No token found, exiting...")
    exit()


def get_prefix(client, message):
    prefixes = getPrefixes()
    prefix = ""
    try:
        prefix = prefixes[str(message.guild.id)]
    except:
        prefix = "!"
    return prefix

#bot = commands.Bot(command_prefix="!", help_command=None)
bot = commands.Bot(command_prefix=(get_prefix), help_command=None)

@bot.command(name="getguild")
async def getguild(ctx):
    print(ctx.guild.id)

@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command(name="fill")
async def fill(ctx):
    # fill database with guild
    # get guild id
    guild_id = ctx.guild.id
    # get notion api key
    notion_api_key = "lol"
    # get notion db id
    notion_db_id = "lol"
    # get tag
    tag = True
    # get prefix
    prefix = "!"
    contributor = True
    # add record to database
    db.add(models.Clients(guild_id, notion_api_key, notion_db_id, tag, prefix, contributor))
    db.commit()
    await ctx.send("Added record to database.")

bot.run(token)
