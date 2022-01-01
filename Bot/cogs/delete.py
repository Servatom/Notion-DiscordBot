import discord
from discord.ext import commands
from functionality.utils import *
from functionality.search import *
import asyncio
from functionality.deleteRecord import *

# bot delete by title function
async def delByTitle(ctx, query, client, bot):
    search_results = searchByTitle(query.strip(), client.notion_db_id, client.notion_api_key)
    
    # check if there are results
    print(len(search_results))
    if len(search_results) == 0:
        # embed
        embed = discord.Embed(
            title="No results found", description="", color=discord.Color.red()
        )

        await ctx.send("No results found")
        return
    count = 1    
    
    embed = discord.Embed(title="Type in the serial number you want to delete", description="Results for {}".format(query), color=discord.Color.green())
    for result in search_results:
        # make sure title and url are present
        if result.title.strip() == "" and result.url == None:
            continue
        embed.add_field(name=str(count)+". "+ result.title.strip(), value=result.url, inline=False)
        count += 1
    await ctx.send(embed=embed)

    # get users response for index
    def check(reply_user):
        return reply_user.author == ctx.author and reply_user.channel == ctx.channel
    # timeout error
    try:
        msg = await bot.wait_for("message", check=check, timeout=60)
    except asyncio.TimeoutError:
        embed = discord.Embed(title="No response", description=f"Waited for 60s no response received", color=discord.Color.red())
        await ctx.send("You have not responded for 60s so quitting!")
        return
    # Check if the input is valid
    try:
        option_to_delete = int(msg.content)
        title = search_results[option_to_delete-1].title
        
        # check if contribuor turned on 
        if client.contributor and not client.tag:
            # enabled contributor
            deleteWithoutTag(search_results[option_to_delete-1], client.notion_api_key)
            #await ctx.send("Deleted without tag")
        elif client.tag and client.contributor:
            deleteAll(search_results[option_to_delete-1], client.notion_api_key)
            #await ctx.send("Deleted all")
        elif not client.contributor and client.tag:
            deleteWithoutContributor(search_results[option_to_delete-1], client.notion_api_key)
            #await ctx.send("Deleted with tag")
        else:
            # disabled contributor
            deleteWithoutTagAndContributor(search_results[option_to_delete-1], client.notion_api_key)
            #await ctx.send("Deleted without tag and contributor")

        embed = discord.Embed(title="Successful! Record deleted", description=f"{title} deleted!", color=discord.Color.green())
        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(title="Enter Valid input", description="This option doesn't exist", color=discord.Color.red())
        await ctx.send(embed=embed)

async def delByTag(ctx, query, client, bot, args):
    # TODO: Raghav Sharma...after searchTag func made use that function to delete stuff by tag
    
    search_results = searchTag(
        notion_db_id=client.notion_db_id,
        notion_api_key=client.notion_api_key,
        tags=getSearchTagsPayload(args),
    )

    if len(search_results) == 0:
        # embed
        embed = discord.Embed(
            title="No results found", description="", color=discord.Color.red()
        )
        
        await ctx.send("No results found")
        return
    
    count = 1    
    
    embed = discord.Embed(title="Type in the serial number you want to delete", description="Results for {}".format(query), color=discord.Color.green())
    for result in search_results:
        # make sure title and url are present
        if result.title.strip() == "" and result.url == None:
            continue
        embed.add_field(name=str(count)+". "+ result.title.strip(), value=result.url, inline=False)
        count += 1
    await ctx.send(embed=embed)

    # get users response for index
    def check(reply_user):
        return reply_user.author == ctx.author and reply_user.channel == ctx.channel
    # timeout error
    try:
        msg = await bot.wait_for("message", check=check, timeout=60)
    except asyncio.TimeoutError:
        embed = discord.Embed(title="No response", description=f"Waited for 60s no response received", color=discord.Color.red())
        await ctx.send("You have not responded for 60s so quitting!")
        return
    # Check if the input is valid
    try:
        option_to_delete = int(msg.content)
        title = search_results[option_to_delete-1].title

        # since tags are enabled delete with or without contributor
        if client.contributor:
            # tag and contribuor both enabled
            deleteAll(search_results[option_to_delete-1], client.notion_api_key)
        else:
            # tag enabled only
            deleteWithoutContributor(search_results[option_to_delete-1], client.notion_api_key)
        embed = discord.Embed(title="Successful! Record deleted", description=f"{title} deleted!", color=discord.Color.green())
        await ctx.send(embed=embed)

    except:
        embed = discord.Embed(title="Enter Valid input", description="This option doesn't exist", color=discord.Color.red())
        await ctx.send(embed=embed)
class Delete(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.guild_data = getGuildInfo()
        print("reload")
    
    @commands.command(name='delete', aliases=['del'])
    async def delete(self, ctx, *args):
        if not checkIfGuildPresent(ctx.guild.id):
            await ctx.send("You are not registered, please run `!setup` first")
            return

        # TODO: raghavTinker paginate the search results
    
        # check if the guild has tags enabled
        # get guild id
        guild_id = ctx.guild.id
        # get guild info 
        client = self.guild_data[str(guild_id)]
    
        query = getQueryForTitle(args)
    
        if query:
            if not client.tag:
                # no tags enabled so search by title
                # get the title of the message
                await delByTitle(ctx, query, client, self.bot)
            else:
                # delete by tag
                await delByTag(ctx, query, client, self.bot, args)
        else:
            # embed
            embed = discord.Embed(
                title="No query found",
                description="Please enter a valid query",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
    @commands.command(name="deleteTitle", aliases=['delTitle'])
    async def deleteTitle(self, ctx, *args):
        if not checkIfGuildPresent(ctx.guild.id):
            await ctx.send("You are not registered, please run `!setup` first")
            return

        # TODO: raghavTinker paginate the search results
    
        # check if the guild has tags enabled
        # get guild id
        guild_id = ctx.guild.id
        # get guild info 
        client = self.guild_data[str(guild_id)]

        if len(args) == 0:
            # embed
            embed = discord.Embed(
                title="No query found",
                description="Please enter a valid query",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return
        query = getQueryForTitle(args)
        with ctx.channel.typing():
            await delByTitle(ctx, query, client, self.bot)
        
        
    
def setup(client):
    client.add_cog(Delete(client))