# Heroku Setup
You can also deploy this bot on heroku.<br>

On heroku you will need to define all the environment variables in the settings page. Define all the environment variables that were mentioned in the README.md file<br>

For GDrive support:
Follow whatever was told related to the GDrive setup in the README.md file. But instead of moving files just copy the contents of the ```token.json``` file<br>
In the environment variable do this:<br>

KEY: ```GOOGLE_APPLICATION_CREDENTIALS```   VALUE: ```google-credentials.json```<br>
KEY: ```GOOGLE_CREDENTIALS```   VALUE: ```<CONTENT OF token.json file>```<br>

In the heroku dashboard in the buildpacks section add this: https://github.com/buyersight/heroku-google-application-credentials-buildpack

And you should be done!
