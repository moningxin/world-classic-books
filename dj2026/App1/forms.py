from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=15, required=True)
    reading_hobbies = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '例如：科普,文学,工程技术'})
    )

    class Meta:
        model = User
        fields = ['username', 'phone', 'reading_hobbies', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))