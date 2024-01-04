from django.forms import ModelForm
from .models import Room,User
from django.contrib.auth.forms import UserCreationForm

class RoomForm(ModelForm):
    class Meta():
        model = Room
        # fields = ['name','body'] # default customized version
        fields='__all__' # This will include all fields from Room in form except date time as they are not editable fields
        exclude = ['host','participants']


class UserForm(ModelForm):
    class Meta():
        model = User
        fields = ['avatar','name','username','email','bio']
        exclude=[]