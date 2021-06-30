import requests
import json
from getTitle import giveTitle
import os
url = "https://api.notion.com/v1/pages"
database = os.environ["DATABASE_TOKEN"]
def addData(url, contributor, tag="misc"):
    data_to_be_written = {
        "parent":{
            "database_id": database
        },
        "properties": {
        "Tag": {
        "rich_text": [
                {
                "text": {
                    "content": tag,
                    }
                }
            ]
        },
        "Title": {
            "rich_text": [
                {
                    "text": {
                        "content": giveTitle(url),
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

    #Posting the dictionary on the database
    payload = json.dumps(data_to_be_written)
    sendData(payload)

def sendData(payload):
    headers = {
        'Authorization': os.environ["AUTH_KEY"],
        'Notion-Version': '2021-05-13',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.status_code)