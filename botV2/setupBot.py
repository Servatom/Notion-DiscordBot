import asyncio
import discord

async def setupConversation(ctx, bot):
    guild_id = str(ctx.guild.id)
    embed = discord.Embed(title="Enter the notion API key")
    await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for(
            "message", check=lambda message: message.author == ctx.author, timeout=60
        )
    except asyncio.TimeoutError:
        discord.Embed(
            title="Timed out",
            description="You took too long to respond",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
    notion_api_key = msg.content

    embed = discord.Embed(title="Enter the notion database id")
    await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for(
            "message", check=lambda message: message.author == ctx.author, timeout=60
        )
    except asyncio.TimeoutError:
        discord.Embed(
            title="Timed out",
            description="You took too long to respond",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
    notion_db_id = msg.content

    embed = discord.Embed(title="Do you to enable tagging? (y/n)")
    await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for(
            "message", check=lambda message: message.author == ctx.author, timeout=60
        )
    except asyncio.TimeoutError:
        discord.Embed(
            title="Timed out",
            description="You took too long to respond",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
    if msg.content == "y":
        tag = True
    else:
        tag = False

    embed = discord.Embed(
        title="Do you want to add contributors' names to the database? (y/n)"
    )
    await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for(
            "message", check=lambda message: message.author == ctx.author, timeout=60
        )
    except asyncio.TimeoutError:
        await ctx.send("You have not responded for 30s so quitting!")
        return
    if msg.content == "y":
        contributor = True
    else:
        contributor = False

    embed = discord.Embed(title="Enter a prefix for your bot (default=!)")
    await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for(
            "message", check=lambda message: message.author == ctx.author, timeout=60
        )
    except asyncio.TimeoutError:
        discord.Embed(
            title="Timed out",
            description="You took too long to respond",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
    prefix = msg.content
    # return notion_api_key, notion_db_id, tag, contributor, prefix
    return {"notion_api": notion_api_key, "notion_db": notion_db_id, "tag": tag, "contributor": contributor, "prefix": prefix, "guild_id": guild_id}