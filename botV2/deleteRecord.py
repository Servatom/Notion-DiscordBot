import requests
import json
import os
from utils import *
import discord
from discord.ext import commands
import asyncio

def patch(notion_key, payload, searchObj_toDelete):
    headers = {
        'Authorization': notion_key,
        'Notion-Version': '2021-05-13',
        'Content-Type': 'application/json'
    }
    url = f"https://api.notion.com/v1/pages/{searchObj_toDelete.id}"
    response = requests.request("PATCH", url, headers=headers, data=payload)
    print(response.content)

def deleteWithoutContributor(searchObj_toDelete, api_key):
    payload = json.dumps({
        "properties": {
            "Title": {
                "rich_text": [
                    {
                        "text": {
                            "content": ""
                        }
                    }
                ]
            },
            "Tag": {
                "type": "multi_select",
                "multi_select": [
                    {
                        "name": " "
                    }
                ]
            },
            "URL": {
                "url": None
            }
        }
    })
    patch(api_key, payload, searchObj_toDelete)

def deleteWithoutTag(searchObj_toDelete, api_key):
    payload = json.dumps({
        "properties": {
            "Title": {
                "rich_text": [
                    {
                        "text": {
                            "content": ""
                        }
                    }
                ]
            },
            "Contributor": {
                "type": "title",
                "title": [
                    {
                        "text": {
                            "content": ""
                        }
                    }
                ]
            },
            "URL": {
                "url": None
            }
        }
    })
    patch(api_key, payload, searchObj_toDelete)

def deleteWithoutTagAndContributor(searchObj_toDelete, api_key):
    payload = json.dumps({
        "properties": {
            "Title": {
                "rich_text": [
                    {
                        "text": {
                            "content": ""
                        }
                    }
                ]
            },
            "URL": {
                "url": None
            }
        }
    })
    patch(api_key, payload, searchObj_toDelete)


def deleteAll(searchObj_toDelete, api_key):
    payload = json.dumps({
        "properties": {
            "Title": {
                "rich_text": [
                    {
                        "text": {
                            "content": ""
                        }
                    }
                ]
            },
            "Tag": {
                "type": "multi_select",
                "multi_select": [
                    {
                        "name": " "
                    }
                ]
            },
            "Contributor": {
                "type": "title",
                "title": [
                    {
                        "text": {
                            "content": ""
                        }
                    }
                ]
            },
            "URL": {
                "url": None
            }
        }
    })
    patch(api_key, payload, searchObj_toDelete)

# bot delete by title function
async def delByTitle(ctx, query, client, bot):
    search_results = searchByTitle(query.strip(), client.notion_db_id, client.notion_api_key)
    
    # check if there are results
    print(len(search_results))
    if len(search_results) == 0:
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
        if client.contributor:
            # enabled contributor
            deleteWithoutTag(search_results[option_to_delete-1], client.notion_api_key)
        else:
            # disabled contributor
            deleteWithoutTagAndContributor(search_results[option_to_delete-1], client.notion_api_key)
            
        embed = discord.Embed(title="Successful! Record deleted", description=f"{title} deleted!", color=discord.Color.green())
        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(title="Enter Valid input", description="This option doesn't exist", color=discord.Color.red())
        await ctx.send(embed=embed)

# bot delete by tag function
async def delByTag(ctx, query, client, bot):
    # TODO: rdotjain - add tag deletion
    print("deleted by tag")