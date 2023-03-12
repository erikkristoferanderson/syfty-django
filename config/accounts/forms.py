from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.HiddenInput(), initial='dummypassword')
    password2 = forms.CharField(
        widget=forms.HiddenInput(), initial='dummypassword')

    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_password2(self):
        return 'dummypassword'
