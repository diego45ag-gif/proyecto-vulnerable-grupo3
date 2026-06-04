# Proyecto Integrado Grupo 3 - Aplicación Segura (DevSecOps)

## 1. Definición de la Aplicación y Ejecución
Este proyecto unifica cuatro micro-aplicaciones en un único ecosistema contenedorizado. El sistema permite la gestión integral de recursos internos de una organización, separando la lógica en distintos módulos aislados para mejorar la escalabilidad y seguridad.

**Módulos integrados:**
* **Puerto 5000:** Gestor de Notas
* **Puerto 5001:** Gestor de Usuarios
* **Puerto 5002:** App de Inventario 
* **Puerto 5003:** Gestor de Tareas

**Miembros del Grupo 3:**
* Alejandro ([Enlace a su repositorio original])
* Diego ([Enlace a su repositorio original])
* Ignacio ([Enlace a su repositorio original])
* Ricardo ([Enlace a su repositorio original])

**Instrucciones de Ejecución:**
Para desplegar todo el ecosistema de forma local y simultánea, asegúrese de tener Docker y Docker Compose instalados, y ejecute en la raíz del proyecto:
`docker compose up --build`

---

## 2. Consideraciones de Seguridad (Enfoque S-SDLC)
Durante el diseño y desarrollo de las aplicaciones individuales, se aplicaron medidas de seguridad preventivas basadas en el Ciclo de Vida de Desarrollo de Software Seguro (S-SDLC):

* **Validación Estricta de Entradas (Input Validation):** En módulos como el de Inventario, se sanitizan los formularios asegurando que el stock o los precios no sean negativos y tengan longitudes mínimas lógicas. Esto previene inyecciones y fallos lógicos en el backend.
* **Manejo de Excepciones:** Se capturan errores (como `ValueError` al castear tipos de datos) para evitar que la aplicación arroje *stack traces* (trazas de error) en la pantalla del usuario, lo cual revelaría información sensible sobre la infraestructura.
* **Control de Acceso Basado en Roles (RBAC):** Se ha diseñado una arquitectura donde el módulo de usuarios gobierna la autenticación. [cite_start]Se establecen fronteras claras: los administradores tienen permisos CRUD completos, mientras que los usuarios estándar tienen accesos limitados de solo lectura[cite: 664, 665].
* [cite_start]**Aislamiento por Contenedores:** Al utilizar Docker base `python:3.11-slim`[cite: 48], se reduce la superficie de ataque del sistema operativo subyacente al mínimo indispensable.

---

## 3. Guía Paso a Paso: Creación de la App con DevSecOps

Para evolucionar este proyecto hacia un modelo **DevSecOps**, la seguridad deja de ser una fase final y se inyecta en cada etapa del ciclo de vida (Shift-Left Security).

### Diagrama de Flujo S-SDLC / DevSecOps en nuestro Proyecto:
```text
[PLANIFICACIÓN] --> [CÓDIGO] --> [CONSTRUCCIÓN] --> [PRUEBAS] --> [DESPLIEGUE] --> [MONITOREO]
      ↑                ↑               ↑               ↑               ↑               ↑
 Threat Modeling   Linters (SAST)  Escaneo Imagen   DAST / Pentest  IAM / Secrets  Análisis Logs
# proyecto-integrado-grupo3
