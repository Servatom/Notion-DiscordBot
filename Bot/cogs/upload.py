import os
import discord
from discord.ext import commands
from functionality.utils import *
from functionality.addRecord import *
import asyncio

try:
    PREFIX = os.environ["PREFIX"]
except:
    PREFIX = "*"


class Upload(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.guild_data = getGuildInfo()

    @commands.command(name="upload", aliases=["u"])
    async def upload(self, ctx, *args):
        # check if guild is in guild_data
        if not checkIfGuildPresent(ctx.guild.id):
            # embed
            embed = discord.Embed(
                description="You are not registered, please run `" + PREFIX + "setup` first",
                title="",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        # get the url of the file uploaded
        url = ""
        try:
            url = ctx.message.attachments[0].url
        except:
            embed = discord.Embed(
                title="",
                description="Please upload a file",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        # ask for title
        embed = discord.Embed(
            title="Enter the title of the file",
            description="",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)
        try:
            msg = await self.bot.wait_for(
                "message",
                check=lambda message: message.author == ctx.author,
                timeout=60,
            )
        except:
            embed = discord.Embed(
                title="Timed out", description="", color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        title = msg.content
        client = self.guild_data[str(ctx.guild.id)]
        # add data
        try:
            if client.tag and client.contributor:
                # addData
                tags = getFileTags(args)
                author = "@" + str(ctx.author).split("#")[0]
                addAllData(
                    url, client.notion_api_key, client.notion_db_id, author, tags, title
                )
            elif client.tag == False and client.contributor == True:
                # addData
                author = "@" + str(ctx.author).split("#")[0]
                addDataWithoutTag(
                    url, client.notion_api_key, client.notion_db_id, title, author
                )
            elif client.tag == True and client.contributor == False:
                # addData
                tags = getFileTags(args)
                addWithoutContributor(
                    url, client.notion_api_key, client.notion_db_id, tags, title
                )
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
            # embed
            embed = discord.Embed(
                title="Error",
                description="Error adding record. Check notion database id and api key provided",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Upload(client))
