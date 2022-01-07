import requests
import json
from functionality.utils import *
from functionality.search import *

def patch(notion_key, payload, searchObj_toDelete):
    headers = {
        'Authorization': notion_key,
        'Notion-Version': '2021-05-13',
        'Content-Type': 'application/json'
    }
    url = f"https://api.notion.com/v1/pages/{searchObj_toDelete.id}"
    response = requests.request("PATCH", url, headers=headers, data=payload)
    print(response.content)

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