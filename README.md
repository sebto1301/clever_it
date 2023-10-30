# Task Tag User

Esta es una API básica que permite la administración de tareas que se pueden etiquetar y cambiar el estado.

La API por defecto utiliza una base de datos sqlite, lo que permite ejecutarse en el equipo local sin problemas. Sin embargo, también se puede utilizar mysql comentando la línea 9 de /app/__init__.py y descomentando la línea 8 y ejecutar por medio de docker-compose, que crea una base de datos mysql con las credenciales utilizadas en la API como modo de prueba.

## Para ejecutar la API necesita:

Modo local:
```
    pip install -r requirements.txt 
    python run.py
```
Docker:
```
    docker build --no-cache -t flask_cleverit .
    docker run -p 8000:8000 -it flask_cleverit
```

Docker-compose (para usar con mysql):
```
    docker-compose up --build
```

No es necesario ejecutar un script para la creación de la base de datos. Al no detectarse las tablas, éstas se crean automáticamente tanto en SQLite como en mysql.

La API tiene una protección con JWT token, a través de Bearer Token, para los endpoints que hacen cambios, por lo que se crea un primer usuario cuyo token se imprime en pantalla. Éste puede ser eliminado y reemplazado por otro. Tenga la precaución de no eliminar el usuario sin un reemplazo.

Todos los usuarios pueden modificar las tareas y usuarios.

## Endpoints

### TAREAS:

```POST '/tasks'```
Requiere token JWT
Crear una tarea en el cuerpo de mensaje en JSON


Ejemplo:

```
{
    "title": "Tarea 1",
    "description": "Tarea muy importante",
    "due_date": "2023-10-31",
    "status": "esperando",
    "tags": [
        "urgente",
        "interna",
    ]
}
```


```GET '/tasks'```
Obtener todas las tareas


```GET '/tasks/<task_id>'```
Obtener una tarea específica con el ID

```PUT '/tasks/<task_id>'```
Requiere token JWT
Modificar tarea identificada con el ID


```DELETE '/tasks/<task_id>'```
Requiere token JWT
Eliminar tarea identificada con el ID

```POST '/tasks/<task_id>/<tag_name>'```
Requiere token JWT
Agrega tag a la tarea identificada


```DELETE '/tasks/<task_id>/<tag_name>'```
Requiere token JWT
Elimina tag de la tarea identificada

```POST '/tasks/status/<task_id>/<status>'```
Requiere token JWT
Cambia el status de la tarea identificada por el texto que se coloque.

### USUARIOS

```GET '/users'```
Requiere token JWT
Obtener listado de usuarios

```POST '/users'```
Requiere token JWT
Crear usuario en el cuerpo de mensaje

Ejemplo:

```
{
    "name":"Fulanito De Tal"
}
```

```DELETE '/users/<user_id>'```
Requiere token JWT
Eliminar usuario identificado con ID