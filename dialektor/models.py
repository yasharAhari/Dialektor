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

