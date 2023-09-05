from . models import CustomUser
from django.forms import ModelForm


class UserCreationForm(ModelForm):
    class Meta:
        model=CustomUser
        fields=['username','phone','email','password']