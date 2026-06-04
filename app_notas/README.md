Alejandro (Grupo 3)

# Gestor de Notas Seguro

## Descripción

Este proyecto es una aplicación web para gestionar notas. La aplicación permite crear notas con un título y un contenido, verlas todas, editarlas y eliminarlas. Cada nota guarda automáticamente su fecha de creación.

He elegido esta aplicación porque sigue el mismo patrón que el Gestor de Tareas del grupo, es fácil de entender y se puede ampliar en las siguientes prácticas.

La aplicación está hecha con Flask y se ejecuta con Docker.

## Funcionalidades

La aplicación permite:

- Crear una nota (título + contenido).
- Ver todas las notas creadas.
- Editar una nota existente.
- Eliminar una nota.
- Guardar automáticamente la fecha de creación de cada nota.

## Tecnologías usadas

- Python
- Flask
- HTML
- CSS
- Docker
- Docker Compose

## Modelo de datos

Las notas se guardan en una lista de Python en memoria (sin base de datos). Cada nota tiene la siguiente estructura:

```python
{
    "id": 1,
    "titulo": "Mi primera nota",
    "contenido": "Texto de la nota",
    "fecha_creacion": "02/06/2026 17:30"
}
```

Al no usar base de datos, las notas se borran cuando se reinicia la aplicación.

## Estructura del proyecto

```
app_notas/
│
├── app/
│   ├── static/
│   │   └── style.css
│   ├── templates/
│   │   └── index.html
│   └── main.py
│
├── Dockerfile
├── docker-compose.yml
├── README.md
└── requirements.txt
```

- El archivo `main.py` tiene la parte principal de la aplicación (lógica Flask y rutas).
- El archivo `index.html` es la página que se muestra en el navegador.
- El archivo `style.css` sirve para dar estilo a la página.
- El archivo `requirements.txt` contiene las dependencias necesarias.
- El `Dockerfile` y el `docker-compose.yml` sirven para ejecutar la aplicación con Docker.

## Rutas de la aplicación

| Método | Ruta                | Descripción                          |
|--------|---------------------|--------------------------------------|
| GET    | `/`                 | Muestra todas las notas              |
| POST   | `/agregar`          | Crea una nueva nota                  |
| GET    | `/editar/<id>`      | Muestra el formulario de edición     |
| POST   | `/editar/<id>`      | Guarda los cambios de una nota       |
| POST   | `/eliminar/<id>`    | Elimina una nota                     |

## Instalación

Para ejecutar la aplicación es necesario tener instalado Docker Desktop.

Primero se clona o se copia el proyecto y se abre la terminal (PowerShell o similar) dentro de la carpeta del proyecto.

## Cómo ejecutar la aplicación con Docker

Dentro de la carpeta del proyecto se ejecuta este comando:

```
docker compose up --build
```

Cuando la aplicación esté iniciada, se abre el navegador y se entra en:

```
http://localhost:5000
```

Para parar la aplicación se puede pulsar `CTRL + C` en la terminal.

## Ejecución sin Docker (opcional)

Si se prefiere ejecutar sin Docker, se pueden instalar las dependencias y lanzar la aplicación así:

```
pip install -r requirements.txt
cd app
python main.py
```

Y después abrir `http://localhost:5000` en el navegador.

## Medidas básicas de seguridad

- No se pueden crear notas con el título o el contenido vacíos.
- El título y el contenido tienen un límite de caracteres.
- El modo debug de Flask está desactivado.
- No se almacena información sensible.
- La aplicación se ejecuta dentro de un contenedor Docker.

## Autor

Alejandro (Grupo 3)
