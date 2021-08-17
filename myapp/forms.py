from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from myapp.models import *


class NoteCreateForm(ModelForm):
    class Meta:
        model = Note
        fields = ('text', 'title', 'price', 'instock')


class UserCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'money')


class TovarForm(ModelForm):
    class Meta:
        model = Buy
        fields = ('quantity',)

class TovarReturn(ModelForm):
    class Meta:
        model=ReturnBuy
        fields= ('returnBuy', )
