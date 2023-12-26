from django.db import models

# Create your models here.

class Room(models.Model):
    #host=
    #topic=
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True) # null=True means null value can be allowed,blank is for forms meaning now field can be left blank
    #participants=
    updated = models.DateTimeField(auto_now=True) # it saves time stamp whenever we save the instance, it will change after every save
    created = models.DateTimeField(auto_now_add=True) # it would save the time stamp of first creation of instance, it wont change

    def __str__(self):
        return self.name

