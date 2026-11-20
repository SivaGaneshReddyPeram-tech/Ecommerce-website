from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class CheckoutForm(forms.Form):
    recipient_name = forms.CharField(max_length=150)
    phone = forms.CharField(max_length=30)
    delivery_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
