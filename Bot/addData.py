from database import SessionLocal, engine
import models


db = SessionLocal()


guild_id = int(input("Guild ID: "))
notion_api_key = input("Notion API Key: ")
notion_db_id = input("Notion DB ID: ")
# if input 1 then true else false
isTag = input("Tag (1/0): ")
if isTag == "1":
    isTag = True
else:
    isTag = False

prefix = input("Prefix: ")

# save it
db.add(models.Clients(guild_id, notion_api_key, notion_db_id, isTag, prefix))
db.commit()
