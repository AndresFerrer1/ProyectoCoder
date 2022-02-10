from dataclasses import fields
import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from AppCoder.models import Contact

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

class ContactoFormumlario(forms.Form):
    correo = forms.EmailField(required=True)
    nombre= forms.CharField(required=True, max_length=30)
    apellido = forms.CharField(required=True, max_length=30)
    asunto = forms.CharField(required=True, max_length=100)
    mensaje = forms.CharField(widget=forms.Textarea, required=True, max_length=10000)