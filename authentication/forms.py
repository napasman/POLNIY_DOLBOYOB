
"""
authentication forms
"""

import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.core.validators import EmailValidator, URLValidator
from django.core.exceptions import ValidationError
from .models import User, Notification
from django.contrib.auth import get_user_model 



class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form
    """
    class Meta(UserCreationForm):
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    """
    Custom user change form
    """
    class Meta:
        model = User
        fields = ('email',)
        
class RegistrationForm(CustomUserCreationForm):
    """
    registration form
    """
    email = forms.CharField(label="Email", widget=forms.EmailInput(attrs={'id': 'email', 'class':'form-control',
                                                                          'placeholder':"name@email.com", 'name':'email'}),
                            max_length=125)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'sign-in-password','class':'form-control',
                                                                 'placeholder':"Enter your password", 'name':'password1'}))
    
    password2 = None
    class Meta:
        model = User
        fields = ("email", "password1" )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        if commit:
            user.save()
        return user



class LoginForm(forms.Form):
    email = forms.CharField(label="Email", widget=forms.EmailInput(attrs={'id': 'email', 'class':'form-control',
                                                                          'placeholder':"name@email.com", 'name':'email'}),
                            max_length=125)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'sign-in-password','class':'form-control',
                                                                 'placeholder':"Enter your password", 'name':'password'}))


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        User = get_user_model()  # Get the user model class
        self.fields['sender'].queryset = User.objects.filter(is_superuser=True)
