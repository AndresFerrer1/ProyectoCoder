from asyncio.windows_events import NULL
from cmath import log
from dataclasses import field
import imp
from pyexpat import model
from queue import Empty
import re
from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse, request
from AppCoder.forms import AvatarFormulario, ContactoFormumlario, CursoFormulario, ProfesorFormulario, UserEditForm
from AppCoder.models import Avatar, Contact, Curso, Post, Profesor
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views import generic

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

    avatar = Avatar.objects.filter(user=req.user.id)

    try:
        return render(req, 'AppCoder/busquedaCamada.html', {"url":avatar[0].imagen.url})
    except:
        return render(req, 'AppCoder/busquedaCamada.html', {"url":""})

def buscar(req):

    avatar = Avatar.objects.filter(user=req.user.id)

    if(req.method == "GET"):

        camada = req.GET["camada"]
        nombre = Curso.objects.filter(camada=camada)

        try:
            return render(req, 'AppCoder/resultadosBusqueda.html', {"nombre": nombre, "camada": camada,"url":avatar[0].imagen.url})
        except:
            return render(req, 'AppCoder/resultadosBusqueda.html', {"nombre": nombre, "camada": camada,"url":""})

        # return render(req, "AppCoder/resultadosBusqueda.html", {"nombre": nombre, "camada": camada})

    else:

        return HttpResponse(f'No enviaste datos')

def buscarn(req):

    avatar = Avatar.objects.filter(user=req.user.id)

    if(req.method == "GET"):

        nombre = req.GET["nombre"]
        camada = Curso.objects.filter(nombre=nombre)

        try:
            return render(req, 'AppCoder/resultadosBusquedan.html', {"nombre": nombre, "camada": camada,"url":avatar[0].imagen.url})
        except:
            return render(req, 'AppCoder/resultadosBusquedan.html', {"nombre": nombre, "camada": camada,"url":""})

        # return render(req, "AppCoder/resultadosBusquedan.html", {"nombre": nombre, "camada": camada})

    else:

        return HttpResponse(f'No enviaste datos')

    # return HttpResponse(f'Estamos buscando los cursos de la camada numero: {req.GET["camada"]}')

def inicio(req):

    avatar = Avatar.objects.filter(user=req.user.id) 

    try:
        return render(req, 'AppCoder/inicio.html', {"url":avatar[0].imagen.url})
    except:
        return render(req, 'AppCoder/inicio.html', {"url":""})

@login_required
def inicio2(request):

    avatar = Avatar.objects.filter(user=request.user.id)  

    return render(request, 'AppCoder/inicio2.html', {"url":avatar[0].imagen.url})

def cursos(req):

    lista = Curso.objects.all()

    return render(req, 'AppCoder/cursoFormulario.html', {"lista": lista})

def leer_cursos(req):

    avatar = Avatar.objects.filter(user=req.user.id)

    curso = Curso.objects.all()

    try:
        return render(req, 'AppCoder/cursos.html', {"curso": curso,"url":avatar[0].imagen.url})
    except:
        return render(req, 'AppCoder/cursos.html', {"curso": curso,"url":""})

    # return render(req, 'AppCoder/cursos.html', {"curso": curso})

def estudiantes(req):

    avatar = Avatar.objects.filter(user=req.user.id)

    try:
        return render(req, 'AppCoder/estudiantes.html', {"url":avatar[0].imagen.url})
    except:
        return render(req, 'AppCoder/estudiantes.html', {"url":""})

    # return render(req,'AppCoder/estudiantes.html')

def entregables(req):

    avatar = Avatar.objects.filter(user=req.user.id)

    try:
        return render(req, 'AppCoder/entregables.html', {"url":avatar[0].imagen.url})
    except:
        return render(req, 'AppCoder/entregables.html', {"url":""})

    # return render(req,'AppCoder/entregables.html')

@login_required
def leer_profesores(req):

    profesores = Profesor.objects.all()

    avatar = Avatar.objects.filter(user=req.user.id)

    try:
        return render(req, 'AppCoder/lista_profesores.html', {"profesores": profesores, "url":avatar[0].imagen.url})
    except:
        return render(req, 'AppCoder/lista_profesores.html', {"profesores": profesores, "url":""})

    # return render(req, 'AppCoder/lista_profesores.html', {"profesores": profesores})

def eliminarProfesor(req, id_profesor):

    profesor = Profesor.objects.get(id=id_profesor)
    profesor.delete()
      
    #vuelvo al menú
    profesores = Profesor.objects.all() #trae todos los profesores

    avatar = Avatar.objects.filter(user=req.user.id)

    try:
        return render(req, 'AppCoder/lista_profesores.html', {"profesores": profesores, "url":avatar[0].imagen.url})
    except:
        return render(req, 'AppCoder/lista_profesores.html', {"profesores": profesores, "url":""})

    # return render(req, "AppCoder/lista_profesores.html", {"profesores":profesores})

def profesores(req):

    avatar = Avatar.objects.filter(user=req.user.id)

    if(req.method == "POST"):

        mi_formulario = ProfesorFormulario(req.POST)

        if (mi_formulario.is_valid()):

            data = mi_formulario.cleaned_data
        
            profesor = Profesor (nombre=data['nombre'], apellido=data['apellido'], email=data['email'], profesion=data['profesion'])
            profesor.save()

            try:
                return render(req, 'AppCoder/inicio.html', {"url":avatar[0].imagen.url})
            except:
                return render(req, 'AppCoder/inicio.html', {"url":""})

            # return render(req, 'AppCoder/inicio.html')

    else:

        mi_formulario = ProfesorFormulario()

        try:
            return render(req, 'AppCoder/profesores.html', {'form': mi_formulario, "url":avatar[0].imagen.url})
        except:
            return render(req, 'AppCoder/profesores.html', {'form': mi_formulario, "url":""})

        # return render(req, 'AppCoder/profesores.html', {'form': mi_formulario})

def editarProfesor(req, profesor_nombre):

    avatar = Avatar.objects.filter(user=req.user.id)

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

            try:
                return render(req, 'AppCoder/inicio.html', {"url":avatar[0].imagen.url})
            except:
                return render(req, 'AppCoder/inicio.html', {"url":""})

            # return render(req, "AppCoder/inicio.html") #Vuelvo al inicio o a donde quieran
      #En caso que no sea post
    else: 
            #Creo el formulario con los datos que voy a modificar
        miFormulario= ProfesorFormulario(initial={'nombre': profesor.nombre, 'apellido':profesor.apellido, 
        'email':profesor.email, 'profesion':profesor.profesion}) 

      #Voy al html que me permite editar

        try:
            return render(req, 'AppCoder/editarProfesor.html', {"miFormulario":miFormulario, "profesor_nombre":profesor_nombre,"url":avatar[0].imagen.url})
        except:
            return render(req, 'AppCoder/editarProfesor.html', {"miFormulario":miFormulario, "profesor_nombre":profesor_nombre,"url":""})
        
        # return render(req, "AppCoder/editarProfesor.html", {"miFormulario":miFormulario, "profesor_nombre":profesor_nombre})

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

                try:
                    return render(req, 'AppCoder/inicio.html', {'mensaje':f'Bienvenido {user.get_username()}',"url":avatar[0].imagen.url})
                except:
                    return render(req, 'AppCoder/inicio.html', {'mensaje':f'Bienvenido {user.get_username()}',"url":""})     

                # return render(req, "AppCoder/inicio.html", {'mensaje':f'Bienvenido {user.get_username()}'})

            else:

                return render(req, "AppCoder/login.html", {'mensaje':f'Falló la autenticación, intentalo de nuevo', 'form':form})

        else:

            return render(req, "AppCoder/login.html", {'mensaje':f'Error, formulario erroneo','form':form})

    form =AuthenticationForm()

    return render(req, "AppCoder/login.html", {'form':form})

def register(req):

    if req.method == "POST":

        form = UserCreationForm(req.POST)
        # form2 =AvatarFormulario(req.POST, req.FILES)
        if form.is_valid():

            username = form.cleaned_data['username']
            # imagen = form.cleaned_data['imagen']
            form.save()
            return render(req,"AppCoder/inicio.html", {"mensaje":"Usuario Creado, crea un avatar :)"})

    else:

        form = UserCreationForm()
        # form2 =AvatarFormulario()

        return render(req, "AppCoder/registro.html", {"form":form})

@login_required
def editarPerfil(req):

    avatar = Avatar.objects.filter(user=req.user.id)  

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

            return render(req, "AppCoder/inicio.html", {'url': avatar[0].imagen.url, 'url':avatar})

    else:

        miFormulario = UserEditForm(initial={'email': usuario.email})

        try:
            return render(req, 'AppCoder/editarPerfil.html', {"miFormulario":miFormulario, "usuario":usuario,"url":avatar[0].imagen.url})
        except:
            return render(req, 'AppCoder/editarPerfil.html', {"miFormulario":miFormulario, "usuario":usuario,"url":""})   

        # return render(req, "AppCoder/editarPerfil.html", {"miFormulario":miFormulario, "usuario":usuario})

@login_required
def perfil(req):

    avatar = Avatar.objects.filter(user=req.user.id)

    try:
        return render(req, 'AppCoder/perfil.html', {"url":avatar[0].imagen.url})
    except:
        return render(req, 'AppCoder/perfil.html', {"url":""})

    # if avatar == "":

    #     return render(req,'AppCoder/perfil.html', {'url': 'AppCoder/assets/img/user.jpg'})

    # else:

    #     return render(req,'AppCoder/perfil.html', {'url': avatar[0].imagen.url})

def contacto_gracias(req):

    avatar = Avatar.objects.filter(user=req.user.id)

    mensaje1 = f'Gracias por enviarnos tu consulta. Nos pondremos en contacto a la brevedad'

    try:
        return render(req, 'AppCoder/contacto_gracias.html', {'mensaje1':mensaje1,"url":avatar[0].imagen.url})
    except:
        return render(req, 'AppCoder/contacto_gracias.html', {'mensaje1':mensaje1,"url":""})

    # if req.user.id == None:

    #     return render(req, 'AppCoder/contacto_gracias.html', {'mensaje1':mensaje1})

    # else:

    #     return render(req, 'AppCoder/contacto_gracias.html', {'mensaje1':mensaje1, "url":avatar[0].imagen.url})

def VistaContacto(req):

    mensaje1 = f'Gracias por enviarnos tu consulta. Nos pondremos en contacto a la brevedad'

    avatar = Avatar.objects.filter(user=req.user.id)

    form = ContactoFormumlario()

    if req.method == 'POST':
        form = ContactoFormumlario(req.POST)
        if form.is_valid():
            asunto = form.cleaned_data['asunto']
            correo = form.cleaned_data['correo']
            mensaje = form.cleaned_data['mensaje']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            try:
                send_mail(asunto, mensaje, correo, ['admin@example.com'], nombre, apellido)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            
            try:
                return render(req, 'AppCoder/contacto_gracias.html', {'mensaje1':mensaje1,"url":avatar[0].imagen.url})
            except:
                return render(req, 'AppCoder/contacto_gracias.html', {'mensaje1':mensaje1,"url":""})
            
            # return render(req, 'AppCoder/contacto_gracias.html', {'mensaje1':mensaje1})

    else:

        try:
            return render(req, 'AppCoder/email.html', {'form': form,"url":avatar[0].imagen.url})
        except:
            return render(req, 'AppCoder/email.html', {'form': form,"url":""})

        # return render(req, "AppCoder/email.html", {'form': form,})

class crearContacto(CreateView):
    model = Contact
    fields = ['correo', 'nombre', 'apellido', 'asunto', 'mensaje']
    success_url = "/AppCoder/contacto_gracias"

class AvatarUserList(LoginRequiredMixin, ListView):

    model = Avatar
    template_name = "AppCoder/avatar_list.html"

class UpdateAvatar(LoginRequiredMixin, UpdateView):

    model = Avatar
    success_url = "/AppCoder/avatarView"
    fields = ['user','imagen']  

class AvatarCreate(CreateView):
    model = Avatar
    fields = ['user', 'imagen']
    success_url = "/AppCoder/avatarView"

class AvatarDelete(LoginRequiredMixin, DeleteView):
    model = Avatar
    success_url = "/AppCoder/avatarView"
    template_name = "AppCoder/avatar_confirm_delete.html"

@login_required
def agregarAvatar(req):

    avatar = Avatar.objects.filter(user=req.user.id)

    if req.method == "POST":
        miFormulario = AvatarFormulario(req.POST, req.FILES)
        if miFormulario.is_valid():

            u = User.objects.get(username=req.user)
            avatar = Avatar (user=u, imagen=miFormulario.cleaned_data['imagen'])

            avatar.save()

        try:
            return render(req, 'AppCoder/inicio.html', {'mensaje':f'Avatar actualizado',"url":avatar[0].imagen.url})
        except:
            return render(req, 'AppCoder/inicio.html', {'mensaje':f'Avatar actualizado',"url":""})

            # return render(req, 'AppCoder/inicio.html', {'mensaje':f'Avatar actualizado'})

    else:

        miFormulario = AvatarFormulario()

        try:
            return render(req, 'AppCoder/agregarAvatar.html', {'miFormulario':miFormulario, "url":avatar[0].imagen.url})
        except:
            return render(req, 'AppCoder/agregarAvatar.html', {'miFormulario':miFormulario,"url":""})

    # return render(req, "AppCoder/agregarAvatar.html", {"miFormulario":miFormulario})

# def indice(req):

#     return render(req, 'AppCoder/indice.html',{})

class VistaPost(ListView):
    model = Post
    template_name = 'AppCoder/listaPost.html'
    ordering = ['fecha_post']
    # ordering = ['-id']

class DetallePost(DetailView):
    model = Post
    template_name = 'AppCoder/detallePost.html'

class CrearPost(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['titulo', 'etiqueta_titulo', 'autor', 'body', 'imagen']
    success_url = "/AppCoder/listaPost"

class ActualizarPost(LoginRequiredMixin, UpdateView):

    model = Post
    success_url = "/AppCoder/listaPost"
    fields = ['titulo', 'etiqueta_titulo', 'body', 'imagen']

class BorrarPost(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = "/AppCoder/listaPost"
    template_name = "AppCoder/post_confirm_delete.html"