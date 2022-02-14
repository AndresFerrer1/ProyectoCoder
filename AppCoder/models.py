from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from datetime import datetime, date

# Create your models here.

class Curso(models.Model):

    nombre = models.CharField(max_length=40)
    camada = models.IntegerField()

    def __str__(self):
        return (f'{self.nombre}-{self.camada}')

class Estudiante(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    email = models.EmailField()

class Profesor(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    email = models.EmailField()
    profesion = models.CharField(max_length=30)

    def __str__(self):
        return (f'{self.nombre}-{self.apellido}')

class Entregable(models.Model):
    nombre = models.CharField(max_length=30)
    fechaDeEntrega = models.DateField()
    entregado = models.BooleanField()

class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='avatares', null=True, blank = True)

    def __str__(self):
        return f"Imagen de {self.user.username}"

class Contact(models.Model):
    correo = models.EmailField()
    nombre= models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    asunto = models.CharField(max_length=100)
    mensaje = models.TextField(max_length=10000)

    def __str__(self):
        return self.correo

class Post(models.Model):
    titulo = models.CharField(max_length=255)
    etiqueta_titulo = models.CharField(max_length=255, default="Etiqueta del Post")
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    fecha_post = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titulo + ' | ' + str(self.autor)

    # def get_absolute_url(self):
    #     return reverse('DetallePost', args=(str(self.id)))