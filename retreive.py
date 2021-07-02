import requests
import json

url = "https://api.notion.com/v1/databases/9e449365893e4657a5502f4723771ece/query"

payload = json.dumps({
  "filter": {
    "property": "Contributor",
    "title": {
      "contains": "@raghavTinker"
    }
  }
})
headers = {
  'Authorization': 'secret_UUy9xtYmdV9UsfZN3ol6Eiq63QPPSGntbutOdhr76Bl',
  'Notion-Version': '2021-05-13',
  'Content-Type': 'application/json'
}
query = {"filter": {"property": "Contributor","title": {"contains": "Raghav"}}}
response = requests.post(url, headers=headers, data=payload)
print(type(response.json()))
print(response.json())