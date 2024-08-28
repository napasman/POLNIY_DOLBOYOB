from django import forms
from .models import EmailSubscriptions, Post
from django.conf import settings
from django.contrib.auth import get_user_model 


class SubscripeForm(forms.ModelForm):
    email = forms.CharField(label="Email", widget=forms.EmailInput(attrs={'id': 'email', 'class':'form-control','placeholder':"Enter your email", 'name':'email'}),max_length=1028)
  
    class Meta:
        model = EmailSubscriptions
        fields = ('email',)
  
  
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        User = get_user_model()  # Get the user model class
        self.fields['author'].queryset = User.objects.filter(is_superuser=True)
