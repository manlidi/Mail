from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Utilisateur(AbstractUser):
    numero =  models.CharField(max_length=100)
    password = models.TextField()
    confirmation_token = models.CharField(max_length=200, default='NULL')
    photo=models.ImageField(upload_to='user', default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
