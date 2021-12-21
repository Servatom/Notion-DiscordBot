import requests
from bs4 import BeautifulSoup
from database import SessionLocal, engine
import models
from fuzzywuzzy import fuzz
import json

db = SessionLocal()


class SearchData:
    id = ""
    title = ""
    url = ""

    def __init__(self, id, title, url):
        self.id = id
        self.title = title
        self.url = url

def getTitle(url):
    try:
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')
        title_tag = soup.find('title')
        return title_tag.get_text()
    except:
        return None

def getGuildData():
    data = {}
    guilds = db.query(models.Clients).all()
    for guild in guilds:
        data[str(guild.guild_id)] = guild
    return data

def getPrefixes():
    prefixes = {}
    guilds = db.query(models.Clients).all()
    for guild in guilds:
        prefixes[str(guild.guild_id)] = guild.prefix
    return prefixes

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

# testing purposes only
#for obj in searchByTitle("django", "9e449365893e4657a5502f4723771ece", "secret_D50ybSSLDed6mTFOy188nHShw2XWPh2v1FFiUAviMfG"):
 #  print(obj.title)

def checkIfGuildPresent(guildId):
    guild = db.query(models.Clients).filter(models.Clients.guild_id == guildId).first()
    if guild:
        return True
    return False