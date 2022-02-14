from re import template
from django.urls import path

from AppCoder import views

from AppCoder.views import Curso, inicio2, leer_cursos, CrearPost

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.inicio, name="Inicio"), #esta era nuestra primer view
    path('cursos/', views.cursos, name="Cursos"),
    path('profesores/', views.profesores, name="Profesores"),
    path('estudiantes/', views.estudiantes, name="Estudiantes"),
    path('entregables/', views.entregables, name="Entregables"),
    path('cursoFormulario/', views.cursoformulario, name="CursoFormulario"),
    path('busquedaCamada/', views.busquedaCamada, name="BusquedaCamada"),
    path('buscar/', views.buscar, name="Buscar"),
    path('buscarn/', views.buscarn, name="Buscarn"),
    path('lista_profesores/', views.leer_profesores, name="lista_profesores"),
    path('agregarProfesores/', views.profesores, name="agregarProfesores"),
    path('eliminarProfesor/<id_profesor>/', views.eliminarProfesor, name="eliminarProfesor"),
    path('editarProfesor/<profesor_nombre>/', views.editarProfesor, name="editarProfesor"),
    path('lista_cursos/', views.leer_cursos, name="lista_cursos"),

    path('listaCursos/', views.CursoList.as_view(), name='List'),
    path('detalleCursos/<pk>/', views.CursoDetail.as_view(), name='Detail'),
    path('crearCursos/', views.CursoCreate.as_view(), name='New'),
    path('actualizarCursos/<pk>/', views.CursoUpdate.as_view(), name='Edit'),
    path('eliminaCursos/<pk>/', views.CursoDelete.as_view(), name='Delete'),

    path('login/', views.login_request, name='Login'),
    path('register/', views.register, name='Register'),
    path('logout/', LogoutView.as_view(template_name="AppCoder/logout.html"), name='Logout'),

    path("editarPerfil/", views.editarPerfil, name='EditarPerfil'),
    path("perfil/", views.perfil, name='Perfil'),
    path('inicio2/', views.inicio2, name="Inicio2"),

    # path('contacto/', views.Contacto.as_view(), name='contacto'),

    path('contacto/', views.VistaContacto, name='contacto'),

    path('crearcontacto/', views.crearContacto.as_view(), name='crearcontacto'),
    path('contacto_gracias/', views.contacto_gracias, name='contacto_gracias'),
    path('actualizarAvatar/<pk>/', views.UpdateAvatar.as_view(), name='actualizarAvatar'),
    path('avatarView/', views.AvatarUserList.as_view(), name='AvatarView'),
    path('crearAvatar/', views.AvatarCreate.as_view(), name='AvatarCreate'),
    path('agregarAvatar/', views.agregarAvatar, name='AgregarAvatar'),

    
    path('listaPost/',views.VistaPost.as_view(), name='listaPost'),
    path('detalle/<int:pk>', views.DetallePost.as_view(), name='DetallePost'),
    path('crearPost/', views.CrearPost.as_view(), name='CrearPost'),
]