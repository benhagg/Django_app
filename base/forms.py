from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User

class RoomForm(ModelForm): # model based forms. creating a form that is based on the values in the Room model
    class Meta:    
        model = Room
        fields = '__all__' # customizable based on the model class variables
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'bio', 'avatar']
        
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
