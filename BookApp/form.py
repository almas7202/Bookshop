from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
class RegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class CustomerAddressForm(forms.ModelForm): 
    class Meta:
        model=CustomerModel
        fields = ["state", "city", "zipcode","add2", "add1", "mobile", "email", "lname", "fname"][::-1]
        widgets = {
                "fname":forms.TextInput(attrs={'class':'form-control required','placeholder':'* Enter First Name'}),
                "lname":forms.TextInput(attrs={'class':'form-control required','placeholder':'* Enter Last Name'}),
                "email":forms.EmailInput(attrs={'class':'form-control required','placeholder':'* Enter E-mail'}),
                "mobile":forms.TextInput(attrs={'class':'form-control required','placeholder':'* Enter Mobile Number'}),
                "add1":forms.TextInput(attrs={'class':'form-control required','placeholder':'* House Number & Street name '}),
                "add2":forms.TextInput(attrs={'class':'form-control required','placeholder':'* Apartment, Suite, Unit etc.'}), 
                "city":forms.TextInput(attrs={'class':'form-control required','placeholder':'City'}),
                "state":forms.TextInput(attrs={'class':'form-control required','placeholder':'State'}),
                "zipcode":forms.TextInput(attrs={'class':'form-control required','placeholder':'* Enter Zipcode'}),
        }
