from django.core.management.base import BaseCommand
from datetime import date, timedelta
from taskflow_app.models import (
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
    HistorialActividad,
)


class Command(BaseCommand):
    help = "Puebla la base de datos con información inicial de demostración para TaskFlow"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Iniciando carga de datos iniciales para TaskFlow..."))

        # 1. Roles de Colaborador
        roles_data = [
            ("ADMIN", "Administrador", "Control total del espacio o tablero"),
            ("MIEMBRO", "Miembro Regular", "Puede crear, editar y mover tarjetas"),
            ("OBSERVADOR", "Observador", "Solo permisos de lectura"),
        ]
        roles = {}
        for cod, nom, desc in roles_data:
            obj, _ = RolColaborador.objects.get_or_create(
                codigo=cod,
                defaults={"nombre": nom, "descripcion": desc}
            )
            roles[cod] = obj

        # 2. Visibilidad de Tableros
        vis_data = [
            ("PRIVADO", "Privado", "Visible únicamente por los miembros asignados"),
            ("ESPACIO", "Espacio de Trabajo", "Visible por todos los miembros del espacio"),
            ("PUBLICO", "Público", "Cualquiera con el enlace puede visualizar"),
        ]
        visibilidades = {}
        for cod, nom, desc in vis_data:
            obj, _ = VisibilidadTablero.objects.get_or_create(
                codigo=cod,
                defaults={"nombre": nom, "descripcion": desc}
            )
            visibilidades[cod] = obj

        # 3. Niveles de Prioridad
        prioridades_data = [
            ("BAJA", "Baja", "#10b981", 1),
            ("MEDIA", "Media", "#3b82f6", 2),
            ("ALTA", "Alta", "#f59e0b", 3),
            ("URGENTE", "Crítica / Urgente", "#ef4444", 4),
        ]
        prioridades = {}
        for cod, nom, col, niv in prioridades_data:
            obj, _ = Prioridad.objects.get_or_create(
                codigo=cod,
                defaults={"nombre": nom, "color": col, "nivel": niv}
            )
            prioridades[cod] = obj

        # 4. Usuarios
        usuarios_data = [
            ("Kekari", "19.876.543-2", "kekari@taskflow.local", "+56911223344", "Lead Developer", "#0284c7"),
            ("Camila Soto", "18.765.432-1", "camila.soto@taskflow.local", "+56922334455", "Product Owner", "#8b5cf6"),
            ("Rodrigo Araya", "17.654.321-0", "rodrigo.araya@taskflow.local", "+56933445566", "Frontend UI Engineer", "#ec4899"),
            ("Valentina Silva", "20.123.456-7", "valentina.silva@taskflow.local", "+56944556677", "QA & Testing Specialist", "#10b981"),
            ("Erick Bailey", "15.432.109-8", "profesor.bailey@taskflow.local", "+56955667788", "Docente & Mentor Backend", "#f59e0b"),
        ]
        usuarios = {}
        for nom, rut, mail, tel, car, col in usuarios_data:
            obj, _ = Usuario.objects.get_or_create(
                correo=mail,
                defaults={
                    "nombre": nom,
                    "rut": rut,
                    "telefono": tel,
                    "cargo": car,
                    "color_avatar": col
                }
            )
            usuarios[nom] = obj

        u_kekari = usuarios["Kekari"]
        u_camila = usuarios["Camila Soto"]
        u_rodrigo = usuarios["Rodrigo Araya"]
        u_valentina = usuarios["Valentina Silva"]

        # 5. Espacio de Trabajo
        espacio, _ = EspacioTrabajo.objects.get_or_create(
            nombre="Ingeniería & Desarrollo de Software",
            defaults={
                "descripcion": "Espacio de trabajo para el desarrollo del producto TaskFlow y aplicaciones web.",
                "sitio_web": "https://taskflow.local",
                "correo_contacto": "contacto@taskflow.local",
                "creador": u_kekari
            }
        )

        # Miembros del espacio
        for u in [u_kekari, u_camila, u_rodrigo, u_valentina]:
            MiembroEspacio.objects.get_or_create(
                espacio=espacio,
                usuario=u,
                defaults={"rol": roles["ADMIN"] if u == u_kekari else roles["MIEMBRO"]}
            )

        # 6. Tablero Principal: Sprint 1 - Lanzamiento TaskFlow
        tablero1, _ = Tablero.objects.get_or_create(
            nombre="Sprint 1: Lanzamiento TaskFlow",
            espacio=espacio,
            defaults={
                "descripcion": "Gestión del MVP de la plataforma TaskFlow con integración de Django y vistas Kanban.",
                "color_fondo": "#0284c7",
                "icono": "🚀",
                "creador": u_kekari,
                "visibilidad": visibilidades["ESPACIO"],
                "favorito": True
            }
        )

        # Tablero Secundario: Diseño UI/UX
        tablero2, _ = Tablero.objects.get_or_create(
            nombre="Diseño UI/UX y Experiencia de Usuario",
            espacio=espacio,
            defaults={
                "descripcion": "Investigación, wireframes y componentes visuales para el diseño web responsive.",
                "color_fondo": "#7c3aed",
                "icono": "🎨",
                "creador": u_rodrigo,
                "visibilidad": visibilidades["ESPACIO"],
                "favorito": False
            }
        )

        # 7. Listas para el Tablero 1
        listas_tablero1 = [
            ("📌 Por Hacer", 1),
            ("⚡ En Progreso", 2),
            ("👀 En Revisión", 3),
            ("✅ Finalizado", 4),
        ]
        columnas1 = {}
        for nom, pos in listas_tablero1:
            col, _ = Lista.objects.get_or_create(
                tablero=tablero1,
                nombre=nom,
                defaults={"posicion": pos}
            )
            columnas1[nom] = col

        # Listas para Tablero 2
        listas_tablero2 = [
            ("💡 Ideas & Backlog", 1),
            ("🎨 Prototipado", 2),
            ("🧪 Pruebas de Usabilidad", 3),
            ("🚀 Aprobado para Dev", 4),
        ]
        for nom, pos in listas_tablero2:
            Lista.objects.get_or_create(
                tablero=tablero2,
                nombre=nom,
                defaults={"posicion": pos}
            )

        # 8. Etiquetas
        etiquetas_data = [
            ("Backend", "#0284c7"),
            ("Frontend", "#06b6d4"),
            ("Base de Datos", "#8b5cf6"),
            ("Seguridad", "#ef4444"),
            ("Documentación", "#10b981"),
            ("Bugfix", "#f97316"),
        ]
        etiquetas = {}
        for nom, col in etiquetas_data:
            tag, _ = Etiqueta.objects.get_or_create(
                tablero=tablero1,
                nombre=nom,
                defaults={"color": col}
            )
            etiquetas[nom] = tag

        # 9. Tarjetas de Ejemplo en Tablero 1
        tarjetas_data = [
            # Por hacer
            (columnas1["📌 Por Hacer"], "Desplegar servidor en producción", "Configurar Nginx, Gunicorn y variables de entorno.", prioridades["ALTA"], u_kekari, u_kekari, date.today() + timedelta(days=5), 8.0, ["Backend", "Seguridad"]),
            (columnas1["📌 Por Hacer"], "Crear pruebas unitarias en tests.py", "Diseñar pruebas para los modelos de datos y las vistas principales.", prioridades["MEDIA"], u_camila, u_valentina, date.today() + timedelta(days=7), 4.5, ["Documentación"]),

            # En progreso
            (columnas1["⚡ En Progreso"], "Integrar vistas interactivas Kanban", "Crear las plantillas HTML con soporte para mover tarjetas entre columnas.", prioridades["URGENTE"], u_kekari, u_rodrigo, date.today() + timedelta(days=2), 6.0, ["Frontend", "Backend"]),
            (columnas1["⚡ En Progreso"], "Completar README con pauta docente", "Documentar pasos de instalación, ambiente virtual y configuración .env.", prioridades["MEDIA"], u_kekari, u_kekari, date.today() + timedelta(days=1), 2.0, ["Documentación"]),

            # En revision
            (columnas1["👀 En Revisión"], "Verificar manejo de error 404 personalizado", "Asegurar que al ingresar a rutas inexistentes cargue la plantilla 404.html.", prioridades["BAJA"], u_kekari, u_valentina, date.today() + timedelta(days=3), 1.5, ["Seguridad"]),

            # Finalizado
            (columnas1["✅ Finalizado"], "Creación del ambiente virtual venv", "Configuración de Python 3.14 y aislamiento de paquetes.", prioridades["BAJA"], u_kekari, u_kekari, date.today() - timedelta(days=1), 1.0, ["Backend"]),
            (columnas1["✅ Finalizado"], "Modelos de Datos con ORM de Django", "Definición de 17 entidades con comentarios y relaciones referenciales.", prioridades["ALTA"], u_kekari, u_kekari, date.today() - timedelta(days=1), 5.0, ["Base de Datos", "Backend"]),
            (columnas1["✅ Finalizado"], "Desacoplar secretos con python-decouple", "Manejo seguro de SECRET_KEY y credenciales en archivo .env.", prioridades["URGENTE"], u_kekari, u_kekari, date.today() - timedelta(days=1), 2.0, ["Seguridad"]),
        ]

        for col, tit, desc, prio, creador, asignado, fecha, est, tags in tarjetas_data:
            card, created = Tarjeta.objects.get_or_create(
                lista=col,
                titulo=tit,
                defaults={
                    "descripcion": desc,
                    "prioridad": prio,
                    "creador": creador,
                    "asignado_a": asignado,
                    "fecha_limite": fecha,
                    "estimacion_horas": est,
                    "completada": (col.nombre == "✅ Finalizado")
                }
            )
            if created:
                for tname in tags:
                    if tname in etiquetas:
                        TarjetaEtiqueta.objects.create(tarjeta=card, etiqueta=etiquetas[tname])

        # 10. Checklists para la tarjeta de integración
        card_integ = Tarjeta.objects.filter(titulo__contains="Integrar vistas interactivas").first()
        if card_integ:
            chk, _ = Checklist.objects.get_or_create(
                tarjeta=card_integ,
                titulo="Checklist de Implementación",
                defaults={"posicion": 1}
            )
            ItemChecklist.objects.get_or_create(checklist=chk, descripcion="Diseño responsive de columnas", defaults={"completado": True})
            ItemChecklist.objects.get_or_create(checklist=chk, descripcion="Formulario de adición rápida de tarjeta", defaults={"completado": True})
            ItemChecklist.objects.get_or_create(checklist=chk, descripcion="Selector para mover tarjetas de lista", defaults={"completado": True})
            ItemChecklist.objects.get_or_create(checklist=chk, descripcion="Pruebas cruzadas de navegadores", defaults={"completado": False})

            Comentario.objects.get_or_create(
                tarjeta=card_integ,
                autor=u_camila,
                defaults={"contenido": "¡Excelente avance! El tablero luce muy fluido e intuitivo para el equipo."}
            )

        self.stdout.write(self.style.SUCCESS("[OK] Base de datos poblada exitosamente con datos de TaskFlow!"))
