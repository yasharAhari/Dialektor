from django.db import models
from django.contrib.auth.models import User, AbstractUser

class CustomUser(AbstractUser):
    pass
    inst_name = models.CharField(max_length=100)
    inst_addr = models.CharField(max_length=100)
    inst_city = models.CharField(max_length=100)
    inst_state = models.CharField(max_length=100)
    inst_country = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100, primary_key=True, default="noID")

    def __str__(self):
        return self.username

class metadata(models.Model):
    user_id = models.CharField(max_length=100, default='defaultUser')
    rec_length = models.DurationField()
    collection = models.CharField(max_length=200, default='defaultCollection')
    tags = models.CharField(max_length=200, default='defaultTags')
    category = models.CharField(max_length=100, default='defaultCategory') #I think we also are going to want a file ID as well (hash of length+collection+tags)
    title = models.CharField(max_length=300, default='defaultTitle')
    fileID = models.CharField(max_length=100, default='defaultID', primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    nonce = models.CharField(max_length=100, default='defaultNonce')

    def __str__(self):
        return self.fileID


class collection(models.Model):
    name = models.CharField(max_length=200, default='defaultName')
    user_id = models.CharField(max_length=100, default='defaultUser')
    pic_id = models.CharField(max_length=100, default='default_id')
