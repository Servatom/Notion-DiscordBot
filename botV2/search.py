from fuzzywuzzy import fuzz
import json
import requests
from bs4 import BeautifulSoup
from utils import *
import discord
from discord.ext import commands
import asyncio

def getAllTitles(notion_db, notion_api):
    url = "https://api.notion.com/v1/databases/" + notion_db + "/query"
    headers = {
        'Authorization': notion_api,
        'Content-Type': 'application/json',
        'Notion-Version': '2021-08-16'
    }

    payload = {
    "filter":{
        "property": "Title",
        "text": {
            "contains": ""
        }
    }
    }   
    payload = json.dumps(payload)
    response = requests.post(url, headers=headers, data=payload)
    data = json.loads(response.text)
    objects = {}
    for row in data['results']:
        try:
            title = row["properties"]["Title"]["rich_text"][0]["text"]["content"]
            obj = SearchData(row["id"], title, row["properties"]["URL"]["url"])
            objects[title] = obj
        except:
            pass
    return objects


def searchByTitle(search, notion_db, notion_api):
    print(search)
    # first get all the data of the database
    titles = getAllTitles(notion_db, notion_api)
    weights = {}

    for title in titles:
        title_list = title.lower().split(" ")
        search_list = search.lower().split(" ")
        for word in search_list:
            if word in title_list:
                if titles[title] not in weights:
                    # fuzzy ratio
                    # replacing - / from title and replacing it with a space
                    
                    weights[titles[title]] = fuzz.partial_ratio(search.lower(), title.lower().replace("-", " ").replace("/", " "))
                else:
                    break
    # return objects in descending order in list
    return sorted(weights, key=weights.get, reverse=True)


async def searchByTitleBot(ctx, query, client, bot):
    # first get all the data of the database
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