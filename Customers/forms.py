from typing import Any
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms

from Website.forms import *

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        
    def __init__(self, *args: Any, **kwargs: Any):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['id'] = 'Registration_Username'
        
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['id'] = 'Registration_First_Name'
        
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['id'] = 'Registration_Last_Name'
        
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['id'] = 'Registration_Email'
        
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['id'] = 'Registration_Password1'
        
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['id'] = 'Registration_Password2'
        
        
class UserUpdateForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
    
    def __init__(self, *args: Any, **kwargs: Any):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['id'] = 'Registration_Username'

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['id'] = 'Registration_First_Name'

        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['id'] = 'Registration_Last_Name'

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['id'] = 'Registration_Email'
        
        
class UserUpdatePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ("new_password1", "new_password2",)
        
    def __init__(self, *args: Any, **kwargs: Any):
        super(UserUpdatePasswordForm, self).__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['id'] = 'Registration_Username'

        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['id'] = 'Registration_First_Name'
        
        
class UserProfileForm(forms.ModelForm):
    Phone_Number = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "Phone Number"}), required=False)
    Address1 = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "Address Line 1"}), required=False)
    Address2 = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "Address Line 2"}), required=False)
    City = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "City"}), required=False)
    State = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "State"}), required=False)
    ZipCode = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "Zip Code"}), required=False)
    Country = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "Country"}), required=False)

    class Meta:
        model = WebsiteAccounts
        fields = ("Phone_Number", 'Address1', "Address2", "City", "State", "ZipCode", "Country")