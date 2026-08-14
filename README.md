# PRUEBA TÉCNICA WEARE DEV - TASKS CRUD (PYTHON/DJANGO & POSTGRESQL)

**Tasks CRUD** es un API REST que permite administrar la información de tareas.

Las características principales son:

  - Listado de tareas
  - Búsqueda de tarea por ID
  - Creación de tareas
  - Actualización de tareas
  - Eliminación lógica de tareas (soft delete utilizando campo deleted_at)
  - Listado de tareas próximas a vencer dentro del criterio de horas predefinido (criterio dentro del .env)
  - Búsqueda de tareas por filtros:
    - Búsqueda por texto (busca dentro de título y descripción)
    - Búsqueda por rango de fechas (desde - hasta)
    - Búsqueda con filtros combinados (por texto y rango de fechas)

## Tecnologías

  - **Python**
  - **Django**
  - **PostgreSQL**
  - **Docker**

## Librerías

  - **django-filters**: búsqueda por filtros
  - **drf-spectacular**: documentación Swagger & OpenAPI
  - **python-decouple**: manejo de .env y variables de entorno secretas

## Configuraciones

  - Se actualizó el campo "LANGUAGE_CODE" para que los mensajes de error predeterminados sean en español.

## Endpoints

### API
  
  - localhost:8000/api/ (puerto por defecto de Django) 

### Documentación

  - localhost:8000/api/docs

### Tasks (tareas)

  - `POST /api/tasks/` - Crear tarea
  - `GET /api/tasks/` - Listar tareas
  - `GET /api/tasks/{id}/` - Buscar tarea por ID
  - `GET /api/tasks/?status={status}&search={texto}` - Filtrar por texto y estado
  - `GET /api/tasks/?due_date_from=2026-08-13T00:00:00Z&due_date_to=2026-08-19T00:00:00Z` - Filtrar por rango de fecha
  - `GET /api/tasks/upcoming/` - Listar tareas próximas a vencer dentro del criterio definido
  - `PATCH /api/tasks/{id}/` - Editar tarea (solo se envía el parametro a editar)
  - `PUT /api/tasks/{id}/` - Editar tarea (se envía tanto el campo a actualizar con la información nueva, como los demás con sus datos correspondientes)
  - `PATCH /api/tasks/{id}/status/` - Actualizar estado
  - `DELETE /api/tasks/{id}/` - Eliminación lógica de tarea

## Ejemplos de request/response

Archivo de ejemplos de request/response: [archivo](./docs/request_response_examples.md).

## Colección Postman

La colección está dentro de `/docs/postman/`, ya incluye la variable de entorno `host` que hace referencia a `http://localhost:8000` por defecto.

Importar el archivo en Postman y ejecutar primero la carpeta "Datos de prueba" para poder verificar los endpoints de filtros y upcoming con datos reales predefinidos.

## Variables de entorno

Los valores por defecto de estas variables están en el archivo .env.template

- SECRET_KEY: clave secreta de Django (requerida)
- DEBUG: modo debug del proyecto
- POSTGRES_DB: nombre de la base de datos
- POSTGRES_USER: usuario de Postgres
- POSTGRES_PASSWORD: contraseña de Postgres
- DB_HOST: host de Postgres
- DB_PORT: puerto de Postgres
- UPCOMING_HOURS_LIMIT: criterio de horas para el endpoint de tareas próximas a vencer (por defecto 48 horas).

## Criterio próximas a vencer

El campo `UPCOMING_HOURS_LIMIT` en el archivo `.env` representa las horas en las que una tarea estaría próxima a vencer. Este campo tiene un valor predeterminado de `48 horas`.

Suponiendo que una tarea fue creada el día de hoy 13 de agosto, y se le dio un due_date (fecha de vencimiento) para el 14 o 15 de agosto, la tarea se encuentra próxima a vencer dentro del rango de las 48 horas y se listará en el endpoint `/api/tasks/upcoming/`.

Si la fecha de vencimiento para la tarea fuera, por ejemplo, el 20 de agosto, no se listaría dentro de las tareas próximas a vencer porque no está dentro del rango de las 48 horas, aún queda tiempo para esto.
Si se hiciera la petición al endpoint el día 18, ahora sí estaría dentro del rango de las 48 horas y se mostraría.

## Iniciar proyecto

### Pre-requisitos

- Python 3.11
- Docker
- pip

### 1. Clonar el repositorio

```bash
git clone https://github.com/0xkley/django-technical-test
cd django-technical-test
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv .venv
```

```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copiar el archivo de ejemplo ".env.template", renombrarlo a ".env" y reemplazar los valores:

```bash
# En Windows (PowerShell)
copy .env.template .env

# En otras terminales
cp .env.template .env
```

### 5. Iniciar la base de datos Postgres con Docker

```bash
docker compose up -d
```

Verificar que el contenedor esté corriendo:

```bash
docker ps
```

### 6. Ejecutar migraciones

```bash
python manage.py migrate
```

### 7. Levantar el servidor

```bash
python manage.py runserver
```

**Nota:** todas las rutas que incluyen `id` tienen que finalizar con `/` (ejemplo `/api/tasks/{id}/`), sino se genera un error debido a configuraciones del framework.
