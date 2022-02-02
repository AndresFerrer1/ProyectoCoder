from django.contrib import admin

from AppCoder.models import * #importamos todo los models

# Register your models here.
# Registramos los modelos

admin.site.register(Curso)

admin.site.register(Estudiante)

admin.site.register(Profesor)

admin.site.register(Entregable)

admin.site.register(Avatar)