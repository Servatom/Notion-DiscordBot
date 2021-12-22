import requests
from bs4 import BeautifulSoup
from database import SessionLocal, engine
import models


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

# testing purposes only
#for obj in searchByTitle("django", "9e449365893e4657a5502f4723771ece", "secret_D50ybSSLDed6mTFOy188nHShw2XWPh2v1FFiUAviMfG"):
 #  print(obj.title)

def checkIfGuildPresent(guildId):
    guild = db.query(models.Clients).filter(models.Clients.guild_id == guildId).first()
    if guild:
        return True
    return False

def getQueryForTitle(args):
    query = ""
    # check args
    if(len(args) > 0):
        # received data
        for arg in args:
            query += arg + " "
    else:
        # no data received
        return None
    query = query.strip()
    return query