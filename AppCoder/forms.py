from dataclasses import fields
from msilib.schema import Class
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CursoFormulario(forms.Form):

    nombre = forms.CharField()
    camada = forms.IntegerField()

class ProfesorFormulario(forms.Form):

    nombre = forms.CharField(max_length=30)
    apellido = forms.CharField(max_length=30)
    email = forms.EmailField()
    profesion = forms.CharField(max_length=30)

class UserEditForm(UserCreationForm):

    email = forms.EmailField(label="Modificar email")
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir la contraseña", widget=forms.PasswordInput)
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name']
        #Saca los mensajes de ayuda
        help_texts = {k: "" for k in fields}

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    # Configuration
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']