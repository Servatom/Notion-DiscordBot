# Notion-DiscordBot



[![Build Status](https://travis-ci.com/Servatom/Notion-DiscordBot.svg?branch=main)](https://travis-ci.com/Servatom/Notion-DiscordBot)[![Visits Badge](https://badges.pufler.dev/visits/Servatom/Notion-DiscordBot)](https://github.com/Servatom/Notion-DiscordBot/)<br>
<br>
<p align="center">
<img src="https://i.imgur.com/sSqTu56.png" height="200px">
  
<h3 align="center"> A discord bot consuming Notion API to add and retrieve data from Notion databases. </h3>
</p>
<br>
<br>
<br>

## Instructions to use the bot:

  Invite the bot using [Bot Invite Link](https://discord.com/api/oauth2/authorize?client_id=859893575227670528&permissions=274877910016&scope=bot) and run `*setup` <br>

  To self-host the bot, read [SETUP.md](https://github.com/Servatom/Notion-DiscordBot/blob/main/SETUP.md).
<hr>

### Creating Notion Database:

1. Go to Notion and create a new [Integration](https://www.notion.so/my-integrations).
  Note the internal Integration.

2. Then in Notion create a table like this (Tag being optional field):

<img src="https://assets.servatom.com/Notion-DiscordBot/TableHeader.png">

4 columns where:
- Contributor is of property type Title
- URL of url type
- Title of text type
- Tag of multi-select type

3. Click on the three dots and press Open as page

 <img src="https://assets.servatom.com/Notion-DiscordBot/OpenPage.png">
 
 <br>
 
4. Then press share and copy the URL. The URL will look something like this:
https://www.notion.so/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX?v=YYYYYYYYYYYYYYYYYYYYYYYYY

  <img src="https://assets.servatom.com/Notion-DiscordBot/databaseID.png">

  Note down the X part of the url (RED part)

  This is your database id

5. Also press share again, press Invite and then click on the integration you made earlier


## Bot Usage:

1. [Setup](https://github.com/Servatom/Notion-DiscordBot#setup-bot)
2. [Add Record](https://github.com/Servatom/Notion-DiscordBot#adding-record)
3. [Search](https://github.com/Servatom/Notion-DiscordBot#searching-record-through-tags)
4. [Delete](https://github.com/Servatom/Notion-DiscordBot#deleting-record-through-tags)
5. [Upload Files](https://github.com/Servatom/Notion-DiscordBot#uploading-files)
6. [Change Prefix](https://github.com/Servatom/Notion-DiscordBot#changing-prefix)

### Setup Bot:
Run `*setup` command and enter notion api key (the one you got after creating integration) and notion database id. <br>

<img src="https://assets.servatom.com/Notion-DiscordBot/setup.jpeg" width="60%"><br>

### Adding Record:

```*add <URL_YOU_WANT_TO_RECORD>``` => This will add a new record to your database (if tagging is enabled, it will add a `misc` tag)

```*add <URL_YOU_WANT_TO_RECORD> <TAG>``` => This will add a new record to your database with the ```<TAG>``` tag

For multiple tags:
```*add <URL_YOU_WANT_TO_RECORD> <TAG>,<TAG1>,<TAG2>```<br>

Example:<br>
<img src="https://assets.servatom.com/Notion-DiscordBot/add.jpeg" width="60%"><br>

Sample database populated by the bot:

<img src="https://assets.servatom.com/Notion-DiscordBot/db.png">

### Searching Record through tags:
```*search <Tag1>```<br>

For multiple tags:  ```/search <Tag1> <Tag2>.....<TagN>```<br>

### Searching Record through title:
```*title <title>``` <br>

Example:<br>
<img src="https://assets.servatom.com/Notion-DiscordBot/search.jpeg" width="60%">

### Deleting Record through tags:
```*delete <Tag 1>```<br>

For multiple tags: ```*delete <Tag 1> <Tag2>......<Tag N>```<br>

### Deleting Record through title:
```*delete <title>```<br>

Example:<br>
<img src="https://assets.servatom.com/Notion-DiscordBot/delete.jpeg" width="60%"><br>

### Uploading files
NOTE: In the below images the prefix used is: ```*```<br>

You can upload any file to the notion database. It can be a pdf, png, jpeg etc.<br>
Here a png file is being uploaded<br>
1. Drag your file to the chat in discord, add comment to the file you uploaded

<img src="https://assets.servatom.com/Notion-DiscordBot/upload1.jpeg" width="60%"><br>
Here `servatom` is tag for the file.

2. It will then ask the title of the file you uploaded:

<img src="https://assets.servatom.com/Notion-DiscordBot/upload2.jpeg" width="60%"><br>

3. The database will be updated:

<img src="https://assets.servatom.com/Notion-DiscordBot/upload3.jpeg" width="60%"><br>

### Changing Prefix
To change the bot prefix, type `*prefix`, `*` being the deault prefix.

<img src="https://assets.servatom.com/Notion-DiscordBot/prefix.jpeg" width="60%"><br>

<hr><br>

