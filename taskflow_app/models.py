from django.db import models

# Constantes de cadenas para campos estándar
str_habilitado = "Habilitado"
str_fecha_creacion = "Fecha Creación"
str_fecha_actualizacion = "Fecha Actualización"
str_codigo = "Código"
str_nombre = "Nombre"
str_descripcion = "Descripción"
str_color = "Color"
str_posicion = "Posición / Orden"
str_icono = "Ícono"
str_rut = "RUT"
str_email = "Correo Electrónico"
str_telefono = "Teléfono"


class Usuario(models.Model):
    nombre = models.CharField(str_nombre, max_length=150, null=False)
    rut = models.CharField(str_rut, max_length=12, null=True, blank=True)
    correo = models.EmailField(str_email, unique=True, null=False)
    telefono = models.CharField(str_telefono, max_length=20, null=True, blank=True)
    cargo = models.CharField("Cargo / Rol", max_length=80, default="Miembro del Equipo")
    color_avatar = models.CharField(str_color, max_length=20, default="#0284c7")
    habilitado = models.BooleanField(str_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table_comment = "Registro de usuarios y perfiles que participan en los tableros de TaskFlow."

    def __str__(self):
        return f"{self.nombre} ({self.correo})"


class EspacioTrabajo(models.Model):
    nombre = models.CharField(str_nombre, max_length=100, null=False)
    descripcion = models.TextField(str_descripcion, null=True, blank=True)
    sitio_web = models.URLField("Sitio Web", null=True, blank=True)
    correo_contacto = models.EmailField(str_email, null=True, blank=True)
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="espacios_creados")
    habilitado = models.BooleanField(str_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    class Meta:
        verbose_name = "Espacio de Trabajo"
        verbose_name_plural = "Espacios de Trabajo"
        db_table_comment = "Espacios de trabajo organizacionales que agrupan múltiples tableros y equipos."

    def __str__(self):
        return self.nombre


class RolColaborador(models.Model):
    codigo = models.CharField(str_codigo, max_length=20, unique=True, null=False)
    nombre = models.CharField(str_nombre, max_length=50, null=False)
    descripcion = models.CharField(str_descripcion, max_length=255, null=True, blank=True)
    habilitado = models.BooleanField(str_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    class Meta:
        verbose_name = "Rol de Colaborador"
        verbose_name_plural = "Roles de Colaboradores"
        db_table_comment = "Roles y niveles de permisos para miembros de espacios y tableros (ADMIN, MIEMBRO, OBSERVADOR)."

    def __str__(self):
        return self.nombre


class MiembroEspacio(models.Model):
    espacio = models.ForeignKey(EspacioTrabajo, on_delete=models.CASCADE, related_name="miembros")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="membresias_espacios")
    rol = models.ForeignKey(RolColaborador, on_delete=models.CASCADE)
    habilitado = models.BooleanField(str_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    class Meta:
        verbose_name = "Miembro de Espacio"
        verbose_name_plural = "Miembros de Espacio"
        unique_together = ('espacio', 'usuario')
        db_table_comment = "Asignación de usuarios a espacios de trabajo con un rol determinado."

    def __str__(self):
        return f"{self.usuario.nombre} - {self.espacio.nombre} ({self.rol.nombre})"


class VisibilidadTablero(models.Model):
    codigo = models.CharField(str_codigo, max_length=20, unique=True, null=False)
    nombre = models.CharField(str_nombre, max_length=50, null=False)
    descripcion = models.CharField(str_descripcion, max_length=255, null=True, blank=True)
    habilitado = models.BooleanField(str_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    class Meta:
        verbose_name = "Visibilidad de Tablero"
        verbose_name_plural = "Visibilidades de Tablero"
        db_table_comment = "Nivel de visibilidad y acceso de un tablero (privado, espacio, público)."

    def __str__(self):
        return self.nombre


class Tablero(models.Model):
    nombre = models.CharField(str_nombre, max_length=120, null=False)
    descripcion = models.TextField(str_descripcion, null=True, blank=True)
    color_fondo = models.CharField("Color de Fondo", max_length=30, default="#0284c7")
    icono = models.CharField(str_icono, max_length=10, default="📋")
    espacio = models.ForeignKey(EspacioTrabajo, on_delete=models.CASCADE, related_name="tableros")
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="tableros_creados")
    visibilidad = models.ForeignKey(VisibilidadTablero, on_delete=models.CASCADE)
    favorito = models.BooleanField("Favorito", default=False)
    habilitado = models.BooleanField(str_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    class Meta:
        verbose_name = "Tablero"
        verbose_name_plural = "Tableros"
        db_table_comment = "Tableros estilo Kanban para gestión visual de proyectos y tareas."

    def __str__(self):
        return self.nombre


class MiembroTablero(models.Model):
    tablero = models.ForeignKey(Tablero, on_delete=models.CASCADE, related_name="miembros")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="tableros_asignados")
    rol = models.ForeignKey(RolColaborador, on_delete=models.CASCADE)
    habilitado = models.BooleanField(str_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    class Meta:
        verbose_name = "Miembro de Tablero"
        verbose_name_plural = "Miembros de Tablero"
        unique_together = ('tablero', 'usuario')
        db_table_comment = "Colaboradores asignados específicamente a un tablero."

    def __str__(self):
        return f"{self.usuario.nombre} en {self.tablero.nombre} ({self.rol.nombre})"


class Lista(models.Model):
    tablero = models.ForeignKey(Tablero, on_delete=models.CASCADE, related_name="listas")
    nombre = models.CharField(str_nombre, max_length=80, null=False)
    posicion = models.IntegerField(str_posicion, default=0, null=False)
    habilitado = models.BooleanField(str_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    class Meta:
        verbose_name = "Lista de Tablero"
        verbose_name_plural = "Listas de Tablero"
        ordering = ['posicion', 'id']
        db_table_comment = "Columnas o listas que representan las etapas del flujo de trabajo (Kanban)."

    def __str__(self):
        return f"{self.tablero.nombre} - {self.nombre}"


class Prioridad(models.Model):
    codigo = models.CharField(str_codigo, max_length=20, unique=True, null=False)
    nombre = models.CharField(str_nombre, max_length=50, null=False)
    color = models.CharField(str_color, max_length=20, default="#10b981")
    nivel = models.IntegerField("Nivel de Urgencia", default=1)
    habilitado = models.BooleanField(str_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    class Meta:
        verbose_name = "Prioridad"
        verbose_name_plural = "Prioridades"
        ordering = ['nivel']
        db_table_comment = "Niveles de prioridad para categorizar la urgencia de cada tarjeta."

    def __str__(self):
        return self.nombre


class Etiqueta(models.Model):
    tablero = models.ForeignKey(Tablero, on_delete=models.CASCADE, related_name="etiquetas")
    nombre = models.CharField(str_nombre, max_length=50, null=False)
    color = models.CharField(str_color, max_length=20, default="#6366f1")
    habilitado = models.BooleanField(str_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"
        db_table_comment = "Etiquetas de color para clasificar tarjetas según temáticas o áreas."

    def __str__(self):
        return f"{self.nombre} ({self.tablero.nombre})"


class Tarjeta(models.Model):
    lista = models.ForeignKey(Lista, on_delete=models.CASCADE, related_name="tarjetas")
    titulo = models.CharField("Título", max_length=200, null=False)
    descripcion = models.TextField(str_descripcion, null=True, blank=True)
    prioridad = models.ForeignKey(Prioridad, on_delete=models.SET_NULL, null=True, blank=True, related_name="tarjetas")
    posicion = models.IntegerField(str_posicion, default=0, null=False)
    fecha_inicio = models.DateField("Fecha Inicio", null=True, blank=True)
    fecha_limite = models.DateField("Fecha Límite / Vencimiento", null=True, blank=True)
    estimacion_horas = models.DecimalField("Estimación en Horas", max_digits=5, decimal_places=2, null=True, blank=True)
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="tarjetas_creadas")
    asignado_a = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name="tarjetas_asignadas")
    completada = models.BooleanField("Completada", default=False)
    habilitado = models.BooleanField(str_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    class Meta:
        verbose_name = "Tarjeta"
        verbose_name_plural = "Tarjetas"
        ordering = ['posicion', 'id']
        db_table_comment = "Tarjetas de trabajo individuales con contenido, responsables y plazos."

    def __str__(self):
        return self.titulo


class TarjetaEtiqueta(models.Model):
    tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE, related_name="asignaciones_etiquetas")
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.CASCADE, related_name="tarjetas_asociadas")
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)

    class Meta:
        verbose_name = "Etiqueta de Tarjeta"
        verbose_name_plural = "Etiquetas de Tarjetas"
        unique_together = ('tarjeta', 'etiqueta')
        db_table_comment = "Relación de asignación entre tarjetas y etiquetas temáticas."

    def __str__(self):
        return f"{self.tarjeta.titulo} - {self.etiqueta.nombre}"


class Checklist(models.Model):
    tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE, related_name="checklists")
    titulo = models.CharField("Título de Checklist", max_length=120, null=False)
    posicion = models.IntegerField(str_posicion, default=0)
    habilitado = models.BooleanField(str_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    class Meta:
        verbose_name = "Checklist"
        verbose_name_plural = "Checklists"
        ordering = ['posicion', 'id']
        db_table_comment = "Listas de comprobación o subtareas asociadas a una tarjeta."

    def __str__(self):
        return f"{self.titulo} ({self.tarjeta.titulo})"


class ItemChecklist(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name="items")
    descripcion = models.CharField(str_descripcion, max_length=255, null=False)
    completado = models.BooleanField("Completado", default=False)
    posicion = models.IntegerField(str_posicion, default=0)
    asignado_a = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    habilitado = models.BooleanField(str_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    class Meta:
        verbose_name = "Item de Checklist"
        verbose_name_plural = "Items de Checklist"
        ordering = ['posicion', 'id']
        db_table_comment = "Elementos individuales o pasos verificables dentro de una checklist."

    def __str__(self):
        estado = "✓" if self.completado else "○"
        return f"[{estado}] {self.descripcion}"


class Comentario(models.Model):
    tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE, related_name="comentarios")
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="comentarios_realizados")
    contenido = models.TextField("Contenido del Comentario", null=False)
    habilitado = models.BooleanField(str_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ['-created_at']
        db_table_comment = "Comentarios y retroalimentación de los usuarios en cada tarjeta."

    def __str__(self):
        return f"{self.autor.nombre}: {self.contenido[:40]}"


class Adjunto(models.Model):
    tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE, related_name="adjuntos")
    nombre_archivo = models.CharField("Nombre del Archivo", max_length=200, null=False)
    url_recurso = models.CharField("URL o Enlace del Recurso", max_length=500, null=False)
    tipo_archivo = models.CharField("Tipo de Archivo", max_length=50, null=True, blank=True)
    tamanio_kb = models.IntegerField("Tamaño en KB", null=True, blank=True)
    subido_por = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="adjuntos_subidos")
    habilitado = models.BooleanField(str_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    class Meta:
        verbose_name = "Adjunto"
        verbose_name_plural = "Adjuntos"
        db_table_comment = "Archivos adjuntos, documentación y enlaces asociados a una tarjeta."

    def __str__(self):
        return self.nombre_archivo


class HistorialActividad(models.Model):
    tablero = models.ForeignKey(Tablero, on_delete=models.CASCADE, related_name="actividades")
    tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE, null=True, blank=True, related_name="actividades")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="actividades_registradas")
    accion = models.CharField("Acción Realizada", max_length=100, null=False)
    detalle = models.TextField("Detalle del Movimiento", null=True, blank=True)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)

    class Meta:
        verbose_name = "Historial de Actividad"
        verbose_name_plural = "Historiales de Actividades"
        ordering = ['-created_at']
        db_table_comment = "Auditoría cronológica de eventos y cambios ocurridos en el tablero."

    def __str__(self):
        return f"{self.usuario.nombre} - {self.accion} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
