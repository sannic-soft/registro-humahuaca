# Registro de Alojamientos de Humahuaca

MVP educativo para publicar un directorio de alojamientos y anuncios
relacionados con la disponibilidad de hospedaje en Humahuaca, Jujuy.

## Tecnologías

- Python
- Flask
- SQLite
- HTML, CSS y JavaScript
- Git y GitHub

## Requisitos

- Python 3
- Flask instalado mediante los paquetes del sistema
- Git
- Un navegador web

## Instalación en antiX / Debian

Instalar Flask desde los repositorios:

    sudo apt update
    sudo apt install python3-flask

No se necesita Node.js ni un servidor SQLite independiente.

## Ejecutar en desarrollo

Desde el directorio del proyecto, configurar las variables de entorno:

    export ADMIN_PASSWORD='reemplazar-por-una-clave-local'
    export SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"

Iniciar la aplicación:

    python3 app.py

Abrir en el navegador:

    http://127.0.0.1:5000/

La aplicación crea automáticamente la base de datos local en:

    instance/alojamientos.db

## Rutas principales

- `/` — página de inicio
- `/alojamientos` — directorio público
- `/alojamientos/<id>` — detalle de un alojamiento
- `/login` — acceso administrativo
- `/admin` — panel de administración
- `/admin/alojamientos` — gestión de alojamientos
- `/admin/anuncios` — gestión de anuncios

## Estructura

- `app.py`: rutas y lógica de la aplicación
- `database.py`: conexión e inicialización de SQLite
- `schema.sql`: definición de tablas
- `templates/`: plantillas HTML
- `static/`: CSS, JavaScript e imágenes
- `tests/`: pruebas automatizadas
- `instance/`: datos locales, excluidos de Git
- `uploads/`: reservado para futuras cargas de archivos

## Estado del proyecto

Primera versión funcional en desarrollo local. Se han probado
manualmente la página pública y el registro de un alojamiento.

Antes de publicar en Internet deben revisarse la seguridad, la
configuración de producción, las sesiones y la autenticación.

## Datos y secretos

No subir la base de datos local, contraseñas, claves secretas ni
archivos de configuración privados al repositorio.

La base de datos no se incluye en Git. Los registros creados localmente
no se trasladan automáticamente al clonar el proyecto.
