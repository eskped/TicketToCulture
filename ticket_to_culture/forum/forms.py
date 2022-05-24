from dataclasses import field
from email.policy import default
from logging import Filter
from webbrowser import BackgroundBrowser
from wsgiref import validate

from .models import Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post
from django.core.validators import RegexValidator

LOCATION_CHOICES= [
    ('lokasjon', 'Lokasjon'),
    ('bergen', 'Bergen'),
    ('oslo', 'Oslo'),
    ('trondheim', 'Trondheim'),
    ('stavanger', 'Stavanger'),
    ('larvik', 'Larvik'),
    ('sandes', 'Sandes'),
    ('annet', 'Annet'),
    ]

TYPE_CHOICES= [
    ('arrangement', 'Arrangement'),
    ('konsert', 'Konsert'),
    ('teater', 'Teater'),
    ('film', 'Film'),
    ('kunst', 'Kunst'),
    ('karnival', 'Karnival'),
    ('standup', 'Standup'),
    ('annet', 'Annet'),
    ]

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=40, required=True, help_text='Påkrevd.', label="Fornavn")
    last_name = forms.CharField(max_length=40, required=True, help_text='Påkrevd.', label="Etternavn")
    email = forms.EmailField(max_length=255, help_text='Påkrevd. Skriv inn en valid epost addresse.', label="Email")
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone_number = forms.CharField(max_length=11, validators=[phoneNumberRegex], help_text="Valgfritt telefonnummer.", label="Telefonnummer")
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}),
                             help_text="Valgfritt profilbilde.",
                             label="Profilbilde")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2',)


class CreatePostForm(forms.Form):
    # TODO: Gjøre så bruker kan laste opp bilde
    title = forms.CharField(max_length=40, required=True, help_text='En tittel for annonsen', label="Tittel")
    description = forms.CharField(widget=forms.Textarea, help_text='En beskrivelse for annonsen.', label="Beskrivelse")
    is_sale = forms.BooleanField(required=False, help_text="Er annonsen et salg?", initial=True, label="Salgs annonse")
    price = forms.DecimalField(max_digits=16, help_text='Pris for annonsen.', label="Pris")
    image = forms.ImageField(required=False, help_text="Bilde for annonse.", label="Bilde")
    location= forms.CharField(label='Lokasjon', widget=forms.Select(choices=LOCATION_CHOICES), required=True)
    type= forms.CharField(label='Arrangement', widget=forms.Select(choices=TYPE_CHOICES), required=True )
    


    class Meta:
        model = Post
        fields = ('title', 'description', 'is_sale', 'price', 'location', 'type')


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="E-post",
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email']


class UpdateProfileForm(forms.ModelForm):
    image = forms.ImageField(label="Profilbilde",widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone = forms.CharField(label="Telefonnummer",max_length=11, validators=[phoneNumberRegex], required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['image', 'phone']


class FilterPosts(forms.Form):
    priceLowHigh = forms.BooleanField(label='Lav-Høy', required=False)
    for_sale = forms.BooleanField(label='Til salgs', required=False)
    for_buy = forms.BooleanField(label='Ønskes kjøpt', required=False)
    location= forms.CharField(label='Lokasjon', widget=forms.Select(choices=LOCATION_CHOICES), required=False)
    type= forms.CharField(label='Arrangement', widget=forms.Select(choices=TYPE_CHOICES), required=False)
    
        
    class Meta:
        model = Filter
        fields = ['price', 'location', 'for_sale', 'for_buy', 'type']
        
    
    
         
       
