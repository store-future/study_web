from django.db import models

# Create your models here.
# models.py
from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
