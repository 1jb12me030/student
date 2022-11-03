from django.db import models


from chatbot.models import Questionaire
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Registration(AbstractUser):
    username=models.CharField(max_length=40,unique=True)
    first_name=models.CharField(max_length=60, null=True, blank=True) 
    last_name=models.CharField(max_length=60, null=True, blank=True)
    email=models.CharField(max_length=60,unique=True,verbose_name='email',null=True, blank=True)
    
    location=models.TextField(null=True,blank=True)
    gender=models.CharField(max_length=6,null=True,blank=True)
    profile_pic=models.ImageField(upload_to='image',null=True,blank=True)
    mobile_no=models.CharField(max_length=13)
    birth_place=models.CharField(max_length=30,null=True,blank=True)
    
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username + " " + self.email
    





class Chat(models.Model):
    user=models.ForeignKey(Registration,on_delete=models.CASCADE,)
    questionaire = models.ForeignKey(Questionaire, on_delete=models.CASCADE)
    status = models.PositiveIntegerField(default=1,null=True)
    log = models.TextField(default='')

    def __str__(self):
        return self.log
    
