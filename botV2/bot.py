import asyncio
import discord
from discord.ext import commands
import os
from database import SessionLocal, engine
import models
from utils import *
from deleteRecord import *
from search import searchByTitleBot
from setupBot import setupConversation
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
    
    # check if we need to allow the user to update the settings if needed
    if str(ctx.guild.id) in guild_data:
        await ctx.send("This guild is already setup")
        return
    
    # continue the conversation for setup and get a dictionary of the data. Data verification must happen in this function itself.
    # Rupanshi's TODO: Verify all these details
    setup_data = await setupConversation(ctx, bot)
    if not setup_data:
        # nothing was returned the data wasnt given properly
        embed = discord.Embed(title="Error", description="The data you provided was not correct. Please try again.", color=0xFF0000)
        await ctx.send(embed=embed)
        return
    
    print(setup_data)
    
    # check if guild id already in database
    # add to database
    new_client = models.Clients(
        guild_id=setup_data["guild_id"],
        notion_api_key=setup_data["notion_api"],
        notion_db_id=setup_data["notion_db"],
        tag=setup_data["tag"],
        prefix=setup_data["prefix"],
        contributor=setup_data["contributor"],
    )
    db.add(new_client)
    db.commit()

    # add to guild_data
    guild_data[setup_data["guild_id"]] = new_client
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
            description="You can search by title by typing `" + client.prefix + "searchTitle <query>`",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)

botSetup()
print(guild_data)
print(prefix_data)
bot.run(token)
