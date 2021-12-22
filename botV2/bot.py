import asyncio
import discord
from discord.ext import commands
import os
from database import SessionLocal, engine
import models
from utils import *
from deleteRecord import *
from search import searchByTitleBot
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
    prefix = "*"
# get token
try:
    token = str(os.environ["TOKEN"])
except:
    print("No token found, exiting...")
    exit()


def get_prefix(client, message):
    global prefix_data
    try:
        prefix = prefix_data[str(message.guild.id)]
    except:
        prefix = "*"
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
    global guild_data
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

    # Add the object to the guild_data
    guild_data[str(guild_id)] = new_client
    await ctx.send("Added to database")

@bot.command("delete")
async def delete(ctx, *args):
    if not checkIfGuildPresent(ctx.guild.id):
        await ctx.send("You are not registered, please run `!setup` first")
        return

    # TODO: raghavTinker paginate the search results
    # check if the guild has tags enabled
    # get guild id
    guild_id = ctx.guild.id
    # get guild info 
    client = guild_data[str(guild_id)]
    
    query = getQueryForTitle(args)
    
    if query:
        if not client.tag:
            # no tags enabled so search by title
            # get the title of the message
            await delByTitle(ctx, query, client, bot)
        else:
            # delete by tag
            await delByTag(ctx, query, client, bot)
    else:
        # embed
        embed = discord.Embed(
            title="No query found",
            description="Please enter a valid query",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)

@bot.command("searchTitle")
async def searchTitle(ctx, *args):
    if not checkIfGuildPresent(ctx.guild.id):
        await ctx.send("You are not registered, please run `!setup` first")
        return
    guild_id = ctx.guild.id
    client = guild_data[str(guild_id)]
    query = getQueryForTitle(args)
    if query:
        await searchByTitleBot(ctx, query, client, bot)
    else:
        # embed send
        embed = discord.Embed(
            title="Please enter a valid query",
            description="You can search by title by typing `!searchTitle <query>`",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)

botSetup()
print(guild_data)
print(prefix_data)
bot.run(token)
