import discord
from discord.ext import commands
import os
from addRecord import addData
import validators
from duplicateCheck import doesItExist
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
                    #Tag provided
                    final_tag = []
                    list_of_tags = []
                    #Multiple
                    for tag in args[1:]:
                        list_of_tags.append(tag)
                    for tag in list_of_tags:
                        tag_list = tag.split(",")
                        for single_tag in tag_list:
                            if(single_tag.strip() == ""):
                                continue
                            final_tag.append({"name": single_tag.strip(), "color": "default"})
                    if(".pdf" in url):
                        final_tag.append({"name": "PDF", "color": "default"})

                    print(final_tag)               
                    #Add data
                    addData(url, author, final_tag)
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


try:
    print(os.environ['DISCORD_AUTH'])
    token = str(os.environ['DISCORD_AUTH'])
    bot.run(token)
except:
    print("Invalid token")
