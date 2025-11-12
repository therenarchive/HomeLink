from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

INPUT_CLASSES = 'w-full h-10 rounded-lg px-4'

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': INPUT_CLASSES
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'password',
        'class': INPUT_CLASSES
    }))

class SignUpForm(UserCreationForm):

    ACC_TYPE = (
        ('worker','Worker'),
        ('homeowner', 'Homeowner'),
    )

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': INPUT_CLASSES
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email',
        'class': INPUT_CLASSES
    }))
    acc_type = forms.ChoiceField(choices = ACC_TYPE, widget=forms.Select(attrs={
        'class': INPUT_CLASSES
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'password',
        'class': INPUT_CLASSES
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'repeat password',
        'class': INPUT_CLASSES
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'acc_type', 'password1', 'password2')