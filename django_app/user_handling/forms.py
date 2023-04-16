from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(AuthenticationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "password")