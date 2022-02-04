from cmath import log
from dataclasses import field
import imp
import re
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.http import HttpResponse, request
from AppCoder.forms import CursoFormulario, ProfesorFormulario, UserEditForm, UserRegisterForm
from AppCoder.models import Avatar, Curso, Profesor
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

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
        nombre = Curso.objects.filter(camada=camada)

        return render(req, "AppCoder/resultadosBusqueda.html", {"nombre": nombre, "camada": camada})

    else:

        return HttpResponse(f'No enviaste datos')

    # return HttpResponse(f'Estamos buscando los cursos de la camada numero: {req.GET["camada"]}')

def inicio(req):
    
    if (req.user.id) == None:

        return render(req, 'AppCoder/inicio.html')

    else:

        avatar = Avatar.objects.filter(user=req.user.id)

        return render(req, 'AppCoder/inicio.html', {"url":avatar[0].imagen.url})

@login_required
def inicio2(req):

    avatar = Avatar.objects.filter(user=req.user.id)  

    return render(req, 'AppCoder/inicio2.html', {"url":avatar[0].imagen.url})

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

@login_required
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

class CursoList(LoginRequiredMixin, ListView):

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
    
def login_request(req):

    if req.method == "POST":
        form = AuthenticationForm(req, data = req.POST)

        if form.is_valid():
            # usuario = form.cleaned_data.get('username')
            # contra = form.cleaned_data.get('password')

            data = form.cleaned_data

            # user = authenticate(username=usuario, password=contra)

            user = authenticate(username=data['username'], password=data['password'])

            if user is not None:
                login(req, user)

                avatar = Avatar.objects.filter(user=req.user.id)                

                return render(req, "AppCoder/Inicio.html", {'mensaje':f'Bienvenido {user.get_username()}', 
                    'url': avatar[0].imagen.url
                })

            else:

                return render(req, "AppCoder/login.html", {'mensaje':f'Falló la autenticación, intentalo de nuevo'})

        else:

            return render(req, "AppCoder/login.html", {'mensaje':f'Error, formulario erroneo'})

    form =AuthenticationForm()

    return render(req, "AppCoder/login.html", {'form':form})

def register(req):

    if req.method == "POST":

        form = UserCreationForm(req.POST)
        #form =UserRegisterForm(req.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            form.save()
            return render(req,"AppCoder/inicio.html", {"mensaje":"Usuario Creado :)"})

    else:

        form = UserCreationForm(req.POST)
        #form =UserRegisterForm(req.POST)

        return render(req, "AppCoder/registro.html", {"form":form})

@login_required
def editarPerfil(req):

    usuario = req.user

    if req.method == "POST":
        miFormulario = UserEditForm(req.POST)
        if miFormulario.is_valid():

            informacion = miFormulario.cleaned_data

            usuario.email = informacion['email']
            usuario.password1 = informacion['password1']
            usuario.password2 = informacion['password2']
            #Si quisiera cambiar el nombre del usuario
            usuario.first_name = informacion['first_name']
            usuario.last_name = informacion['last_name']
            usuario.save()

            return render(req, "AppCoder/inicio.html")

    else:

        miFormulario = UserEditForm(initial={'email': usuario.email})

        return render(req, "AppCoder/editarPerfil.html", {"miFormulario":miFormulario, "usuario":usuario})

@login_required # Require user logged in before they can access profile page
def profile(req):

    avatar = Avatar.objects.filter(user=req.user.id)  

    usuario = req.user

    if (req.method == "POST"):
        miFormulario = UserEditForm(req.POST)
        if miFormulario.is_valid():

            informacion = miFormulario.cleaned_data

            usuario.email = informacion['email']
            usuario.password1 = informacion['password1']
            usuario.password2 = informacion['password2']
            #Si quisiera cambiar el nombre del usuario
            usuario.first_name = informacion['first_name']
            usuario.last_name = informacion['last_name']
            usuario.save()

            return render(req, "AppCoder/profile.html", {"miFormulario":miFormulario, "usuario":usuario, "url":avatar[0].imagen.url})

    else:

        miFormulario = UserEditForm(initial={'email': usuario.email})

        return render(req, 'AppCoder/profile.html', {"miFormulario":miFormulario, "usuario":usuario, "url":avatar[0].imagen.url})