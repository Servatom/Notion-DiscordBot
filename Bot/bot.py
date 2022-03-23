import asyncio
import discord
from discord.ext import commands
from functionality import setupBot, utils
import os
from database import SessionLocal, engine
import models
import json
import functionality.utils as utils
import functionality.security as security
# database setup
db = SessionLocal()
# prefix data
prefix = ""
prefix_data = {}

# cogs
cogs = ["cogs.delete", "cogs.search", "cogs.add", "cogs.upload", "cogs.help"]

try:
    prefix = os.environ["PREFIX"]
except:
    prefix = "*"

try:
    token = os.environ["TOKEN"]
except:
    print("No token found, exiting...")
    exit()

# get prefixes from the database
def fillPrefix():
    global prefix_data
    prefix_data = {}
    guilds = db.query(models.Clients).all()
    for guild in guilds:
        prefix_data[str(guild.guild_id)] = guild.prefix


# cog loading reloading
def reload_cogs():
    for cog in cogs:
        bot.reload_extension(cog)


def load_cogs():
    for cog in cogs:
        bot.load_extension(cog)


# get prefix of the guild that triggered bot
def get_prefix(client, message):
    global prefix_data
    try:
        prefix = prefix_data[str(message.guild.id)]
    except:
        prefix = "*"
    return prefix

fillPrefix()

bot = commands.Bot(command_prefix=(get_prefix), help_command=None)

# setup command
@bot.command(name="setup")
async def setup(ctx):
    global prefix_data

    setup_data = await setupBot.setupConversation(ctx, bot)
    if setup_data is not None:
        guild_id = setup_data.guild_id
        prefix = setup_data.prefix

        # update prefix_data
        prefix_data[str(guild_id)] = prefix

        # update guild_info
        bot.guild_info[str(guild_id)] = setup_data

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


@bot.command(name="prefix")
async def changePrefix(ctx):
    """
    Change the prefix of the bot
    """
    global prefix
    if not utils.checkIfGuildPresent(ctx.guild.id):
            embed = discord.Embed(
                description="You are not registered, please run `" + prefix + "setup` first",
                title="",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return
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
    embed = discord.Embed(
        title="Successfully updated prefix",
        description="Prefix changed to " + new_prefix,
        color=discord.Color.green(),
    )
    await ctx.send(embed=embed)

    # Update prefix_data and reload cogs
    global prefix_data
    prefix_data[str(ctx.guild.id)] = new_prefix
    
    # update guild_info
    bot.guild_info[str(ctx.guild.id)].prefix = new_prefix

# storing guild info in an attribute of bot so that all cogs can access
bot.guild_info = utils.getGuildInfo()
# loading all the cogs
load_cogs()
try:
    bot.run(token)
except Exception as e:
    print("No token...exiting!")
