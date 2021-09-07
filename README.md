# Notion-DiscordBot



[![Build Status](https://travis-ci.com/Servatom/Notion-DiscordBot.svg?branch=main)](https://travis-ci.com/Servatom/Notion-DiscordBot)[![Visits Badge](https://badges.pufler.dev/visits/Servatom/Notion-DiscordBot)](https://github.com/Servatom/Notion-DiscordBot/)<br>
<br>
<p align="center">
<img src="https://servatom.com/assets/bannerDark.png" height="200px">
  
<h3 align="center"> A discord bot consuming Notion API to add and retrieve data from Notion databases. </h3>
</p>
<br>
<br>
<br>

## Instructions to use the bot:

### Pre-Requisites:


a) Install all the requirements using ```pip3 install -r requirements.txt```

b) Create a discord bot using the developer platform of discord and obtain your **OAuth2 token**. Keep it somewhere safe

c) Go to Notion and create a new Integration  https://www.notion.so/my-integrations
Note the internal Integration.

d) Go to Notion and create a table like this:

<img src="https://servatom.com/assets/Notion-DiscordBot/TableHeader%20.png">

4 columns where:
- Contributor is of property type Title
- URL of url type
- Title of text type
- Tag of multi-select type

e) Click on the three dots and press Open as page

 <img src="https://servatom.com/assets/Notion-DiscordBot/OpenPage.png">
 
 <br>
 
 f)Then press share and copy the URL. The URL will look something like this:
https://www.notion.so/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX?v=YYYYYYYYYYYYYYYYYYYYYYYYY

<img src="https://servatom.com/assets/Notion-DiscordBot/databaseID.png">

Note down the X part of the url (RED part)

This is your database id

g) Also press share again, press Invite and then click on the integration you made earlier

h) Google Drive setup:
All physical files or pdf files from links are downloaded on a google drive folder of your choice.

**Setup Procedure:**<br>
  a) <a href=https://github.com/Servatom/Notion-DiscordBot/tree/main/GoogleDrive_Setup>Follow the README file located here</a><br>
  b) Move the ```credentials.json``` file and ```token.json``` to the ```creds``` folder in the Bot folder<br>
  c) Now go to google drive and create a folder. The link of folder will be something like  this https://drive.google.com/drive/folders/ID <br>
  
  d) Note the ID down. This will be the id of the folder where all files will be stored. Also share the folder accordingly<br>

f) Now on the terminal of your machine:

```$export DATABASE_TOKEN=<THE DATABASE TOKEN YOU NOTED DOWN>```

```$export AUTH_KEY=<THE INTEGRATION SECRET KEY FROM NOTION>```

```$export GDRIVE_FOLDER=<FOLDER ID YOU NOTED ABOVE>```

```$export DISCORD_AUTH=<THE SECRET TOKEN OF BOT>```<br>
If you want your prefix to be something else other than '/' then 
```$export PREFIX=<Your Desired character>```

## Running Procedure:


a) Now simply go into the Bot folder and run: ```$python3 bot.py```

b)On the discord developer site copy the OAuth2 link and paste it in the browser and invite it to a server you own/have permissions to do so

c) Bot Usage:

### Adding Record:

```/add <URL_YOU_WANT_TO_RECORD>``` => This will add a new record to your database with a ```misc``` tag

```/add <URL_YOU_WANT_TO_RECORD> <TAG>``` => This will add a new record to your database with the ```<TAG>``` tag

For multiple tags:

```/add <URL_YOU_WANT_TO_RECORD> <TAG>,<TAG1>,<TAG2>```<br>
Example:<br>
<img src="https://servatom.com/assets/Notion-DiscordBot/addRecord.png"><br>

Sample database populated by the bot:

<img src="https://servatom.com/assets/Notion-DiscordBot/db.png">

### Searching Record through tags:
```/search <Tag1>```<br>

For multiple tags:  ```/search <Tag1> <Tag2>.....<TagN>```<br>

Example:<br>
<img src="https://servatom.com/assets/Notion-DiscordBot/search.png">
<img src="https://www.servatom.com/assets/Notion-DiscordBot/multiTagSearch.png"><br>


### Deleting Record through tags:
```/delete <Tag 1>```<br>

For multiple tags: ```/delete <Tag 1> <Tag2>......<Tag N>```<br>

Example:<br>
<b>Intial database:</b><br>
<img src="https://servatom.com/assets/Notion-DiscordBot/initialDB.png"><br>

<b>Deleting Record:</b><br>
<img src="https://servatom.com/assets/Notion-DiscordBot/delete.png"><br>

<b>Final Database:</b><br>
<img src="https://servatom.com/assets/Notion-DiscordBot/finalDB.png"><br>

### Uploading files
NOTE: In the below images the prefix used is: ```!```<br>

You can upload any file to the notion database. It can be a pdf, png, jpeg etc.<br>
Here a png file is being uploaded<br>
a) Drag your file to the chat in discord

<img src="https://servatom.com/assets/Notion-DiscordBot/drag.png" width="50%"><br>

b) Add comment to the file you uploaded

<img src="https://servatom.com/assets/Notion-DiscordBot/comment.png" width="50%"><br>
Here memoji and profile-pic are tags for the file

c) It will then ask the title of the file you uploaded:

<img src="https://servatom.com/assets/Notion-DiscordBot/finalUploaded.png" width="50%"><br>

d) Now the file will uploaded on the google drive folder which you mentioned above

e) The database will be updated:

<img src="https://servatom.com/assets/Notion-DiscordBot/recordAddedImg.png"><br>

f) The link will open the file in google drive

<hr><br>

Instead of running the discord bot via python and exporting environment variables you can use our docker container. <br>
### Link to image: <a href="https://hub.docker.com/repository/docker/servatom/notiondiscordbot">Docker Hub</a>

<hr><br>
You can also deploy this on heroku. Please follow the additional instructions here: <a href = "https://github.com/Servatom/Notion-DiscordBot/blob/main/HEROKU-SETUP.md"> Heroku Setup</a>
