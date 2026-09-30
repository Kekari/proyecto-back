"""
URL configuration for core project (TaskFlow).

Configuracion de rutas principales segun README:
- Panel Administrador de Django (/admin/)
- Rutas de la aplicacion TaskFlow ('')
- Manejador de error 404 personalizado (handler404)
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('taskflow_app.urls')),
]

# Vista personalizada para error 404 segun seccion 7 de la guia
handler404 = 'taskflow_app.views.error_404_view'
