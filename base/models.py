from django.db import models
from django.contrib.auth.models import User # built in user model



# Create your models here. ---------------------------------------------------------------------

class Topic(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    topic = models.ForeignKey(Topic, on_delete = models.SET_NULL, null = True) # if the topic is deleted, room's topic set to null
    name = models.CharField(max_length = 200)
    description = models.TextField(null = True, blank = True) # null for db, blank for form submissions-
    participants = models.ManyToManyField(User, related_name = 'participants') # many to many relationship with User (by fk)
    updated = models.DateTimeField(auto_now = True) # field will be timestamped with every edit to the model
    created = models.DateTimeField(auto_now_add = True) # timestamp for when the model was created


    class Meta: # it allows you to specify options (also known as metadata)
        ordering = ['-updated', '-created'] # newest room will be displayed first

    def __str__(self):
        return self.name
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE) # from default User model
    # one to many relationship with Room (connected by ForeignKey)
    room = models.ForeignKey(Room, on_delete = models.CASCADE) # if the room is deleted, delete the message
    body = models.TextField()
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.body[0:50] # return the first 50 characters of the message body in the preview