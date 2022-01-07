import requests
import json
from database import SessionLocal, engine
import models
from bs4 import BeautifulSoup

db = SessionLocal()

url = "https://api.notion.com/v1/pages"

def getTitle(url):
    try:
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')
        title_tag = soup.find('title')
        return title_tag.get_text()
    except:
        return None

def addAllData(url, notion_api_key, notion_db_id, contributor, tag, title):
    data_to_be_written = {
        "parent": {
            "database_id": notion_db_id
        },
        "properties": {
            "Tag": {
                "multi_select": tag
            },
            "Title": {
                "rich_text": [
                    {
                        "text": {
                            "content": title,
                        },
                        "annotations": {
                            "bold": True,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "yellow"
                        }
                    },

                ]
            },
            "URL": {
                "url": url
            },
            "Contributor": {
                "title": [
                    {
                        "text": {
                            "content": contributor,
                        },
                    }
                ]
            }
        }
    }
    payload = json.dumps(data_to_be_written)
    sendData(payload, notion_api_key)

def addDataWithoutTag(url, notion_api_key, notion_db_id, title, contributor):
    data_to_be_written = {
        "parent": {
            "database_id": notion_db_id
        },
        "properties": {
            "Title": {
                "rich_text": [
                    {
                        "text": {
                            "content": title,
                        },
                        "annotations": {
                            "bold": True,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                        }
                    },

                ]
            },
            "URL": {
                "url": url
            },
            "Contributor": {
                "title": [
                    {
                        "text": {
                            "content": contributor,
                        },
                    }
                ]
            }
        }
    }
    payload = json.dumps(data_to_be_written)
    sendData(payload, notion_api_key)

def sendData(payload, notion_api_key):
    headers = {
        'Authorization': notion_api_key,
        'Notion-Version': '2021-05-13',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    print(response.status_code)