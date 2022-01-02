import os
import discord
import asyncio
from discord.ext import commands
from functionality.utils import *
from functionality.search import *

try:
    PREFIX = os.environ["PREFIX"]
except:
    PREFIX = "*"


class Search(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.guild_data = getGuildInfo()

    async def searchByTitleBot(self, ctx, query, client):
        # first get all the data of the database
        search_results = searchByTitle(
            query.strip(), client.notion_db_id, client.notion_api_key
        )

        # check if there are results
        print(len(search_results))
        if len(search_results) == 0:
            # embeded
            embed = discord.Embed(
                title="No results found", description="", color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        count = 1

        embed = discord.Embed(
            title="Search Results",
            description="Results for {}".format(query),
            color=discord.Color.green(),
        )
        for result in search_results:
            # make sure title and url are present
            if result.title.strip() == "" and result.url == None:
                continue
            embed.add_field(
                name=str(count) + ". " + result.title.strip(),
                value=result.url,
                inline=False,
            )
            count += 1
        await ctx.send(embed=embed)

    @commands.command(name="search", aliases=["s"])
    async def search(self, ctx, *args):
        # check if the guild is present
        if not checkIfGuildPresent(ctx.guild.id):
            # embed send
            embed = discord.Embed(
                description="You are not registered, please run `" + PREFIX + "setup` first",
                title="",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        #  Check if tagging is enabled
        if self.guild_data[str(ctx.guild.id)].tag:
            # Call search by tag
            async with ctx.typing():
                await self.searchTag(ctx, *args)
                return
        else:
            # Call search by title
            async with ctx.typing():
                await self.searchTitle(ctx, *args)
                return

    @commands.command(name="searchTitle", aliases=["title"])
    async def searchTitle(self, ctx, *args):
        # check if guild is setup
        if not checkIfGuildPresent(ctx.guild.id):
            # embed send
            embed = discord.Embed(
                description="You are not registered, please run `" + PREFIX + "setup` first",
                title="",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return
        guild_id = ctx.guild.id
        client = self.guild_data[str(guild_id)]
        query = getQueryForTitle(args)

        # check if query is empty
        if query:
            async with ctx.typing():
                await self.searchByTitleBot(ctx, query, client)
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

    @commands.command(name="searchTag", aliases=["tag"])
    async def searchTag(self, ctx, *args):
        notion_db = self.guild_data[str(ctx.guild.id)].notion_db_id
        if len(args) > 0:
            # Check if tag exists
            query = ""

            for tag in args:
                query = query + tag.strip().lower() + ", "
            query = query.rstrip(", ")

            search_results = searchTag(
                notion_db_id=notion_db,
                notion_api_key=self.guild_data[str(ctx.guild.id)].notion_api_key,
                tags=getSearchTagsPayload(args),
            )

            if len(search_results) > 0:
                # Found a result
                embed = discord.Embed(
                    title="Search Results",
                    description="Results for {}".format(query),
                    color=discord.Color.green(),
                )
                count = 1
                for result in search_results:
                    # Add the result to the embed
                    embed.add_field(
                        name=str(count) + ". " + result.title,
                        value=result.url,
                        inline=False,
                    )
                    count += 1
                await ctx.send(embed=embed)
            else:
                # No results
                embed = discord.Embed(
                    title="No Results",
                    description="No results found for {}".format(query),
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)
        else:
            # No tags
            embed = discord.Embed(
                title="No Tags",
                description="Please enter a tag to search for",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Search(client))
