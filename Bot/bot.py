import discord
from discord.ext import commands
import os
from addRecord import addData
import validators
from duplicateCheck import doesItExist
from tagGiver import giveTags
prefix = "/"
bot = commands.Bot(command_prefix=prefix)


@bot.command(name="add")
async def add(ctx, *args):
    author = '@' + str(ctx.author).split('#')[0]
    print(args)

    if(len(args) > 0):
        url = args[0]
        if(validators.url(url)):
            #Its a valid link
            if(doesItExist(url) == False):
                #The link doesnt exist in the database
                if(len(args) > 1):             
                    #Add data
                    addData(url, author, giveTags(args))
                else:
                    #Tag not provided
                    addData(url, author)

                #Send confirmation that data was pushed
                embed = discord.Embed(title="Data added", description="New link added by {}".format(author), color=discord.Color.from_rgb(190, 174, 226))
                await ctx.send(embed=embed)

            else:
                #the link was already in the database
                #Preventing duplication of data
                embed = discord.Embed(title="Already Added", description="This link is already in the refrences page", color=discord.Color.red())
                await ctx.send(embed=embed)
        else:
            #Invalid URL provided
            embed = discord.Embed(title="Invalid URL provided",
                                  description="Please check the URL you have provided", color=discord.Color.red())
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="URL not provided", description="Abe kuch to daal de!", color=discord.Color.red())
        await ctx.send(embed=embed)



#Getting discord token and running the bot
try:
    print(os.environ['DISCORD_AUTH'])
    token = str(os.environ['DISCORD_AUTH'])
    bot.run(token)
except:
    print("Invalid token")