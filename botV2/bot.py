import discord
from discord.ext import commands
import os
import json
from database import SessionLocal, engine
import models

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
    # get 
    prefixes = {}
    with open('guilds.json', 'r') as f:
        prefixes = json.loads(f.read())
    print(prefixes)
    print(prefixes[str(message.guild.id)])
    return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix=(get_prefix), help_command=None)

@bot.command(name="getguild")
async def getguild(ctx):
    print(ctx.guild.id)

@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("Hello!")


bot.run(token)
