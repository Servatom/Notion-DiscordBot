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
    print("No prefix found, using default: *")
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

    setup_status = await setupConversation(ctx, bot)
    if setup_status:
        embed = discord.Embed(
            description="Setup complete",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Setup failed", description="Setup failed", color=discord.Color.red()
        )
        await ctx.send(embed=embed)


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
            description="You can search by title by typing `"
            + client.prefix
            + "searchTitle <query>`",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)


@bot.command(name="prefix")
async def prefix(ctx):
    """
    Change the prefix of the bot
    """
    prefix = db.query(models.Clients).filter_by(guild_id=ctx.guild.id).first().prefix
    embed = discord.Embed(
        title="Enter the new prefix for your bot",
        description="Current prefix is : " + prefix,
    )
    await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for(
            "message", check=lambda message: message.author == ctx.author, timeout=60
        )
    except asyncio.TimeoutError:
        embed = discord.Embed(
            title="Timed out",
            description="You took too long to respond",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
    new_prefix = msg.content.strip()
    db.query(models.Clients).filter_by(guild_id=ctx.guild.id).update(
        {"prefix": new_prefix}
    )
    try:
        db.commit()
    except Exception as e:
        print(e)
        await ctx.send("Something went wrong, please try again!")
        return
    await ctx.send("Successfully updated prefix!")
    global prefix_data
    prefix_data[str(ctx.guild.id)] = new_prefix


botSetup()
print(guild_data)
print(prefix_data)
bot.run(token)
