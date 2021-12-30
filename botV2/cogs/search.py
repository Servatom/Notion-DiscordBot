import discord
import asyncio
from discord.ext import commands
from functionality.utils import *
from functionality.search import *


class Search(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.guild_data = getGuildInfo()

    async def searchByTitleBot(self, ctx, query, client):
        # first get all the data of the database
        async with ctx.typing():
            search_results = searchByTitle(query.strip(), client.notion_db_id, client.notion_api_key)

            # check if there are results
            print(len(search_results))
            if len(search_results) == 0:
                # embeded
                embed = discord.Embed(title="No results found", description="", color=discord.Color.red())
                await ctx.send(embed=embed)
                return

            count = 1    

            embed = discord.Embed(title="Search Results", description="Results for {}".format(query), color=discord.Color.green())
            for result in search_results:
                # make sure title and url are present
                if result.title.strip() == "" and result.url == None:
                    continue
                embed.add_field(name=str(count)+". "+ result.title.strip(), value=result.url, inline=False)
                count += 1
        await ctx.send(embed=embed)

    @commands.command(name='searchTitle', aliases=['title'])
    async def searchTitle(self, ctx, *args):
        # check if guild is setup
        if not checkIfGuildPresent(ctx.guild.id):
            await ctx.send("You are not registered, please run `!setup` first")
            return
        guild_id = ctx.guild.id
        client = self.guild_data[str(guild_id)]
        query = getQueryForTitle(args)

        # check if query is empty
        if query:
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

def setup(client):
    client.add_cog(Search(client))