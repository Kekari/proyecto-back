from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('tableros/', views.lista_tableros, name='tableros'),
    path('tablero/<int:tablero_id>/', views.detalle_tablero, name='detalle_tablero'),
    path('tarjeta/<int:tarjeta_id>/mover/', views.mover_tarjeta, name='mover_tarjeta'),
    path('lista/<int:lista_id>/crear-tarjeta/', views.crear_tarjeta, name='crear_tarjeta'),
]
