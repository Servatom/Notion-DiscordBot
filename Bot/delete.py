import requests
import json
import os
from deleteGoogleDrive import delete_file

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

def deleteMe(searchObj_toDelete):
    # Deleting the record/page of the table using PATCH
    global headers
    url = f"https://api.notion.com/v1/pages/{searchObj_toDelete.id}"
    response = requests.request("PATCH", url, headers=headers, data=payload)
    print(response.content)

    #Check if the url of the object is a drive link

    url_of_obj = searchObj_toDelete.url
    if("drive" in url_of_obj and "file" in url_of_obj):
      file_id = url_of_obj.split('/')[-1]
      delete_file(file_id)
    


    