from dataclasses import field
import imp
from django.shortcuts import render, HttpResponse
from django.http import HttpResponse, request
from AppCoder.forms import CursoFormulario, ProfesorFormulario
from AppCoder.models import Curso, Profesor
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


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

    return render(req, 'AppCoder/cursoFormulario.html', {"lista": lista})

def leer_cursos(req):

    curso = Curso.objects.all()

    return render(req, 'AppCoder/cursos.html', {"curso": curso})

def estudiantes(req):

    return render(req,'AppCoder/estudiantes.html')

def entregables(req):

    return render(req,'AppCoder/entregables.html')

def leer_profesores(req):

    profesores = Profesor.objects.all()

    return render(req, 'AppCoder/lista_profesores.html', {"profesores": profesores})

def eliminarProfesor(req, id_profesor):

    profesor = Profesor.objects.get(id=id_profesor)
    profesor.delete()
      
    #vuelvo al menú
    profesores = Profesor.objects.all() #trae todos los profesores

    return render(req, "AppCoder/lista_profesores.html", {"profesores":profesores})

def profesores(req):

    if(req.method == "POST"):

        mi_formulario = ProfesorFormulario(req.POST)

        if (mi_formulario.is_valid()):

            data = mi_formulario.cleaned_data
        
            profesor = Profesor (nombre=data['nombre'], apellido=data['apellido'], email=data['email'], profesion=data['profesion'])
            profesor.save()

            return render(req, 'AppCoder/inicio.html')

    else:

        mi_formulario = ProfesorFormulario()

        return render(req, 'AppCoder/profesores.html', {'form': mi_formulario})

def editarProfesor(req, profesor_nombre):

    #Recibe el nombre del profesor que vamos a modificar
    profesor = Profesor.objects.get(nombre=profesor_nombre)

    #Si es metodo POST hago lo mismo que el agregar
    if req.method == 'POST':

        miFormulario = ProfesorFormulario(req.POST) #aquí mellega toda la información del html

        print(miFormulario)

        if miFormulario.is_valid:   #Si pasó la validación de Django

            informacion = miFormulario.cleaned_data

            profesor.nombre = informacion['nombre']
            profesor.apellido = informacion['apellido']
            profesor.email = informacion['email']
            profesor.profesion = informacion['profesion']

            profesor.save()

            return render(req, "AppCoder/inicio.html") #Vuelvo al inicio o a donde quieran
      #En caso que no sea post
    else: 
            #Creo el formulario con los datos que voy a modificar
        miFormulario= ProfesorFormulario(initial={'nombre': profesor.nombre, 'apellido':profesor.apellido, 
        'email':profesor.email, 'profesion':profesor.profesion}) 

      #Voy al html que me permite editar
    return render(req, "AppCoder/editarProfesor.html", {"miFormulario":miFormulario, "profesor_nombre":profesor_nombre})

class CursoList(ListView):

    model = Curso
    template_name = "AppCoder/curso_list.html"

class CursoDetail(DetailView):

    model = Curso
    template_name = "AppCoder/curso_detalle.html"

class CursoUpdate(UpdateView):

    model = Curso
    success_url = "/AppCoder/listaCursos"
    fields = ['nombre', 'camada']
    

class CursoDelete(DeleteView):
    model = Curso
    success_url = "/AppCoder/listaCursos"
    template_name = "AppCoder/curso_confirm_delete.html"

class CursoCreate(CreateView):
    model = Curso
    fields = ['nombre', 'camada']
    success_url = "/AppCoder/listaCursos"
    