# Hosting the bot yourself setup

## Option 1: Running it as a simple python application

Prerequistes:<br>
a) Install the requirements: ```pip install -r requirements.txt```<br>

b) Create a discord bot using the developer platform of discord and obtain your **OAuth2 token**. Keep it somewhere safe

c) Create a database folder in the Bot directory

d) Export the token as an environment variable: ```export TOKEN=<OAUTH TOKEN>```

e) Generate a secret key which will be used for encrypting the database and keep it safe. Export this key as an environment variable => ```export SECRET_KEY=<SECRET_KEY>```

f) Go into the Bot directory and then run: ```python bot.py```

g) Get the bot invite link from the discord developer platform and invite them to your desired servers!


## Option 2: Running it as a docker container
a) Create a discord bot using the developer platform of discord and obtain your **OAuth2 token**. Keep it somewhere safe

b) In the ```docker-compose.yml``` file at line 12 change the ```TOKEN``` variable with the OAUTH token you received above.
The line should look like this: ```- TOKEN=YOUR OAUTH TOKEN```

c) Generate a secret key which will be used for encrypting the database and keep it safe. In the ```docker-compose.yml``` file at line 14 change the ```SECRET_KEY``` variable with the SECRET_KEY you generated above. The line should look like this: ```- SECRET_KEY=YOUR SECRET KEY```

d) Create a ```database``` folder in the root directory.

e) Now to run the container simply run:
```docker-compose up --build```

f) Get the bot invite link from the discord developer platform and invite them to your desired servers!
