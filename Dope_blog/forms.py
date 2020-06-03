from django import forms
from django.forms import ModelForm
from .models import Post, Heading, Subheading, Usercontact, Comment, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True,
                            widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('avatar',)



class CommentForm(forms.ModelForm):
    comment = forms.CharField(label='',widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Text goes here','rows':3,'cols':50}))
    class Meta:
        model = Comment
        fields = ('comment',)

