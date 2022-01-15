from django.shortcuts import render
from django.http import HttpResponse

from AppCoder.models import Curso

# Create your views here.

def crea_curso(req, nombre, camada):

    curso = Curso(nombre=nombre, camada=camada)
    
    curso.save()

    return HttpResponse(f'Se creo el curso de {curso.nombre} con el numero de camada {curso.camada}')

def inicio(req):

    return render(req, 'AppCoder/inicio.html')

def cursos(req):

    lista = Curso.objects.all()

    return render(req, 'AppCoder/cursos.html', {"lista": lista})

def profesores(req):

    return render(req,'AppCoder/profesores.html')

def estudiantes(req):

    return render(req,'AppCoder/estudiantes.html')

def entregables(req):

    return render(req,'AppCoder/entregables.html')