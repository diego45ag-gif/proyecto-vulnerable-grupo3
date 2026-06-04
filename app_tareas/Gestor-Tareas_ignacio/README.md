Ignacio Pérez San Román

Descripción

Este proyecto es una aplicación web  para gestionar tareas. La aplicación permite añadir tareasa una lista marcarlas como completadas y eliminarlas.

He elegido esta aplicación porque es fácil de entender y también porque se puede ampliar en las siguientes prácticas del grupo.

La aplicación está hecha con Flask y se ejecuta con Docker.

Funcionalidades

La aplicación permite:

Añadir una tarea.
Ver las tareas creadas.
Marcar una tarea como completada.
Eliminar una tarea.
Tecnologías usadas
Python
Flask
HTML
CSS
Docker
Docker Compose
Estructura del proyecto
Gestor-Tareas_ignacio/
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

El archivo main.py tiene la parte principal de la aplicación.
El archivo index.html es la página que se muestra en el navegador.
El archivo style.css sirve para dar algo de estilo a la página.
El archivo requirements.txt contiene las dependencias necesarias.
El Dockerfile y el docker-compose.yml sirven para ejecutar la aplicación con Docker.

Cómo ejecutar la aplicación

Para ejecutar la aplicación es necesario tener instalado Docker Desktop.

Primero se abre PowerShell o la terminal dentro de la carpeta del proyecto.

Después se ejecuta este comando:

docker compose up --build

Cuando la aplicación esté iniciada, se abre el navegador y se entra en:

http://localhost:5000

Para parar la aplicación se puede pulsar CTRL + C en la terminal.

Relación con el entorno de una aplicación segura

En esta práctica no solo se ha pensado en que la aplicación funcione, sino también en el entorno donde se ejecuta.

Una aplicación no depende solo del código. También influyen el sistema operativo, las dependencias que usa, la red y la forma en la que se despliega.

Por eso se ha usado Docker. Con Docker la aplicación se puede ejecutar de una forma más controlada y parecida en distintos ordenadores, evitando algunos problemas de configuración.

En esta primera versión la aplicación es bastante sencilla. No usa servicios externos ni guarda datos personales o contraseñas. Esto hace que el riesgo inicial sea menor.

Algunas medidas básicas que se han tenido en cuenta son:

No se pueden crear tareas vacías.
El texto de las tareas tiene un límite de caracteres.
El modo debug de Flask está desactivado.
No se almacena información sensible.
La aplicación se ejecuta con Docker.
El proyecto se puede ampliar más adelante con nuevas medidas de seguridad.
Creación de la aplicación siguiendo el SDLC

1. Planificación

Se decidió crear un gestor de tareas porque es una aplicación sencilla, fácil de probar y que permite aplicar algunas medidas básicas de seguridad.

Se uso Docker para que la aplicación pudiera ejecutarse de forma más sencilla en otros equipos.

2. Análisis de requisitos

Se pensaron las funciones básicas que debía tener la aplicación:

Añadir tareas.
Mostrar las tareas creadas.
Marcar tareas como completadas.
Eliminar tareas.

También se tuvieron en cuenta algunos requisitos de seguridad:

Evitar tareas vacías.
Limitar el tamaño del texto introducido.
No guardar información personal.
Tener el modo debug desactivado.

3. Diseño

Se diseñó una estructura sencilla para que el proyecto fuera fácil de entender.

La aplicación se dividió en varias partes:

Código principal en Python.
Plantilla HTML para la página web.
Archivo CSS para el diseño.
Archivos de Docker para poder ejecutarla.

La idea era no hacer una aplicación demasiado compleja, sino una base que se pueda mejorar en las siguientes actividades.

4. Desarrollo

La aplicación se desarrolló con Flask.

Primero se creó la página principal. Después se añadieron las funciones para añadir tareas, completar tareas y eliminarlas.

También se añadió una validación básica para que no se puedan guardar tareas vacías.

5. Pruebas

Se hicieron pruebas manuales para comprobar que la aplicación funcionaba bien.

Las pruebas realizadas fueron:

Comprobar que la aplicación arranca con Docker.
Añadir una tarea nueva.
Intentar añadir una tarea vacía.
Marcar una tarea como completada.
Eliminar una tarea.
Comprobar que el modo debug aparece desactivado.

La aplicación se probó desde el navegador usando la dirección:

http://localhost:5000

6. Despliegue

El despliegue se hizo con Docker Compose.

Esto permite iniciar la aplicación con un solo comando:

docker compose up --build

De esta forma no hace falta instalar Flask manualmente en el ordenador, ya que las dependencias se instalan dentro del contenedor.

7. Mantenimiento

En futuras versiones se podrían añadir mejoras como:

Registro e inicio de sesión de usuarios.
Base de datos para guardar las tareas.
Contraseñas protegidas con hash.
Control de acceso para que cada usuario vea solo sus tareas.
Revisión de dependencias vulnerables.
Herramientas automáticas de análisis de seguridad.