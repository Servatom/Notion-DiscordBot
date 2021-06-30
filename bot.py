import discord
from discord.ext import commands,tasks
import asyncio
import os
from addRecord import addData
prefix = "/"
bot = commands.Bot(command_prefix = prefix)

@bot.command(name="add")
async def add(ctx, *args):
    author = '@' + str(ctx.author).split('#')[0]
    print(args)
    url = args[0]
    if(len(args) > 1):
        tag = args[1]
        addData(url, author, tag)
    else:
        addData(url, author)

    embed = discord.Embed(title="Data added", description="New link added by {}".format(author), color=discord.Color.from_rgb(190, 174, 226))
    await ctx.send(embed=embed)


try:
    print(os.environ['DISCORD_AUTH'])
    token = str(os.environ['DISCORD_AUTH'])
    bot.run(token)
except:
    print("Invalid token")