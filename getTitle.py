import requests
from bs4 import BeautifulSoup

def giveTitle(given_url):
    url  = given_url

    try:
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')
        title_tag = soup.find('title')
        return title_tag.get_text()
    except:
        return "Generic title"
