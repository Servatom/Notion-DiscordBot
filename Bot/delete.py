import requests
import json
import os

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

headers = {
    'Authorization': os.environ["AUTH_KEY"],
    'Notion-Version': '2021-05-13',
    'Content-Type': 'application/json'
}

def deleteMe(id):
    # Deleting the record/page of the table using PATCH
    global headers
    url = f"https://api.notion.com/v1/pages/{id}"
    response = requests.request("PATCH", url, headers=headers, data=payload)
    print(response.content)
    