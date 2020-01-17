from django.db import models
from django.contrib.auth.models import User, AbstractUser

class User(AbstractUser):
    is_personal = models.BooleanField(default=False)
    is_research = models.BooleanField(default=False)

class Researcher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    instName = models.CharField(max_length=100)
    instAddrOne = models.CharField(max_length=100)
    instAddrTwo = models.CharField(max_length=100)
    instCity = models.CharField(max_length=100)
    instCountry = models.CharField(max_length=100)

