import discord
from discord.ext import commands
from functionality.utils import *
import os

try:
    PREFIX = os.environ["PREFIX"]
except:
    PREFIX = "*"

class Help(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.guild_data = self.bot.guild_info

    @commands.command(name="help", aliases=["h"])
    async def help(self, ctx, *args):
        """Give commands list"""
        # check if guild is present
        if not checkIfGuildPresent(ctx.guild.id):
            # embed send
            embed = discord.Embed(
                description="You are not registered, please run `" + PREFIX + "setup` first",
                title="",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return
        
        guild = self.guild_data[str(ctx.guild.id)]
        prefix = guild.prefix
        commands = {}
        if guild.tag:
            # check if the guild has tags enabled
            commands = {f"```{prefix}add <URL> <Tag 1> <Tag2>...<TagN>```": "Add URL to database with the tags (1,2...N)",
                        f"```{prefix}search <Tag 1> <Tag2>...<TagN>```": "List of records with Tag1, Tag2...Tag N",
                        f"```{prefix}searchTitle <Title>```": "List of records with the title",
                        f"```{prefix}delete <Tag1> <Tag2>....<TagN>```": "To delete record having tag 1,2...N. Will give list of records. Type in the serial number of the record you want to delete",
                        f"```{prefix}deleteTitle <Title>```": "To delete record having the title. Will give list of records. Type in the serial number of the record you want to delete",
                        f"```{prefix}upload <Tag 1> <Tag2>...<TagN>```": "Drag and drop the file and use this command in the comment section. It will upload it on the notion database with Tag 1,2.....N.",
                        f"```{prefix}prefix```": "Change the prefix of the bot"}
        else:
            # no tags enabled
            commands = {f"```{prefix}add <URL>```": "Add URL to database",
                        f"```{prefix}search <Title>```": "List of records with Title",
                        f"```{prefix}delete <Title>```": "To delete record having title. Will give list of records. Type in the serial number of the record you want to delete",
                        f"```{prefix}upload```": "Drag and drop the file and use this command in the comment section. It will upload it on the notion database with Title",
                        f"```{prefix}prefix```": "Change the prefix of the bot"}


        embed = discord.Embed(title="List of commands:", description="These are the commands to use with this bot", color=discord.Color.green())
        count = 1
        for command in commands:
                embed.add_field(name=str(count)+". "+ command, value=commands[command], inline=False)
                count += 1
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))