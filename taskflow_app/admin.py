from django.contrib import admin
from .models import (
    Usuario,
    EspacioTrabajo,
    RolColaborador,
    MiembroEspacio,
    VisibilidadTablero,
    Tablero,
    MiembroTablero,
    Lista,
    Prioridad,
    Etiqueta,
    Tarjeta,
    TarjetaEtiqueta,
    Checklist,
    ItemChecklist,
    Comentario,
    Adjunto,
    HistorialActividad,
)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'rut', 'cargo', 'habilitado', 'created_at')
    search_fields = ('nombre', 'correo', 'rut', 'cargo')
    list_filter = ('habilitado', 'cargo')


@admin.register(EspacioTrabajo)
class EspacioTrabajoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'creador', 'correo_contacto', 'habilitado', 'created_at')
    search_fields = ('nombre', 'creador__nombre', 'descripcion')
    list_filter = ('habilitado',)


@admin.register(RolColaborador)
class RolColaboradorAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'descripcion', 'habilitado')
    search_fields = ('codigo', 'nombre')


@admin.register(MiembroEspacio)
class MiembroEspacioAdmin(admin.ModelAdmin):
    list_display = ('espacio', 'usuario', 'rol', 'habilitado', 'created_at')
    list_filter = ('rol', 'habilitado')
    search_fields = ('espacio__nombre', 'usuario__nombre')


@admin.register(VisibilidadTablero)
class VisibilidadTableroAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'habilitado')


@admin.register(Tablero)
class TableroAdmin(admin.ModelAdmin):
    list_display = ('icono', 'nombre', 'espacio', 'creador', 'visibilidad', 'favorito', 'habilitado', 'created_at')
    list_filter = ('visibilidad', 'favorito', 'habilitado')
    search_fields = ('nombre', 'espacio__nombre', 'creador__nombre')


@admin.register(MiembroTablero)
class MiembroTableroAdmin(admin.ModelAdmin):
    list_display = ('tablero', 'usuario', 'rol', 'habilitado')
    list_filter = ('rol', 'habilitado')
    search_fields = ('tablero__nombre', 'usuario__nombre')


@admin.register(Lista)
class ListaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tablero', 'posicion', 'habilitado', 'created_at')
    list_filter = ('habilitado', 'tablero')
    search_fields = ('nombre', 'tablero__nombre')


@admin.register(Prioridad)
class PrioridadAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'color', 'nivel', 'habilitado')
    ordering = ('nivel',)


@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'color', 'tablero', 'habilitado')
    list_filter = ('tablero', 'habilitado')
    search_fields = ('nombre', 'tablero__nombre')


class TarjetaEtiquetaInline(admin.TabularInline):
    model = TarjetaEtiqueta
    extra = 1


class ChecklistInline(admin.StackedInline):
    model = Checklist
    extra = 0


@admin.register(Tarjeta)
class TarjetaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'lista', 'prioridad', 'asignado_a', 'fecha_limite', 'completada', 'habilitado')
    list_filter = ('completada', 'prioridad', 'habilitado', 'lista__tablero')
    search_fields = ('titulo', 'descripcion', 'asignado_a__nombre')
    inlines = [TarjetaEtiquetaInline, ChecklistInline]


@admin.register(TarjetaEtiqueta)
class TarjetaEtiquetaAdmin(admin.ModelAdmin):
    list_display = ('tarjeta', 'etiqueta', 'created_at')


@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tarjeta', 'posicion', 'habilitado')


@admin.register(ItemChecklist)
class ItemChecklistAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'checklist', 'completado', 'asignado_a')
    list_filter = ('completado', 'habilitado')


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor', 'tarjeta', 'created_at')
    search_fields = ('contenido', 'autor__nombre', 'tarjeta__titulo')


@admin.register(Adjunto)
class AdjuntoAdmin(admin.ModelAdmin):
    list_display = ('nombre_archivo', 'tarjeta', 'tipo_archivo', 'subido_por', 'created_at')


@admin.register(HistorialActividad)
class HistorialActividadAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'accion', 'tablero', 'tarjeta', 'created_at')
    list_filter = ('accion', 'tablero')
    search_fields = ('accion', 'detalle', 'usuario__nombre')
