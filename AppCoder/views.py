from django.shortcuts import render, HttpResponse
from django.http import HttpResponse, request
from AppCoder.forms import CursoFormulario
from AppCoder.models import Curso

# Create your views here.

def crea_curso(req, nombre, camada):

    curso = Curso(nombre=nombre, camada=camada)
    
    curso.save()

    return HttpResponse(f'Se creo el curso de {curso.nombre} con el numero de camada {curso.camada}')

def cursoformulario(req):

    if(req.method == 'POST'):

        mi_formulario = CursoFormulario(req.POST)

        if (mi_formulario.is_valid()):

            data = mi_formulario.cleaned_data
        
            curso = Curso (nombre=data['nombre'], camada=data['camada'])
            curso.save()

            return render(req, 'AppCoder/inicio.html')

    else:

        mi_formulario = CursoFormulario()

    return render(req, 'AppCoder/cursoFormulario.html', {'form': mi_formulario})

def busquedaCamada(req):

    return render(req, 'AppCoder/busquedaCamada.html')

def buscar(req):

    if(req.method == "GET"):

        camada = req.GET["camada"]
        cursos = Curso.objects.filter(camada=camada)

        return render(req, "AppCoder/cursos.html", {"cursos": cursos, "camada": camada})

    else:

        return HttpResponse(f'No enviaste datos')

    # return HttpResponse(f'Estamos buscando los cursos de la camada numero: {req.GET["camada"]}')

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