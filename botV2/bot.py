import asyncio
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


# guild data
guild_data = {}

# guild prefix_data
prefix_data = {}


try:
    prefix = str(os.environ["PREFIX"])
except:
    print("No prefix found, using default: !")
    prefix = "$"
# get token
try:
    token = str(os.environ["TOKEN"])
except:
    print("No token found, exiting...")
    exit()


def get_prefix(client, message):
    global prefix_data
    prefix = ""
    try:
        prefix = prefix_data[str(message.guild.id)]
    except:
        prefix = "!"
    return prefix

def botSetup():
    # get guild data
    global guild_data
    guild_data = getGuildData()

    # get prefix data
    global prefix_data
    prefix_data = getPrefixes()


bot = commands.Bot(command_prefix=(get_prefix), help_command=None)


@bot.command(name="setup")
async def setup(ctx):
    guild_id = ctx.guild.id
    embed = discord.Embed(title="Enter the notion API key")
    await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for(
            "message", check=lambda message: message.author == ctx.author, timeout=60
        )
    except asyncio.TimeoutError:
        discord.Embed(
            title="Timed out",
            description="You took too long to respond",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
    notion_api_key = msg.content

    embed = discord.Embed(title="Enter the notion database id")
    await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for(
            "message", check=lambda message: message.author == ctx.author, timeout=60
        )
    except asyncio.TimeoutError:
        discord.Embed(
            title="Timed out",
            description="You took too long to respond",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
    notion_db_id = msg.content

    embed = discord.Embed(title="Do you to enable tagging? (y/n)")
    await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for(
            "message", check=lambda message: message.author == ctx.author, timeout=60
        )
    except asyncio.TimeoutError:
        discord.Embed(
            title="Timed out",
            description="You took too long to respond",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
    if msg.content == "y":
        tag = True
    else:
        tag = False

    embed = discord.Embed(
        title="Do you want to add contributors' names to the database? (y/n)"
    )
    await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for(
            "message", check=lambda message: message.author == ctx.author, timeout=60
        )
    except asyncio.TimeoutError:
        await ctx.send("You have not responded for 30s so quitting!")
        return
    if msg.content == "y":
        contributor = True
    else:
        contributor = False

    embed = discord.Embed(title="Enter a prefix for your bot (default=!)")
    await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for(
            "message", check=lambda message: message.author == ctx.author, timeout=60
        )
    except asyncio.TimeoutError:
        discord.Embed(
            title="Timed out",
            description="You took too long to respond",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
    prefix = msg.content

    # Rupanshi's TODO: Verify all these details

    # add to database
    new_client = models.Clients(
        guild_id=guild_id,
        notion_api_key=notion_api_key,
        notion_db_id=notion_db_id,
        tag=tag,
        prefix=prefix,
        contributor=contributor,
    )
    db.add(new_client)
    db.commit()
    await ctx.send("Added to database")


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
    db.add(
        models.Clients(guild_id, notion_api_key, notion_db_id, tag, prefix, contributor)
    )
    db.commit()
    await ctx.send("Added record to database.")

botSetup()
bot.run(token)
