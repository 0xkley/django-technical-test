# Ejemplos de uso de la API

Ejemplos de Requests y Responses del API.
Las fechas están en formato ISO.

Todos los endpoints que tienen `id` en la URL necesita la barra al final o provoca un error por configuraciones del framework.

## Crear una tarea

POST `/api/tasks/`

```json
{
  "title": "Tarea 1",
  "description": "Tarea de la universidad",
  "due_date": "2026-08-20T10:00:00Z",
  "created_by_name": "Jefferson"
}
```

Devuelve 201 con la tarea creada:

```json
{
  "id": "37aa84f4-6937-4cca-8e8a-b538604f8e4a",
  "title": "Tarea 1",
  "description": "Tarea de la universidad",
  "status": "pending",
  "due_date": "2026-08-20T10:00:00Z",
  "created_at": "2026-08-13T21:30:22.903419Z",
  "updated_at": "2026-08-13T21:30:22.903434Z",
  "created_by_name": "Jefferson",
  "deleted_at": null
}
```

## Listar

GET `/api/tasks/` devuelve un array con todas las tareas que no estén eliminadas

```json
[
  {
    "id": "37aa84f4-6937-4cca-8e8a-b538604f8e4a",
    "title": "Tarea 1",
    "description": "Tarea de la universidad",
    "status": "pending",
    "due_date": "2026-08-20T10:00:00Z",
    "created_at": "2026-08-13T21:30:22.903419Z",
    "updated_at": "2026-08-13T21:30:22.903434Z",
    "created_by_name": "Jefferson",
    "deleted_at": null
  }
]
```

## Buscar por id

GET `/api/tasks/{id}/` devuelve la tarea con ese ID

```json
{
  "id": "37aa84f4-6937-4cca-8e8a-b538604f8e4a",
  "title": "Tarea 1",
  "description": "Tarea de la universidad",
  "status": "pending",
  "due_date": "2026-08-20T10:00:00Z",
  "created_at": "2026-08-13T21:30:22.903419Z",
  "updated_at": "2026-08-13T21:30:22.903434Z",
  "created_by_name": "Jefferson",
  "deleted_at": null
}
```

Si la tarea no existe o fue eliminada da un error 404

```json
{
  "detail": "La tarea con id 37aa84f4-6937-4cca-8e8a-b538604f8e4a no existe o fue eliminada."
}
```

## Actualizar

**PATCH** `/api/tasks/{id}/` - solamente se envia el dato que se quiere cambiar

```json
{ "title": "Tarea 1 actualizada" }
```

**PUT** `/api/tasks/{id}/` - hay que mandar el objeto completo, si no da error 400

```json
{
  "title": "Tarea 1 actualizada completa",
  "description": "Nueva descripcion",
  "status": "pending",
  "due_date": "2026-08-21T10:00:00Z",
  "created_by_name": "Jefferson"
}
```

Los dos endpoints devuelven la tarea

## Cambiar estado

PATCH `/api/tasks/{id}/status/` - cualquier otro dato aparte del status se ignora, solo actualiza ese campo

```json
{ "status": "completed" }
```

Si se manda un valor de status que no está permitido dentro del enum ("pending", "completed", "postponed") da un error

```json
{
  "status": ["Estado inválido. Los valores permitidos son: pending, completed, postponed."]
}
```

## Eliminar (lógica)

DELETE `/api/tasks/{id}/` - cambia el estado de `deleted_at` de NULL a una fecha, lo que indica que se eliminó, pero no se borra del todo en la base de datos, devuelve estado 204

## Próximas a vencer

GET `/api/tasks/upcoming/`

Trae las tareas con vencimiento dentro del criterio definido (48 horas, se define en el archivo .env)
No muestra las tareas ya completadas

```json
[
  {
    "id": "37aa84f4-6937-4cca-8e8a-b538604f8e4a",
    "title": "Tarea 1",
    "description": "Tarea de la universidad",
    "status": "pending",
    "due_date": "2026-08-14T18:00:00Z",
    "created_at": "2026-08-13T21:30:22.903419Z",
    "updated_at": "2026-08-13T21:30:22.903434Z",
    "created_by_name": "Jefferson",
    "deleted_at": null
  }
]
```

## Filtros

Todos van como query parameters y se pueden combinar:

- Por estado: `/api/tasks/?status=pending`
- Por texto (busca en title y description): `/api/tasks/?search=universidad`
- Por rango de fechas: `/api/tasks/?due_date_from=2026-08-13T00:00:00Z&due_date_to=2026-08-19T00:00:00Z`
- Combinado: `/api/tasks/?status=pending&search=universidad&due_date_from=2026-08-13T00:00:00Z`

Devuelve un listado con los datos que coincidan con los filtros

## Datos de prueba (colección Postman)

La colección de Postman tiene una carpeta "Datos de prueba" con 5 tareas con fechas diferentes para verificar los endpoints de búsqueda por filtros y próximas a vencer.

Ejecutar las peticiones en orden antes de verificar filtros y próximos a vencer.

La salida debería ser algo tipo:

- Tarea 1: vence 21h posterior a creación, está pendiente, debe mostrarse en `upcoming`.

- Tarea 2: vence 47h posterior a creación, está pendiente, debe mostrarse en `upcoming`.

- Tarea 3: vence 5 días posterior a creación, está pendiente, NO debe mostrarse en `upcoming` (fuera de rango).

- Tarea 4: vence 21h posterior a creación, está completada, NO debe mostrarse en `upcoming` (completada).

- Tarea 5: vence 1 mes posterior a creación, está pendiente, NO debe mostrarse en `upcoming` (fuera de rango).