from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(null=True,unique=True)
    bio = models.TextField(null=True)

    # avatar=

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

# Create your models here.
   
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic= models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) # If Topic was placed below Room in code then we would pass 'Topic' instead 
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True) # null=True means null value can be allowed,blank is for forms meaning now field can be left blank
    participants=models.ManyToManyField(User,related_name='participants',blank=True)
    updated = models.DateTimeField(auto_now=True) # it saves time stamp whenever we save the instance, it will change after every save
    created = models.DateTimeField(auto_now_add=True) # it would save the time stamp of first creation of instance, it wont change

    def __str__(self):
        return self.name
    
    
    class Meta():
        ordering =['-updated','-created'] # orders rooms by first updated value then created, - is used for descending order
 

class Message(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE) #if room is deleted message will also be deleted, parent deleted child also deleted
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50] # in preview we only want first 50 characters to prevent a lot of text
    
    class Meta():
        ordering =['-updated','-created']
    