from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import (
    EspacioTrabajo,
    Tablero,
    Lista,
    Tarjeta,
    Usuario,
    Prioridad,
    HistorialActividad,
)


def inicio(request):
    """
    Vista principal de bienvenida a TaskFlow segun seccion 6 del README.
    Obtiene metricas del sistema y renderiza inicio.html extendiendo base.html.
    """
    total_tableros = Tablero.objects.filter(habilitado=True).count()
    total_listas = Lista.objects.filter(habilitado=True).count()
    total_tarjetas = Tarjeta.objects.filter(habilitado=True).count()
    total_usuarios = Usuario.objects.filter(habilitado=True).count()

    context = {
        'total_tableros': total_tableros,
        'total_listas': total_listas,
        'total_tarjetas': total_tarjetas,
        'total_usuarios': total_usuarios,
    }
    return render(request, 'inicio.html', context)


def lista_tableros(request):
    """
    Vista de listado de tableros organizados por espacios de trabajo.
    """
    espacios = EspacioTrabajo.objects.filter(habilitado=True).prefetch_related('tableros')
    context = {
        'espacios': espacios,
    }
    return render(request, 'tableros.html', context)


def detalle_tablero(request, tablero_id):
    """
    Vista interactiva del tablero Kanban estilo Trello.
    Muestra columnas y tarjetas con sus etiquetas, prioridades y asignados.
    """
    tablero = get_object_or_404(Tablero, id=tablero_id, habilitado=True)
    context = {
        'tablero': tablero,
    }
    return render(request, 'tablero.html', context)


@require_POST
def mover_tarjeta(request, tarjeta_id):
    """
    Mueve una tarjeta de una lista a otra (flujo Kanban).
    """
    tarjeta = get_object_or_404(Tarjeta, id=tarjeta_id)
    nueva_lista_id = request.POST.get('nueva_lista_id')

    if nueva_lista_id:
        nueva_lista = get_object_or_404(Lista, id=nueva_lista_id, tablero=tarjeta.lista.tablero)
        lista_anterior = tarjeta.lista.nombre
        tarjeta.lista = nueva_lista
        tarjeta.save()

        # Registrar en historial de auditoria
        usuario_defecto = tarjeta.creador
        HistorialActividad.objects.create(
            tablero=nueva_lista.tablero,
            tarjeta=tarjeta,
            usuario=usuario_defecto,
            accion="Mover tarjeta",
            detalle=f"Tarjeta '{tarjeta.titulo}' movida desde '{lista_anterior}' a '{nueva_lista.nombre}'."
        )

    return redirect('detalle_tablero', tablero_id=tarjeta.lista.tablero.id)


@require_POST
def crear_tarjeta(request, lista_id):
    """
    Creacion rapida de tarjeta dentro de una lista Kanban.
    """
    lista = get_object_or_404(Lista, id=lista_id)
    titulo = request.POST.get('titulo', '').strip()

    if titulo:
        # Asignar creador por defecto (primer usuario habilitado o creador del tablero)
        creador = lista.tablero.creador
        tarjeta = Tarjeta.objects.create(
            lista=lista,
            titulo=titulo,
            creador=creador,
            posicion=lista.tarjetas.count() + 1
        )
        HistorialActividad.objects.create(
            tablero=lista.tablero,
            tarjeta=tarjeta,
            usuario=creador,
            accion="Crear tarjeta",
            detalle=f"Tarjeta '{titulo}' añadida a la lista '{lista.nombre}'."
        )

    return redirect('detalle_tablero', tablero_id=lista.tablero.id)


def error_404_view(request, exception=None):
    """
    Controlador personalizado de error 404 segun seccion 7 del README.
    """
    return render(request, '404.html', status=404)
