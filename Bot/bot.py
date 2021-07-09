import discord
from discord.ext import commands
import os
from addRecord import addData, addPDF, addGenericFile
import validators
from duplicateCheck import doesItExist, amIThere
from tagGiver import giveTags, getSearchTags, giveTagsFileUpload
from search import SearchObject, searchTag
from delete import deleteMe
from uploadFiles import downloadFile
from getTitle import giveTitle
import asyncio

prefix = ""
try:
    print(os.environ['PREFIX'])
    prefix = str(os.environ['PREFIX'])
except:
    prefix = '!'

bot = commands.Bot(command_prefix=prefix, help_command=None)
bot.remove_command('help')

@bot.command(name="add")
async def add(ctx, *args):
    async with ctx.typing():
        author = '@' + str(ctx.author).split('#')[0]
        print(args)

        if(len(args) > 0):
            url = args[0]
            if(validators.url(url)):
                embed = discord.Embed(title="Adding Data...", description="Please Wait while I upload the data", color=discord.Color.green())
                await ctx.send(embed=embed)
                #Its a valid link
                if((doesItExist(url) == False) and (amIThere(url) == False)):
                    # amIThere checks if its on Gdrive and doesItexist on notion db
                    #The link doesnt exist in the database
                    if(len(args) > 1):             
                        #Add data
                        if(".pdf" in url):
                            gDrive_link = downloadFile(url)
                            addPDF(gDrive_link, author, giveTitle(url), giveTags(args))
                        else:
                            addData(url, author, giveTags(args))
                    else:
                        #Tag not provided
                        if(".pdf" in url):
                            gDrive_link = downloadFile(url)
                            addPDF(gDrive_link,author, giveTitle(url))
                        else:
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


@bot.command(name="search")
async def search(ctx, *args):
    """Returns all entries containing the tag specified"""
    if (len(args) > 0):
        #Check if the tag exists
        query = ""

        for tag in args:
            query = query + tag.strip().lower() + ", "
        query = query.rstrip(", ")

        search_results = searchTag(getSearchTags(args))

        if (len(search_results) > 0):
            #Found a result
            embed = discord.Embed(title="Search Results", description="Results for {}".format(query), color=discord.Color.green())
            count = 1
            for result in search_results:
                #Add the result to the embed
                embed.add_field(name=str(count)+". "+ result.title, value=result.url, inline=False)
                count += 1
            await ctx.send(embed=embed)
        else:
            #No results
            embed = discord.Embed(title="No Results", description="No results found for {}".format(query), color=discord.Color.red())
            await ctx.send(embed=embed)

    else:
        #No tag provided
        embed = discord.Embed(title="Invalid Search", description="Kuch to daal de!", color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.command(name="delete")
async def delete(ctx, *args):
    if (len(args) > 0):
        #Check if the tag exists
        query = ""

        for tag in args:
            query = query + tag.strip().lower() + ", "
        query = query.rstrip(", ")

        search_results = searchTag(getSearchTags(args))

        if (len(search_results) > 0):
            #Found a result
            embed = discord.Embed(title="Type in the serial number you want to delete", description="Results for {}".format(query), color=discord.Color.green())
            count = 1
            for result in search_results:
                #Add the result to the embed
                embed.add_field(name=str(count)+". "+ result.title, value=result.url, inline=False)
                count += 1
            await ctx.send(embed=embed)

            def check(reply_user):
                return reply_user.author == ctx.author and reply_user.channel == ctx.channel
            
            # Timeout error
            try:
                reply = await bot.wait_for("message", check=check, timeout=30)
            except asyncio.TimeoutError:
                embed = discord.Embed(title="No response", description=f"Waited for 30s no response received", color=discord.Color.red())
                await ctx.send("You have not responded for 30s so quitting!")
                return
            
            # Check if the input is valid
            try:
                option_to_delete = int(reply.content)
                title = search_results[option_to_delete-1].title
                print(title)
                deleteMe(search_results[option_to_delete-1].id)
                embed = discord.Embed(title="Successful! Record deleted", description=f"{title} deleted!", color=discord.Color.green())
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(title="Enter Valid input", description="This option doesn't exist", color=discord.Color.red())
                await ctx.send(embed=embed)

            
        else:
            #No results
            embed = discord.Embed(title="No Results", description="No results found for {}".format(query), color=discord.Color.red())
            await ctx.send(embed=embed)
    else:
        #No tag provided
        embed = discord.Embed(title="Invalid Search", description="Kuch to daal de!", color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.command(name="upload")
async def upload(ctx, *args):
    async with ctx.typing():
        author = '@' + str(ctx.author).split('#')[0]
        try:
            url = ctx.message.attachments[0].url
        except:
            embed = discord.Embed(title="Please upload a file", description="Kuch to daal de!", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(title="Provide Title", description="Please give us the title of the resource you are uploading", color=discord.Color.green())
        await ctx.send(embed=embed)

        def check(reply_user):
            return reply_user.author == ctx.author and reply_user.channel == ctx.channel
        
        try:
            reply = await bot.wait_for("message", check=check, timeout=30)
        except asyncio.TimeoutError:
            embed = discord.Embed(title="No response", description=f"Waited for 30s no response received", color=discord.Color.red())
            await ctx.send("You have not responded for 30s so quitting!")
            return
        
        title = reply.content
        print(title)
        if(len(args) > 0):
            addPDF(downloadFile(url),author, title, giveTagsFileUpload(args,url))
        else:
            if(".pdf" in url):
                addPDF(downloadFile(url),author, title)
            else:
                addGenericFile(downloadFile(url),author, title)
        
    embed = discord.Embed(title="Data added", description="New link added by {}".format(author), color=discord.Color.from_rgb(190, 174, 226))
    await ctx.send(embed=embed)
    

@bot.command()
async def help(ctx):
    """Give commands list"""
    commands = {f"```{prefix}add <URL> <Tag 1> <Tag2>...<TagN>```": "Add URL to database with the tags (1,2...N)",
                f"```{prefix}search <Tag 1> <Tag2>...<TagN>```": "List of records with Tag1, Tag2...Tag N",
                f"```{prefix}delete <Tag1> <Tag2>....<TagN>```": "To delete record having tag 1,2...N. Will give list of records. Type in the serial number of the record you want to delete"}
    
    embed = discord.Embed(title="List of commands:", description="These are the commands to use with this bot", color=discord.Color.green())
    count = 1
    for command in commands:
          embed.add_field(name=str(count)+". "+ command, value=commands[command], inline=False)
          count += 1
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{prefix}help"))

#Getting discord token and running the bot
try:
    print(os.environ['DISCORD_AUTH'])
    token = str(os.environ['DISCORD_AUTH'])
    bot.run(token)
except:
    print("Invalid token")