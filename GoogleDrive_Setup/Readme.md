# Google Drive Setup

> Go to this site: https://console.cloud.google.com 

### A) Creating a project.

On the top blue menu bar, click on "**Select a project**"

<img src="https://servatom.com/assets/GDriveAPI/Screenshot%202021-07-09%20at%2012.33.23%20PM.png">

Click on “**New Project**”

Then you will see something like this:

<img src="https://servatom.com/assets/GDriveAPI/Screenshot%202021-07-09%20at%2012.36.28%20PM.png">

Give your project some name and leave everything else to default. 

You will be redirected the GCP dashboard. Go to the sidebar and click on "**API & Service**"

<img src="https://servatom.com/assets/GDriveAPI/apiService.png">

Now click on Enable APIs and Services

<img src="https://servatom.com/assets/GDriveAPI/Screenshot%202021-07-09%20at%2012.40.04%20PM.png">

Now in the API Library Search for the "**Google Drive API**"

<img src="https://servatom.com/assets/GDriveAPI/g.png">

Click on the Google Drive API and press "**Enable**".

<img src="https://servatom.com/assets/GDriveAPI/Screenshot%202021-07-09%20at%2012.42.11%20PM.png">

Now here click on "**Create Credentials**".


Now in Credential Type: in the drop down menu choose the google drive api and then click on User Data.

<img src="https://servatom.com/assets/GDriveAPI/credType.png">

Click on next

Now give your app a name and also put in your email id. 

<img src="https://servatom.com/assets/GDriveAPI/oauthConsent.jpeg" width="50%">

Click on Save and Continue

Here click on "**Add Or Remove Scopes**"

<img src="https://servatom.com/assets/GDriveAPI/scope.png">

And this:

<img src="https://servatom.com/assets/GDriveAPI/list.png">

Then click on "**Update**"
And then press save and continue.

<img src="https://servatom.com/assets/GDriveAPI/oauthClientID.png">

Here the application type is Desktop App and you can enter any name you like

Click on "**Create**"

<img src="https://servatom.com/assets/GDriveAPI/download.png">

You will see this. Just press on download
And rename that json file as  “credentials.json”


Now on the left sidebar click on OAuth consent screen

<img src="https://servatom.com/assets/GDriveAPI/consent.png">

Click on Make External 
and then press on Testing

<img src="https://servatom.com/assets/GDriveAPI/testing.png">

Click on "**Confirm**"

Scroll down to the Test Users section and press on Add Users

In the text field add the email id which will be giving its Google Drive access

<img src="https://servatom.com/assets/GDriveAPI/addUser.png">

Click on Save

Now you are done.


### B) Generating the token.json file

Keep the credentials.json file and generateTokenAuth.py in one folder

Now create a virtual environment using pipenv. 
```$pipenv install```
And then do ```$pipenv install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib```

Now enter the pipenv shell
```$pipenv shell```

Run the generateTokenAuth.py

```$python3 generateTokenAuth.py ```

If all goes well the web browser must open. 
Sign in to the google drive account you mentioned earlier in the tester step

<img src="https://servatom.com/assets/GDriveAPI/notVerify.png">

Click on Continue then it will ask you to grant permissions.

Keep pressing Allow

<img src="https://servatom.com/assets/GDriveAPI/grant.png">

Click on Allow

<img src="https://servatom.com/assets/GDriveAPI/allow.png">

When the popups close click here allow too

And accept all the conditions it asks.

<img src="https://servatom.com/assets/GDriveAPI/success.png">

When this comes this means it was successful.

<img src="https://servatom.com/assets/GDriveAPI/token.png">

And you are done. As you can see you now have the ```token.json``` file and ```credentials.json``` file
