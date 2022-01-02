# Hosting the bot yourself setup

## Option 1: Running it as a simple python application

Prerequistes:<br>
a) Install the requirements: ```pip install -r requirements.txt```<br>

b) Create a discord bot using the developer platform of discord and obtain your **OAuth2 token**. Keep it somewhere safe

c) Create a database folder in the Bot directory

d) Export the token as an environment variable: ```export TOKEN=<OAUTH TOKEN>```

e) Go into the Bot directory and then run: ```python bot.py```

f) From the discord developer page get the bot invitation link and invite them to different servers!


## Option 2: Running it as a docker container
a) Create a discord bot using the developer platform of discord and obtain your **OAuth2 token**. Keep it somewhere safe

b) In the ```docker-compose.yml``` file at line 13 change the ```TOKEN``` variable with the OAUTH token you received above.
The line should look like this: ```- TOKEN=YOUR OAUTH TOKEN```

c) Create a ```database``` folder in the root directory.

d) Now to run the container simply run:
```docker-compose up --build```

e) Get the bot invite link from the discord developer platform and invite them to your desired servers!
