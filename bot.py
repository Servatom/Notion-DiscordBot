import discord
from discord.ext import commands,tasks
import asyncio
import os
from addRecord import addData
import validators

prefix = "/"
bot = commands.Bot(command_prefix = prefix)

@bot.command(name="add")
async def add(ctx, *args):
    author = '@' + str(ctx.author).split('#')[0]
    print(args)
    
    if(len(args) > 0):
        url = args[0]
        if(validators.url(url)):
            if(len(args) > 1):
                tag = args[1]
                addData(url, author, tag)
            else:
                addData(url, author)

            embed = discord.Embed(title="Data added", description="New link added by {}".format(author), color=discord.Color.from_rgb(190, 174, 226))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Invalid URL provided", description="Please check the URL you have provided", color=discord.Color.red())
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="URL not provided", description="Abe kuch to daal de!", color=discord.Color.red())
        await ctx.send(embed=embed)


try:
    print(os.environ['DISCORD_AUTH'])
    token = str(os.environ['DISCORD_AUTH'])
    bot.run(token)
except:
    print("Invalid token")