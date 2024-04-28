from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

class RoomForm(ModelForm): # model based forms. creating a form that is based on the values in the Room model
    class Meta:    
        model = Room
        fields = '__all__' # customizable based on the model class variables
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        
