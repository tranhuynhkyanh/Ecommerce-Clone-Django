from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauth.models import User
from core.models import Address
from urllib import request

def user_directory_path(instance,filename):
    return 'user_{0}/{1}'.format(instance.id,filename)
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'input','placeholder':'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    class Meta:
        model = User
        fields = ['username','email'] 
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={ 'placeholder': 'Password from numbers and letters of the Latin alphabet'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={ 'placeholder': 'Password confirmation'})

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'input'}))
    last_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'input','placeholder': 'Last name'}))
    image = forms.ImageField()
    class Meta:
        model = User
        fields = ['first_name','last_name','image'] 

class AddressEditForm(forms.ModelForm):
    address = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'input','placeholder': 'Address'}))
    phone = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'input','placeholder': 'Phone number'}))
   # location = forms.PointField(required=False)
    class Meta:
        model = Address
        fields = ['address','phone'] 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].widget.attrs['placeholder'] = self.fields['address'].label or 'Address'
        self.fields['phone'].widget.attrs['placeholder'] = self.fields['phone'].label or 'Address'