# TaskFlow - Sistema de Gestión de Tareas Kanban

> **Asignatura:** IEI_N4_C1 - Clases de Backend con Django  
> **Proyecto Asignado:** TaskFlow (Plataforma Ágil tipo Trello)  
> **Desarrollador:** Kekari  
> **Tecnologías:** Python 3.14, Django 6.1, python-decouple, MySQL / SQLite, HTML5, CSS3  

---

## 📌 Descripción del Proyecto

**TaskFlow** es una aplicación web tipo Trello desarrollada sobre el framework **Django**, diseñada para la planificación, organización y seguimiento ágil de proyectos mediante tableros Kanban interactivos. 

El sistema implementa una arquitectura desacoplada basada en el patrón de diseño **Modelo-Vista-Plantilla (MTV)**, incorporando persistencia relacional con ORM, configuración modular con variables de entorno (`python-decouple`), panel administrativo enriquecido (`ModelAdmin`), vistas Kanban dinámicas y página de error 404 personalizada según las directrices académicas.

---

## 🚀 Características Principales

* **Tableros y Espacios de Trabajo:** Organización multinivel por equipos y proyectos con visibilidad privada, pública o de espacio.
* **Columnas y Listas de Estado:** Estructuración de flujos Kanban (e.g. *Por Hacer*, *En Progreso*, *En Revisión*, *Finalizado*).
* **Tarjetas Inteligentes:** Tareas con título, descripción, prioridades clasificadas por color, fechas de vencimiento, responsables y estimación horaria.
* **Etiquetas y Categorías:** Código cromático para bugs, frontend, backend, seguridad y documentación.
* **Checklists y Subtareas:** Desglose de actividades con verificación de completitud porcentual.
* **Comentarios y Auditoría:** Historial cronológico de cambios y comentarios colaborativos entre usuarios.
* **Seguridad y Desacoplamiento:** Credenciales, claves secretas (`SECRET_KEY`) y configuración de base de datos aisladas en `.env`.
* **Página de Error 404 Genérica:** Manejo elegante de rutas inexistentes protegiendo información interna del servidor.

---

## 🛠️ Instalación y Configuración Paso a Paso

### 1. Clonar el Repositorio
```bash
git clone <url-del-repositorio>
cd "proyecto back"
```

### 2. Creación del Ambiente Virtual (VENV)
```bash
python -m venv venv
```

### 3. Activación del Ambiente Virtual
* En Windows (PowerShell):
```powershell
Set-ExecutionPolicy Bypass -Scope CurrentUser
.\venv\Scripts\Activate
```
* En Linux / macOS:
```bash
source venv/bin/activate
```

### 4. Actualización de PIP e Instalación de Dependencias
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configuración de Variables de Entorno (`.env`)
Copie el archivo de ejemplo `.env.example` y renómbrelo como `.env`:
```bash
cp .env.example .env
```
Ajuste los valores de configuración según su entorno:
```env
SECRET_KEY=clave_secreta_django_aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=sqlite
NAME=taskflow_db.sqlite3
HOST=127.0.0.1
PORT=3306
USER=root
PASSWORD=
```
*(Para utilizar MySQL, configure `DB_ENGINE=mysql` y suministre las credenciales de su servidor MySQL local).*

### 6. Ejecución de Migraciones
Aplique las migraciones del modelo de datos de Django:
```bash
python manage.py makemigrations taskflow_app
python manage.py migrate
```

### 7. Carga de Datos de Demostración (Seed)
Para poblar automáticamente tableros, columnas Kanban, usuarios, tarjetas y etiquetas de prueba:
```bash
python manage.py poblar_datos
```

### 8. Creación de Superusuario (Administrador)
```bash
python manage.py createsuperuser
```
*(Por defecto se incluye el usuario administrador de prueba `admin` con contraseña `admin1234`).*

### 9. Iniciar el Servidor de Desarrollo
```bash
python manage.py runserver
```
La aplicación estará disponible en [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## 🧭 Mapa de Rutas de la Aplicación

| Ruta URL | Nombre | Descripción |
| :--- | :--- | :--- |
| `/` | `inicio` | Landing page principal con métricas en tiempo real y resumen de funcionalidades |
| `/tableros/` | `tableros` | Explorador de tableros Kanban organizados por Espacio de Trabajo |
| `/tablero/<id>/` | `detalle_tablero` | Tablero Kanban interactivo con listas, tarjetas, tags y acciones de movimiento |
| `/tarjeta/<id>/mover/` | `mover_tarjeta` | Endpoint POST para mover tarjetas entre columnas Kanban |
| `/lista/<id>/crear-tarjeta/` | `crear_tarjeta` | Endpoint POST para creación rápida de tarjetas dentro de una columna |
| `/admin/` | `admin:index` | Panel administrativo de Django con gestión CRUD de todas las entidades |
| `/ruta-no-valida/` | `handler404` | Plantilla 404 personalizada con diseño integrado |

---

## 🗄️ Modelo de Datos Implementado

El modelo relacional implementado en `taskflow_app/models.py` consta de 17 clases que soportan la totalidad del flujo de trabajo:

1. **`Usuario`**: Perfil de usuario con RUT, nombre, correo, teléfono, cargo y color de avatar.
2. **`EspacioTrabajo`**: Organización o área de trabajo que agrupa múltiples tableros.
3. **`RolColaborador`**: Catálogo de roles (ADMIN, MIEMBRO, OBSERVADOR).
4. **`MiembroEspacio`**: Tabla asociativa entre usuarios y espacios con rol asignado.
5. **`VisibilidadTablero`**: Nivel de acceso del tablero (PRIVADO, ESPACIO, PUBLICO).
6. **`Tablero`**: Tablero Kanban con nombre, descripción, color de fondo, ícono y creador.
7. **`MiembroTablero`**: Colaboradores asignados al tablero.
8. **`Lista`**: Columnas del flujo Kanban con orden y posición.
9. **`Prioridad`**: Catálogo de prioridades con código, color y nivel de urgencia.
10. **`Etiqueta`**: Etiquetas cromáticas para catalogación de tareas.
11. **`Tarjeta`**: Unidad de trabajo con lista, prioridad, fechas, horas estimadas y asignado.
12. **`TarjetaEtiqueta`**: Relación de asignación de etiquetas a tarjetas.
13. **`Checklist`**: Agrupador de subtareas dentro de una tarjeta.
14. **`ItemChecklist`**: Elemento verificable individual de checklist con estado completado.
15. **`Comentario`**: Retroalimentación y comentarios entre miembros en cada tarjeta.
16. **`Adjunto`**: Registro de archivos y enlaces asociados a la tarjeta.
17. **`HistorialActividad`**: Registro de auditoría cronológica de eventos en el tablero.

---

## 🧪 Pruebas Unitarias

Para ejecutar la suite automatizada de validaciones unitarias:
```bash
python manage.py test
```
Validará la consistencia de modelos, creación de tableros, lógica de relaciones foráneas y respuestas HTTP 200/302 de las vistas.

---

## 📦 Estructura del Proyecto

```text
backend/
├── .env                     # Variables de entorno (ignorado en git)
├── .env.example             # Plantilla de variables de entorno
├── .gitignore               # Archivos excluidos de control de versiones
├── manage.py                # Gestor de comandos de Django
├── README.md                # Documentación del proyecto
├── requirements.txt         # Lista de dependencias congeladas (pip freeze)
├── static/                  # Archivos estáticos complementarios
├── core/                    # Módulo de configuración principal
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py          # Configuración con Decouple y base de datos
│   ├── urls.py              # Enrutador principal y handler404
│   └── wsgi.py
└── taskflow_app/            # Aplicación TaskFlow
    ├── admin.py             # Registro de modelos en Django Admin
    ├── apps.py              # Metadatos de la app
    ├── models.py            # Modelos ORM de TaskFlow
    ├── tests.py             # Pruebas unitarias
    ├── urls.py              # Rutas de la app
    ├── views.py             # Lógica de vistas y controladores
    ├── management/
    │   └── commands/
    │       └── poblar_datos.py # Comando de carga de datos iniciales
    ├── migrations/          # Scripts de migración de base de datos
    └── templates/           # Plantillas HTML
        ├── 404.html         # Error 404 personalizado
        ├── base.html        # Plantilla base común
        ├── inicio.html      # Página de inicio
        ├── tablero.html     # Tablero Kanban interactivo
        └── tableros.html    # Listado de tableros
```
