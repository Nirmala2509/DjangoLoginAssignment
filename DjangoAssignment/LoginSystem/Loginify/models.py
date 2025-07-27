from django.db import models

# Create your models here.
class Register(models.Model):
    username=models.CharField(max_length=50,primary_key=True)
    email=models.CharField(max_length=30,unique=True)
    password=models.EmailField(max_length=12,blank=True)
