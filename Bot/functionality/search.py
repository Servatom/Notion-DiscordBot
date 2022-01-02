from fuzzywuzzy import fuzz
import json
import requests
from bs4 import BeautifulSoup
from functionality.utils import *

def getTitles(headers, payload, url):
    # send payload to get results
    payload = json.dumps(payload)
    response = requests.post(url, headers=headers, data=payload)
    data = json.loads(response.text)
    return data

def getAllTitles(notion_db, notion_api):
    # manage payload and see across all pages
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
    data = getTitles(headers, payload, url)
    objects = {}
    for row in data['results']:
        try:
            title = row["properties"]["Title"]["rich_text"][0]["text"]["content"]
            obj = SearchData(row["id"], title, row["properties"]["URL"]["url"])
            objects[title] = obj
        except:
            pass
    while data["next_cursor"]:
        # means there is another page
        payload = {
            "filter":{
                "property": "Title",
                "text": {
                    "contains": ""
                }
            },
            "start_cursor": data["next_cursor"]
        }
        data = getTitles(headers, payload, url)
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