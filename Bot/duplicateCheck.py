import requests
import json
import os

database = os.environ["DATABASE_TOKEN"]
print(database)
url = "https://api.notion.com/v1/databases/" + str(database) + "/query"

def doesItExist(link):
  payload = json.dumps({
    "filter": {
      "property": "URL",
      "url":{
        "equals": link
      }
    }
  })
  headers = {
    'Authorization': str(os.environ["AUTH_KEY"]),
    'Notion-Version': '2021-05-13',
    'Content-Type': 'application/json'
  }
  response = requests.post(url, headers=headers, data=payload)
  result = response.json()["results"]
  if(len(result) == 0):
    return False
  return True

def amIThere(file):
    filesUploaded = []
    with open("./Bot/dataUploaded.txt") as log:
        filesUploaded = [line.strip() for line in log]
    print(filesUploaded)

    if file in filesUploaded:
        return True
    return False
