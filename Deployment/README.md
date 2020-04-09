## Deployment
Our project is web based and is hosted on the Google App engine. It utilizes Google storage and Google database services.

To deploy, you will need a Google account, and permissions for the above services. Most of reqired configurations are in the setting file and ready to go, with few exceptions: 

### Pre deployement checklist

### GCP 
1. Download and install Google Cloud SDK and make sure logged in to an approved account 

#### Cloud Storage Buckets
1. Create a Google Storage Bucket, name it "dialekt_storage".
2. Follow the instruction [here](https://django-storages.readthedocs.io/en/latest/backends/gcloud.html) and download the Credentials JSON file. Make Sure the listed python packages in the instruction are installed and the python setting file edited properly.
3. Add the downloaded file to the Dialektor/dialektor/GS_Credentials. 

#### Database prep. 

1. In the Dialektor/Dialektor_/settings.py, find the DATABASES section and change the HOST ip to '35.225.20.84' 


### Final step: Deploy 

1. To deploy, make sure you are in the same directory as the `app.yaml` is located. 
2. Issue the follwing command: 
```
gcloud app deploy ./app.yaml
```

Wait until the process is over. 


