from django.db import models
from uuid import uuid4
import os

def user_image_filename(instance, filename):
    """Generate a unique filename for the user's image."""
    ext = filename.split('.')[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join('user/', filename)

# Create your models here.
class User(models.Model):
    class Meta:
        db_table = 'account'
        
    user_type = models.CharField(blank=False, max_length=50)
    name = models.CharField(blank=False, max_length=50)
    contact = models.CharField(blank=False, max_length=50,unique=True)
    email = models.EmailField(blank=False, max_length=100, unique=True)  
    gender = models.CharField(blank=True, max_length=10,default="null")  
    dob = models.DateField()  
    weight = models.CharField(blank=True, max_length=10,default="null")  
    address = models.TextField(blank=True, default=None)  
    password = models.CharField(max_length=200, blank=True, default=None)
    image = models.ImageField(upload_to=user_image_filename, default='user.png',blank=True)
    is_active = models.IntegerField(default = 1)
    timestamp = models.DateTimeField(auto_now_add=True)

class Doctor(models.Model):
    class Meta:
        db_table = 'doctors'
        
    name = models.CharField(blank=False, max_length=50)
    contact = models.CharField(blank=False, max_length=50,unique=True)
    email = models.EmailField(blank=False, max_length=100, unique=True)  
    gender = models.CharField(blank=True, max_length=10,default="null")  
    specialization = models.CharField(blank=True, max_length=100,default="null")  
    address = models.TextField(blank=True, default=None)  
    image = models.ImageField(upload_to=user_image_filename, default='user.png',blank=True)
    is_active = models.IntegerField(default = 1)
    timestamp = models.DateTimeField(auto_now_add=True)

    