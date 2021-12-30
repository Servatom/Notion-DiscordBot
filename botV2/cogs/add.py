import discord
from discord.ext import commands
from functionality.utils import *
from functionality.addRecord import *
import asyncio

class Add(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.guild_data = getGuildInfo()

    @commands.command(name='add', aliases=['a'])
    async def add(self, ctx, *args):
        if not checkIfGuildPresent(ctx.guild.id):
            await ctx.send("You are not registered, please run `!setup` first")
            return
        # check if the guild has tags enabled
        # get guild id
        guild_id = ctx.guild.id
        # get guild info 
        client = self.guild_data[str(guild_id)]

        # check if args are empty
        if len(args) == 0:
            # embed send
            embed = discord.Embed(
                title="Please enter a valid query",
                description="You can search by title by typing `"
                + client.prefix
                + "add <url>`",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return
        
        # get url 
        url = args[0]
        # check if url is valid
        if checkURL(url):
            # get title
            title = getTitle(url)
            # check if title is valid
            if title:
                # valid title received
                # check if record already exists
                if doesItExist(url, client.notion_api_key, client.notion_db_id):
                    print("here")
                    # record already exists
                    # embed send
                    embed = discord.Embed(
                        title="Record already exists",
                        description="",
                        color=discord.Color.red(),
                    )
                    await ctx.send(embed=embed)
                    return
                # check if user has tag and contributor role
            else:
                # title not able to extract
                if doesItExist(url, client.notion_api_key, client.notion_db_id):
                    # record already exists
                    # embed send
                    embed = discord.Embed(
                        title="Record already exists",
                        description="",
                        color=discord.Color.red(),
                    )
                    await ctx.send(embed=embed)
                    return
                # ask for title from user
                # start conversation
                await ctx.send("Please enter a valid title")
                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel
                try:
                    msg = await self.bot.wait_for('message', check=check, timeout=60)
                except asyncio.TimeoutError:
                    await ctx.send("Timed out")
                    return
                # check if title is valid
                if msg.content:
                    # valid title received
                    title = msg.content
                else:
                    # invalid title
                    await ctx.send("Invalid title")
                    return

            # add data
            try:
                if client.tag and client.contributor:
                    # addData
                    tags = getTags(args)
                    author = '@' + str(ctx.author).split('#')[0]
                    addAllData(url, client.notion_api_key, client.notion_db_id, author, tags, title)
                elif client.tag == False and client.contributor == True:
                    # addData
                    author = '@' + str(ctx.author).split('#')[0]
                    addDataWithoutTag(url, client.notion_api_key, client.notion_db_id, title, author)
                elif client.tag == True and client.contributor == False:
                    # addData
                    tags = getTags(args)
                    addWithoutContributor(url, client.notion_api_key, client.notion_db_id, tags, title)
                    # send success message
                # embed
                embed = discord.Embed(
                    title="Success",
                    description="Record added successfully",
                    color=discord.Color.green(),
                )
                await ctx.send(embed=embed)
            except Exception as e:
                print(e)
                #embed
                embed = discord.Embed(
                    title="Error",
                    description="Error adding record. Check notion database id and api key provided",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Add(client))