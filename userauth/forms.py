from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauth.models import User
from core.models import Address
def user_directory_path(instance,filename):
    return 'user_{0}/{1}'.format(instance.id,filename)
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'input','placeholder':'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Repeat password"}))
    class Meta:
        model = User
        fields = ['username','email'] 

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'input'}))
    last_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'input','placeholder': 'Last name'}))
    image = forms.ImageField()
    class Meta:
        model = User
        fields = ['first_name','last_name','image'] 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = self.fields['first_name'].label or 'First name'
class AddressEditForm(forms.ModelForm):
    address = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'input','placeholder': 'Address'}))
    phone = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'input','placeholder': 'Phone number'}))
    class Meta:
        model = Address
        fields = ['address','phone'] 
