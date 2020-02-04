from django.db import models
from django.contrib.auth.models import User, AbstractUser

class CustomUser(AbstractUser):
    pass
    inst_name = models.CharField(max_length=100)
    inst_addr = models.CharField(max_length=100)
    inst_city = models.CharField(max_length=100)
    inst_state = models.CharField(max_length=100)
    inst_country = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class metadata(models.Model):
    user_id = models.CharField(max_length=100, default='defaultID')
    rec_length = models.DurationField()
    collection = models.CharField(max_length=200, default='defaultCollection')
    tags = models.CharField(max_length=200, default='defaultTags')
    category = models.CharField(max_length=100, default='defaultCategory') #I think we also are going to want a file ID as well (hash of length+collection+tags)
    title = models.CharField(max_length=300, default='defaultTitle')
    fileID = models.CharField(max_length=100, default='defaultID')



    
