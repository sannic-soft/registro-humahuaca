# Registro de Alojamientos de Humahuaca

Plataforma web desarrollada como un **MVP (Producto Mínimo Viable)** para facilitar la consulta y administración de alojamientos turísticos de Humahuaca.

El sistema reúne en un mismo sitio la información pública de los alojamientos registrados, sus fotografías y anuncios de interés. También incorpora herramientas de administración para gestionar alojamientos, cuentas y anuncios.

> **Estado del proyecto:** MVP académico en evolución. Algunas estructuras de la base de datos, como las reservas, forman parte del modelo de datos, pero no implican que exista un proceso de reserva en línea habilitado para el público.

---

## Índice

- [¿Qué permite hacer la plataforma?](#qué-permite-hacer-la-plataforma)
- [Tipos de usuario](#tipos-de-usuario)
- [Manual de uso](#manual-de-uso)
  - [Visitantes](#1-visitantes)
  - [Usuarios registrados](#2-usuarios-registrados)
  - [Propietarios](#3-propietarios)
  - [Administradores](#4-administradores)
- [Requisitos para instalar el proyecto](#requisitos-para-instalar-el-proyecto)
- [Instalación y ejecución local](#instalación-y-ejecución-local)
- [Configuración inicial](#configuración-inicial)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Base de datos y archivos](#base-de-datos-y-archivos)
- [Seguridad y buenas prácticas](#seguridad-y-buenas-prácticas)
- [Tecnologías utilizadas](#tecnologías-utilizadas)
- [Despliegue](#despliegue)
- [Limitaciones conocidas](#limitaciones-conocidas)

---

## ¿Qué permite hacer la plataforma?

- Consultar alojamientos turísticos publicados.
- Buscar alojamientos por nombre, tipo, ubicación de referencia, servicios o descripción.
- Abrir la ficha de un alojamiento y consultar sus datos e imágenes.
- Crear una cuenta de usuario.
- Iniciar y cerrar sesión.
- Administrar alojamientos desde un panel de administración.
- Asignar alojamientos a propietarios.
- Gestionar cuentas y roles de usuario desde la administración.
- Publicar, editar, activar y desactivar anuncios generales.
- Mostrar en la página principal los anuncios activos y una selección de alojamientos publicados.

La información visible para los visitantes depende del estado asignado a cada alojamiento. Los alojamientos pendientes, en borrador o suspendidos no aparecen en el catálogo público.

## Tipos de usuario

La plataforma contempla tres roles:

| Rol | Acceso principal |
|---|---|
| **Visitante** | Puede navegar por la página principal, consultar y buscar alojamientos publicados y ver sus fichas. |
| **Usuario** | Puede registrarse e iniciar sesión. La cuenta creada desde el formulario público tiene este rol. |
| **Propietario** | Accede a las funciones habilitadas para gestionar sus propios alojamientos. No puede modificar alojamientos de otros propietarios. |
| **Administrador** | Gestiona alojamientos, propietarios, cuentas de usuario y anuncios desde el panel de administración. |

> El rol de propietario no se obtiene mediante el registro público común. La cuenta debe ser creada o habilitada por un administrador.

---

## Manual de uso

### 1. Visitantes

No es necesario crear una cuenta para consultar la información pública.

1. Ingresar a la dirección web de la plataforma.
2. En la página principal, revisar los anuncios y alojamientos destacados.
3. Entrar en **Alojamientos** para ver el catálogo.
4. Utilizar el campo de búsqueda para filtrar los resultados.
5. Seleccionar un alojamiento para abrir su ficha.
6. Consultar la descripción, ubicación de referencia, capacidad, teléfono, servicios y fotografías disponibles.

Solo se muestran alojamientos que el administrador haya marcado como **Publicados**.

### 2. Usuarios registrados

#### Crear una cuenta

1. Seleccionar la opción **Registrarse**.
2. Completar nombre, correo electrónico y contraseña.
3. Repetir la contraseña para confirmarla.
4. Enviar el formulario.

El sistema valida los campos, comprueba que el correo no esté registrado y solicita una contraseña de al menos 8 caracteres.

La cuenta creada desde este formulario queda registrada con el rol **usuario**.

#### Iniciar sesión

1. Seleccionar **Iniciar sesión**.
2. Introducir el correo electrónico y la contraseña.
3. Enviar el formulario.

Si los datos son correctos y la cuenta está activa, se inicia la sesión.

#### Cerrar sesión

Utilizar la opción **Cerrar sesión** del menú. La sesión se finaliza y se vuelve a la navegación pública.

### 3. Propietarios

El propietario debe recibir sus credenciales de acceso por parte del administrador.

1. Iniciar sesión con la cuenta asignada.
2. Acceder al área de propietario desde la navegación de la plataforma.
3. Consultar los alojamientos asociados a su cuenta.
4. Utilizar las opciones disponibles para editar la información de sus alojamientos.
5. Guardar los cambios realizados.

**Importante:** cada propietario solo puede acceder y modificar los alojamientos que tiene asignados. Si intenta acceder a un alojamiento perteneciente a otra cuenta, el sistema debe impedirlo.

La publicación de un alojamiento está sujeta al estado que gestione el administrador. Si un alojamiento no aparece en el catálogo público, puede encontrarse pendiente, en borrador o suspendido.

### 4. Administradores

El administrador es responsable de mantener actualizada la información publicada y gestionar las cuentas de la plataforma.

#### Acceder al panel

1. Iniciar sesión con una cuenta cuyo rol sea **admin**.
2. Abrir el panel de administración.
3. Consultar el resumen de alojamientos, publicaciones, anuncios y usuarios.

#### Gestionar alojamientos

Desde la sección de alojamientos se puede:

- Consultar el listado de alojamientos registrados.
- Ver a qué propietario está asociado cada alojamiento.
- Registrar nuevos alojamientos y asignarles un propietario activo.
- Revisar los datos cargados.
- Cambiar el estado de publicación.

Los estados disponibles son:

| Estado | Significado |
|---|---|
| **Borrador** | Registro en preparación; no se muestra públicamente. |
| **Pendiente** | Requiere revisión o decisión administrativa. |
| **Publicado** | Se muestra en el catálogo público. |
| **Suspendido** | Deja de mostrarse al público temporalmente. |

Para que un alojamiento aparezca en la web pública, su estado debe ser **Publicado**.

#### Gestionar propietarios y usuarios

Desde la administración de usuarios se pueden gestionar las cuentas del sistema y sus roles, de acuerdo con las opciones disponibles en el panel.

Para incorporar un propietario:

1. Crear o localizar su cuenta de usuario.
2. Asignarle el rol **propietario**.
3. Verificar que la cuenta esté activa.
4. Asociar el alojamiento correspondiente a esa cuenta.
5. Comunicarle sus credenciales de acceso de forma privada.

No se deben compartir contraseñas en documentación pública ni cargarlas en este README.

#### Gestionar anuncios

Los anuncios son mensajes generales que pueden mostrarse en la página principal.

1. Entrar en la sección **Anuncios**.
2. Crear un anuncio indicando título y descripción.
3. Completar, cuando corresponda, la URL de imagen y el enlace de destino.
4. Guardar el anuncio.
5. Activarlo para que pueda mostrarse públicamente.

También se pueden editar anuncios existentes y activarlos o desactivarlos. Los anuncios desactivados se conservan en la administración, pero no se muestran en la página pública.

---

## Requisitos para instalar el proyecto

Para ejecutar el proyecto en una computadora propia se necesita:

- Python 3.10 o superior (se recomienda una versión compatible con Flask 3).
- Git, si se desea clonar el repositorio.
- SQLite 3 (normalmente incluido en la instalación de Python).
- Un navegador web actualizado.

La aplicación utiliza Flask y Werkzeug. Las dependencias de Python se encuentran declaradas en `requirements.txt`.

## Instalación y ejecución local

Los siguientes pasos están pensados para Linux, macOS o Windows con Python instalado.

### 1. Descargar el repositorio

Con Git:

```bash
git clone https://github.com/sannic-soft/registro-humahuaca.git
cd registro-humahuaca
```

También se puede descargar el repositorio como archivo ZIP desde GitHub y descomprimirlo.

> Si la versión que se desea probar está publicada en una rama específica, seleccionar esa rama en GitHub antes de descargarla. La rama de desarrollo puede contener cambios que todavía no estén integrados en la rama principal.

### 2. Crear un entorno virtual (recomendado)

Linux o macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Instalar las dependencias

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar la clave de sesión

Para una ejecución local de desarrollo, Flask puede generar una clave temporal automáticamente. Para mantener una clave fija durante las pruebas, se puede definir una variable de entorno.

Linux o macOS:

```bash
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
```

Windows PowerShell:

```powershell
$env:SECRET_KEY = (py -c "import secrets; print(secrets.token_hex(32))")
```

### 5. Inicializar la base de datos

La aplicación incluye un comando de Flask para crear las tablas:

```bash
flask --app app init-db
```

La base de datos local se crea por defecto dentro de la carpeta `instance/`, con el nombre `alojamientos.db`.

Si se define `DATABASE_PATH`, la aplicación utilizará esa ubicación en lugar de la ruta predeterminada.

### 6. Ejecutar la aplicación

```bash
flask --app app run --debug
```

Abrir en el navegador:

```text
http://127.0.0.1:5000
```

Para detener el servidor, volver a la terminal y presionar `Ctrl + C`.

---

## Configuración inicial

Una instalación nueva crea la estructura de la base de datos, pero no debe suponerse que incluye usuarios, alojamientos o anuncios de demostración.

- La primera cuenta creada mediante el formulario público tendrá rol `usuario`.
- Para utilizar el panel de administración se necesita una cuenta con rol `admin`.
- Las cuentas de propietarios deben ser creadas o configuradas por un administrador.
- Los alojamientos deben estar asociados a una cuenta de propietario.
- Para que un alojamiento sea visible, el administrador debe asignarle el estado `publicado`.

**No existe una contraseña universal de administrador.** Las credenciales dependen de cómo se haya preparado la base de datos de cada instalación. No publicar credenciales reales en el repositorio.

---

## Estructura del proyecto

```text
registro-humahuaca/
├── app.py
├── database.py
├── schema.sql
├── requirements.txt
├── routes/
│   ├── __init__.py
│   ├── public.py
│   ├── auth.py
│   ├── owner.py
│   └── admin.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── alojamientos.html
│   ├── alojamiento_detalle.html
│   ├── login.html
│   ├── registro.html
│   └── admin/
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/
└── instance/
```

- `app.py`: configuración y creación de la aplicación Flask.
- `database.py`: conexión y operaciones de inicialización de SQLite.
- `schema.sql`: estructura de las tablas de la base de datos.
- `routes/`: rutas y lógica de las distintas áreas.
- `templates/`: páginas HTML renderizadas por Flask.
- `static/`: hojas de estilo, JavaScript e imágenes.
- `instance/`: ubicación habitual de la base de datos local. Su contenido no debe subirse al repositorio si contiene datos privados.

La estructura puede variar ligeramente entre versiones del repositorio.

## Base de datos y archivos

La aplicación utiliza SQLite. Entre las entidades principales del modelo se encuentran:

- **usuarios:** datos de acceso, rol y estado de las cuentas.
- **alojamientos:** información de cada alojamiento, propietario asociado y estado de publicación.
- **imagenes_alojamiento:** imágenes asociadas a cada alojamiento.
- **anuncios:** anuncios generales que pueden mostrarse en la página principal.
- **reservas:** estructura prevista en el modelo de datos para registrar reservas.

Las fotografías deben estar disponibles en las rutas de archivos indicadas en sus registros de imagen. En el proyecto, los archivos estáticos se sirven desde `static/`.

**Respaldo:** antes de actualizar la aplicación o modificar datos, realizar una copia de la base SQLite y de las fotografías cargadas. La base de datos y las imágenes son datos independientes: copiar solo el código no garantiza conservar los registros ni sus archivos.

## Seguridad y buenas prácticas

- Utilizar contraseñas únicas y de al menos 8 caracteres.
- No compartir cuentas administrativas.
- No subir bases de datos reales, contraseñas, claves secretas ni datos personales al repositorio.
- Configurar `SECRET_KEY` mediante una variable de entorno en producción.
- Configurar `APP_ENV=production` y `DATABASE_PATH` según el entorno de alojamiento.
- Mantener copias de seguridad de la base de datos y de `static/uploads/`.
- No ejecutar el servidor de desarrollo de Flask como servidor público de producción.

La aplicación incorpora almacenamiento de contraseñas mediante hash, control de acceso por roles y protección CSRF en formularios sensibles.

## Tecnologías utilizadas

- **Python**
- **Flask**
- **Werkzeug**
- **SQLite**
- **HTML**
- **CSS**
- **JavaScript**

## Despliegue

El proyecto puede ejecutarse localmente y adaptarse a un servicio de alojamiento compatible con aplicaciones Flask, como PythonAnywhere.

Para un despliegue público:

1. Subir o clonar el código en el servidor.
2. Instalar las dependencias de `requirements.txt` en el entorno correspondiente.
3. Configurar una `SECRET_KEY` segura.
4. Configurar `APP_ENV=production`.
5. Definir `DATABASE_PATH` apuntando a una base de datos persistente y escribible.
6. Inicializar la base de datos si se trata de una instalación nueva.
7. Configurar el archivo WSGI para importar la aplicación Flask.
8. Comprobar que las fotografías y demás archivos estáticos estén presentes.
9. Reiniciar la aplicación desde el panel del servicio.

En producción, `SECRET_KEY` es obligatoria. La aplicación falla al iniciar si `APP_ENV=production` y no se ha definido esa variable.

La configuración concreta del archivo WSGI y las rutas depende del proveedor de alojamiento utilizado.

## Limitaciones conocidas

- El proyecto es un MVP y puede cambiar entre versiones.
- El catálogo público muestra únicamente alojamientos publicados.
- El registro público crea cuentas con rol `usuario`; no crea propietarios ni administradores.
- La administración de cuentas y la asignación de alojamientos requieren permisos de administrador.
- Aunque el modelo de datos contempla reservas, no debe interpretarse como un sistema de reservas en línea completo: no se debe asumir que permite confirmar disponibilidad, cobrar o gestionar pagos.
- La disponibilidad de fotografías depende de que los archivos estén presentes en el servidor y sus rutas sean correctas.

---

## Autoría y propósito

El objetivo del MVP es centralizar información de alojamientos turísticos y ofrecer una herramienta sencilla para su consulta y administración.
