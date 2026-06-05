Actividad 3: Diseño del Ciclo de Vida de Software Seguro (S-SDLC) y Flujo DevSecOps: GRUPO 3. Ignacio Pérez, Alejandro Rodriguez, Diego Argente y Ricardo Moreno

1. Enfoque del Proyecto Grupal y Modelo de Amenazas

En seguridad de software se aplica el principio de que la cadena es tan fuerte como el más débil de sus eslabones. Si un atacante consigue explotar una vulnerabilidad en un servicio secundario, utilizará ese contenedor comprometido como pivote dentro de la red interna de Docker para atacar los módulos contiguos y extraer información sensible o evadir el control del servicio de usuarios.

2. Diseño del Pipeline DevSecOps

Para mitigar estos riesgos de forma automática antes de que el código llegue a producción, hemos ideado un flujo de inspección en el repositorio de GitHub en 5 partes:

- Análisis SCA Nativo (GitHub Dependabot). Monitoriza los archivos de dependencias en segundo plano. Su objetivo es detectar de forma pasiva librerías obsoletas que tengan fallos de seguridad públicos registrados antes de construir las imágenes del sistema.

- Análisis SAST de Código (Bandit). Inspecciona de forma estática los scripts de Python en busca de código inseguro o funciones peligrosas escritas por los desarrolladores que dejen la aplicación expuesta a inyecciones lógicas.

- Hardening de Configuración (Bandit Environment Check). Evalúa que los parámetros de despliegue del framework de desarrollo cumplan con las buenas prácticas de producción, persiguiendo descuidos habituales como dejar herramientas de depuración abiertas a cualquiera.

- Análisis SCA de Entorno (Safety Check). Actúa como un segundo control de dependencias complementario a Dependabot dentro del pipeline de integración continua, bloqueando la compilación si detecta paquetes peligrosos en los ficheros de requisitos.

- Escaneo de Secretos e Infraestructura (Trivy Filesystem Scan). Analiza los archivos de configuración y la estructura del proyecto en busca de credenciales e identificadores hardcodeados en texto plano, además de detectar residuos o metadatos de entornos de desarrollo locales.

3. Riesgos y Mitigación

Al contrastar nuestro repositorio integrado frente al escenario vulnerable, definimos la siguiente estrategia de remediación:

- Librerías obsoletas: En la app de inventario vulnerable se forzó el uso de Flask==0.12.2. Esto expone el sistema a ataques de denegación de servicio (DoS) y manipulación de registros de auditoría. En el proyecto definitivo se solucionó actualizando a Flask==3.0.0.

- Privilegios en contenedores: Para evitar que un atacante rompa el aislamiento del contenedor y tome el control del servidor host, se modificó la configuración individual de usuarios, forzando el uso de usuarios sin privilegios (USER appuser) en los entornos de producción.

- Claves expuestas y archivos residuales: El entorno vulnerable incluía una SECRET_KEY explícita en el Docker Compose y archivos ocultos locales. En la versión limpia saneamos el directorio, externalizamos los secretos a variables de entorno protegidas e implementamos un .gitignore estricto.

4. Evaluación Práctica de Seguridad mediante Herramientas de GitHub

Para comprobar la efectividad del flujo diseñado, hemos configurado y ejecutado estas 5 herramientas sobre el repositorio vulnerable.

4.1.  Resultados del Escaneo Pasivo (SCA Nativo con Dependabot)

Al activar la herramienta nativa en la pestaña Security, el analizador procesó de inmediato el archivo app_inventario/requirements.txt.

- Resultado: Saltó una alerta crítica por el uso de Flask==0.12.2. Identificó el fallo público CVE-2018-1000656, advirtiendo de que el servidor de desarrollo Werkzeug asociado no sanitiza adecuadamente los saltos de línea en las cabeceras, permitiendo ataques de inyección de logs y división de respuesta HTTP.

4.2. Resultados del Análisis de Código (SAST con Bandit)

Ejecutamos el analizador estático integrado mediante GitHub Actions para revisar los ficheros lógicos de las aplicaciones: bandit -r app_notas/ app_inventario/ app_usuarios/ app_tareas/

- Resultado en Consola (Fallo de Código):
   Error: [B102:exec_used] Use of exec detected.
   Severity: High   Confidence: High
   CWE: CWE-78 (Insecure Execution)
   Ubicación: app_notas/app/main.py:14
   Descripción: Se detectó el uso de la función nativa 'exec' procesando 
   entradas de texto. Esto permite la inyección y ejecución de comandos arbitrarios.


4.3. Resultados de Hardening de Entorno (Bandit Config Check)

En la misma ejecución de Bandit dentro del pipeline de GitHub, la herramienta evaluó el estado de inicialización del servidor web.

- Resultado en Consola (Fallo de Configuración):
   Error: [B201:flask_debug_true] A Flask app appears to be run with debug=True.
   Severity: High   Confidence: High
   CWE: CWE-94 (Code Injection)
   Ubicación: app_inventario/app/main.py:42
   Descripción: El modo debug está activo en producción. Esto expone el depurador 
   interactivo de Werkzeug, permitiendo a cualquier usuario externo ejecutar código Python en el servidor.


4.4. Resultados del Bloqueo del Pipeline (SCA con Safety Check)

Para asegurar que los entornos locales no instalen dependencias corruptas antes de compilar las imágenes, el paso de Safety analizó los paquetes del proyecto.

- Resultado en Consola (Pipeline Abortado):
--> Lanzando analizador de librerías en app_inventario/requirements.txt
[VULNERABILIDAD ENCONTRADA] -> Flask==0.12.2
ID: CVE-2019-1010083 (Severidad: Media-Alta)
Detalle: Riesgo de denegación de servicio (DoS) por consumo desmedido de memoria 
RAM al procesar peticiones multiparte maliciosas (Multipart encoding).
Resultado del paso: Error crítico detectado. Compilación cancelada.


4.5. Resultados de Fugas de Secretos e Infraestructura (Trivy Filesystem Scan)

Para solventar las restricciones de visibilidad de las cuentas personales, añadimos la acción automatizada de Trivy para revisar de arriba a abajo el sistema de archivos del repositorio en busca de credenciales harcodeadas y archivos huérfanos.
- Resultado en Consola (Tabla de Seguridad):

Target: . (Filesystem Scan)

Componente 
	Severidad 
	Anomalía 
	Descripción 
	app_notas/.abacus.donotdelete
	LOW 
	TRV-MISC-001 
	Archivo oculto o residual de desarrollo
	app_usuarios/docker-compose
	CRITICAL 
	TRV-SEC-042
	Se encontró una SECRET_KEY expuesta en el .yml

5. Justificación de las Modificaciones Introducidas (Sembrado de Fallos)

Tal como exige el guión de la práctica de la unidad, detallamos los cambios que introdujimos intencionadamente en la estructura para validar las herramientas:

- Forzado de librería vulnerable: Reemplazamos la versión segura de Flask por la 0.12.2 en el módulo de inventario para poner a prueba los motores SCA (Dependabot y Safety). Ambos cumplieron cazando el fallo de denegación de servicio y la vulnerabilidad en el manejo de logs.

- Inyección de malas prácticas: Añadimos la función dinámica exec() en la app de notas y el parámetro debug=True en la de inventario. Buscábamos simular los descuidos de configuración más habituales para comprobar que los motores SAST (Bandit) interceptan las vulnerabilidades antes de desplegar.

- Fuga de credenciales explícita: Escribimos la contraseña de firma de sesiones directamente en el archivo de orquestación de Docker en lugar de llamarla desde un entorno protegido. Con esto obligamos al análisis de infraestructura de Trivy a reportar una alerta crítica por exposición de secretos en texto plano.

7. Conclusión Técnica

La ejecución demuestra que el repositorio vulnerable habría sido completamente interceptado y bloqueado en un entorno DevSecOps real. Por el contrario, al procesar estas mismas cinco técnicas sobre nuestro proyecto-integrado-grupo3-main, el pipeline devuelve un estado limpio. Esto confirma que las actualizaciones de versión, el borrado de residuos y el aislamiento de claves mediante variables de entorno corrigen de raíz todas las deficiencias detectadas.
