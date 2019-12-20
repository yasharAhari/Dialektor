# Dialektor

Group APYZ CS 4263 Software Engineering Capstone project

Under supervision of:<br>
Dr. Rafal Jabrzemski

TEAM: APYZ

Adam Gracy<br>
Phillip Voss<br>
Yashar G. Ahari<br>
Zachary Arani<br>

[What is Dialektor?](./Documentation/Dialektor.md)

### Version info

Currently running version on google cloud: 0.0.2
[dialekt.appspot.com_version_0.0.2](https://dialekt.appspot.com/)

About Version 0.0.2:<br>
There are few small but necessary changes on the way templates are structured
to meet the Django format specifications. Also all of the static files moved to dedicated 
google storage bucket. This will not add any new functionality from version 0.0.1.
Plus: Added favicon.   

About Version 0.0.1:<br>
It is the initial working bed to implement backend functionality.
It features the login and signup pages but neither of those has any
backend functions... yet.

### Important notes:

#### A word about google cloud

You may notice there are 3 files that are not part of a usual
Django app.

1. app.yaml <br>
   This files contains the configuration to run the app in google cloud app engine.
2. requirements.txt <br>
   This is the file that can get by `pip freeze > requirements.txt`. Contains all the project python dependencies.
   Google cloud will look for this file and install all the listed packages.
3. main.py <br>
   Google app engine looks for this file to starts the our application. In this file, we just restate our
   wsgi choice.

This is a great article about the process:<br>
[Deploying a Django Application to Google App Engine](https://medium.com/@BennettGarner/deploying-a-django-application-to-google-app-engine-f9c91a30bd35)

Also A word about [Static Files](#static-files)

#### Installation and running locally

As usual, start with a git clone, <br>

```bash
git clone https://github.com/yasharAhari/Dialektor.git
```

go to the `Dialektor` directory by typing:

```bash
ls Dialektor
```

<span style="color:red">\*Note:</span> For the following command to run, you may first need to install the required modules list in `requirements.txt` (if you haven't already). To do this, simply navigate to the directory containting `requirements.txt` and type

 ``` bash
pip install -r requirements.txt
 ```

Then run the following command:<br>

Windows:

```cmd
python manage.py runserver
```

Linux

```bash
chmod +x manage.py
./manage.py runserver
```

After this step, the development server will start working.
You should be able to see the website on
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

#### Deployment on google cloud:

Each time after few feature implemented, I will be updating it to the Google cloud.
I am thinking to assign a version number to each upload as something like a release version.

#### Static Files!

The Django framework is not meant to serve static files. Static files are basically all the files that wont get changed by Django. These include all stylesheets (.CSS), JavaScript (.js) and any other images (like logo, favicon, ...). The reason is that the Django is for serving a content that meant to change. 

<strong>All the statics files that are located in the statics directory are hosted on a dedicated google storage bucket. </strong>

For the development purpose, you can add your static files in statics directory and for use the following line every where you need an address for that file: 

```django
{% static 'path/to/your_FILE/in/static/dir/file.css' %}
```

for example to load the stylesheet in an html template:

```django
<link rel="stylesheet" href="{% static 'file.css' %}" />
```



If you like to try it on your own google cloud account, I suggest you to follow the instructions on
this link:

[Deploying a Django Application to Google App Engine](https://medium.com/@BennettGarner/deploying-a-django-application-to-google-app-engine-f9c91a30bd35)
