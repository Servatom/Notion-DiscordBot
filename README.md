# Notion-DiscordBot



[![Build Status](https://travis-ci.com/Servatom/Notion-DiscordBot.svg?branch=main)](https://travis-ci.com/Servatom/Notion-DiscordBot)<br>
<br>
<p align="center">
<img src="https://servatom.com/assets/bannerDark.PNG" height="200px">
  
<h3 align="center"> A discord bot consuming Notion API to add and retrieve data from Notion databases. </h3>
</p>
<br>
<br>
<br>

## Instructions to use the bot:

### Pre-Requisites:


a)Install all the requirements using ```pip3 install -r requirements.txt```

b)Create a discord bot using the developer platform of discord and obtain your **OAuth2 token**. Keep it somewhere safe

c)Go to Notion and create a new Integration  https://www.notion.so/my-integrations
Note the internal Integration.

d)Go to Notion and create a table like this:

<img src="https://servatom.com/assets/DiscordNotionBot/TableHeader%20.png">

4 columns where:
- Contributor is of property type Title
- URL of url type
- Title of text type
- Tag of multi-select type

e)Click on the three dots and press Open as page

 <img src="https://servatom.com/assets/DiscordNotionBot/OpenPage.png">
 
 <br>
 
 f)Then press share and copy the URL. The URL will look something like this:
https://www.notion.so/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX?v=YYYYYYYYYYYYYYYYYYYYYYYYY

<img src="https://servatom.com/assets/DiscordNotionBot/databaseID.png">

Note down the X part of the url (RED part)

This is your database id

g)Also press share again, press Invite and then click on the integration you made earlier

f)Now on the terminal of your machine:

```$export DATABASE_TOKEN=<THE DATABASE TOKEN YOU NOTED DOWN>```

```$export AUTH_KEY=<THE INTEGRATION SECRET KEY FROM NOTION>```

```$export DISCORD_AUTH=<THE SECRET TOKEN OF BOT>```

### Running Procedure:


a)Now simply go into the Bot folder and run: ```$python3 bot.py```

b)On the discord developer site copy the OAuth2 link and paste it in the browser and invite it to a server you own/have permissions to do so

c)Bot Usage:

#### Adding Record:

```/add <URL_YOU_WANT_TO_RECORD>``` => This will add a new record to your database with a ```misc``` tag

```/add <URL_YOU_WANT_TO_RECORD> <TAG>``` => Will add this tag

For multiple tags:

```/add <URL_YOU_WANT_TO_RECORD> <TAG>,<TAG1>,<TAG2>```<br>
Example:<br>
<img src="https://servatom.com/assets/DiscordNotionBot/addRecord.png"><br>

Sample database populated by the bot:

<img src="https://servatom.com/assets/DiscordNotionBot/db.png">

#### Searching Record through tags:
```/search <Tag1>```<br>

For multiple tags:  ```/search <Tag1> <Tag2>.....<TagN>```<br>

Example:<br>
<img src="https://servatom.com/assets/DiscordNotionBot/search.png">

Instead of running the discord bot via python and exporting environment variables you can use our docker container. 

### Link to image: <a href="hub.docker.com/repository/docker/servatom/notiondiscordbot">hub.docker.com/repository/docker/servatom/notiondiscordbot<a>
