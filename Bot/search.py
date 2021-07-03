import os
import json
import requests


class SearchObject:
    # Class for Search Results
    title = ""
    url = ""

    def __init__(self, url, title):
        self.url = url
        self.title = title


def searchTag(args):
    # Search for a tag
    url = "https://api.notion.com/v1/databases/" + \
        os.environ['DATABASE_TOKEN'] + "/query"
    payload = json.dumps({
        "filter": {
            "property": "Tag",
            "multi_select": {
                "contains": args
            }
        }
    })
    headers = {
        'Authorization': os.environ["AUTH_KEY"],
        'Notion-Version': '2021-05-13',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)

    query_results = response.json()["results"]
    no_of_results = len(query_results)

    search_results = []
    if no_of_results == 0:
        # No results found
        return(search_results)

    for result in query_results:
        # Create Search Object for each result
        search_object = SearchObject(
            result["properties"]["URL"]["url"], result["properties"]["Title"]["rich_text"][0]["plain_text"])
        search_results.append(search_object)

    return(search_results)
