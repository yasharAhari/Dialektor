# Dialektor
Group APYZ CS 4263 Software Engineering Capstone project

Under supervision of:<br> 
Dr. Rafal Jabrzemski

TEAM: APYZ

Adam Gracy<br>
Phillip Voss<br>
Yashar G. Ahari<br>
Zachary Arani<br>

[what is Dialektor](./Documentation/Dialektor.md)

### Version info
Currently running version on google cloud: Beta-0 
[dialekt.appspot.com_version_Beta-0](https://dialekt.appspot.com/)

About Version Beta-0:<br>
Beta-0 is the almost finished version of the final product, lacking the final cosmetic touches and the researchers page and functionality. The sound recording, playback, storage, profile, collection all functional. 

### Important notes: 

#### A word about google cloud 
You may notice there are 3 files that are not part of a usual 
Django app. 
1. app.yaml <br>
This files contains the configuration to run the app in google cloud app engine.
2. requirements.txt <br> 
This is the file that can get by ```pip freeze > requirements.txt```. Contains all the project python dependencies.
Google cloud will look for this file and install all the listed packages.
3. main.py <br>
Google app engine looks for this file to starts the our application. In this file, we just restate our 
wsgi choice. 

This is a great article about the process:<br>
[Deploying a Django Application to Google App Engine](https://medium.com/@BennettGarner/deploying-a-django-application-to-google-app-engine-f9c91a30bd35)

#### Installation and running locally

As usual, start with a git clone, <br>
```bash
git clone https://github.com/yasharAhari/Dialektor.git
```
go to the ```Dialektor_``` directory by typing
```bash
ls Dialektor_
```
and run the following command:<br>
 
Windows:
```cmd
python manage.py runserver
```

linux
```bash
chmod +x manage.py 
./manage.py runserver
```

you can also run tests 
```bash
python manage.py test
```

After this step the Development server will start working. 
You should be able to see the website on 
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)


#### Deployment on google cloud:
Each time after few feature implemented, I will be updating it to the Google cloud.
I am thinking to assign a version number to each upload as something like a release version. 

If you like to try it on your own google cloud account, I suggest you to follow the instructions on 
this link:

[Deploying a Django Application to Google App Engine](https://medium.com/@BennettGarner/deploying-a-django-application-to-google-app-engine-f9c91a30bd35)





