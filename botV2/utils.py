import requests
from bs4 import BeautifulSoup
from database import SessionLocal, engine
import models

db = SessionLocal()

def getTitle(url):
    try:
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')
        title_tag = soup.find('title')
        return title_tag.get_text()
    except:
        return None

def getGuildData():
    data = []
    guilds = db.query(models.Clients).all()
    for guild in guilds:
        data.append(guild.serialize)
    return data

def getPrefixes():
    prefixes = {}
    guilds = db.query(models.Clients).all()
    for guild in guilds:
        prefixes[str(guild.guild_id)] = guild.prefix
    return prefixes