from . models import CustomUser,ShippingAddress
from django.forms import ModelForm


class UserCreationForm(ModelForm):
    class Meta:
        model=CustomUser
        fields=['username','phone','email','password']


class ShippingAddressForm(ModelForm):
    class Meta:
        model = ShippingAddress
        fields = '__all__'
