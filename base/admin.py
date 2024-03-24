from django.contrib import admin

# Register your models here. (gets the models from models.py and registers it with the admin site)

from .models import Room, Topic, Message

admin.site.register(Room) # this will add the model to the admin site
admin.site.register(Topic)
admin.site.register(Message) 