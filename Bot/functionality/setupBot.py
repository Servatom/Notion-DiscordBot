import asyncio
import discord
import requests
from database import SessionLocal, engine
import models
from functionality.security import *

db = SessionLocal()

# TODO: Use discord component buttons to make this more user friendly


async def verifyDetails(notion_api_key, notion_db_id, ctx):
    url = "https://api.notion.com/v1/databases/" + notion_db_id
    headers = {
        "Authorization": notion_api_key,
        "Notion-Version": "2021-05-13",
        "Content-Type": "application/json",
    }
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        res = res.json()
        if res["code"] == "unauthorized":
            await ctx.send("Invalid Notion API key")
            return False
        elif res["code"] == "object_not_found":
            await ctx.send("Invalid Notion database id")
            return False
        else:
            print(res)
            return False
    else:
        return True


async def setupConversation(ctx, bot):
    """
    Get all the data from client, verify it and add it to the database
    """

    guild_id = ctx.guild.id
    embed = discord.Embed(description="Enter the notion API key")
    await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for(
            "message",
            check=lambda message: message.author == ctx.author,
            timeout=60,
        )
    except asyncio.TimeoutError:
        embed = discord.Embed(
            title="Timed out",
            description="You took too long to respond",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
    notion_api_key = msg.content.strip()

    embed = discord.Embed(description="Enter the notion database id")
    await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for(
            "message", check=lambda message: message.author == ctx.author, timeout=60
        )
    except asyncio.TimeoutError:
        embed = discord.Embed(
            title="Timed out",
            description="You took too long to respond",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
    notion_db_id = msg.content.strip()

    embed = discord.Embed(description="Do you want to enable tagging? (y/n)")
    await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for(
            "message", check=lambda message: message.author == ctx.author, timeout=60
        )
    except asyncio.TimeoutError:
        embed = discord.Embed(
            title="Timed out",
            description="You took too long to respond",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
    if msg.content.lower().strip() == "y":
        tag = True
    else:
        tag = False

    # Verify the details
    verification = await verifyDetails(notion_api_key, notion_db_id, ctx)
    if verification:
        # If guild already exists, update it
        client = (
            db.query(models.Clients).filter(models.Clients.guild_id == guild_id).first()
        )
        if client:
            client.notion_api_key = encrypt(notion_api_key)
            client.notion_db_id = encrypt(notion_db_id)
            client.tag = tag
            db.commit()
            embed = discord.Embed(
                title="Updated",
                description="The client has been updated",
                color=discord.Color.green(),
            )
            await ctx.send(embed=embed)

            # create obj
            obj = models.Clients(
                guild_id=guild_id,
                notion_api_key=notion_api_key,
                notion_db_id=notion_db_id,
                tag=tag,
            )
            return obj

        # If the details are correct, add them to the database
        new_client = models.Clients(
            guild_id=guild_id,
            notion_api_key=encrypt(notion_api_key),
            notion_db_id=encrypt(notion_db_id),
            tag=tag,
        )

        obj = models.Clients(
            guild_id=guild_id,
            notion_api_key=notion_api_key,
            notion_db_id=notion_db_id,
            tag=tag,
        )
        db.add(new_client)
        db.commit()
        return obj

    return None
