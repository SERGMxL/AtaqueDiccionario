#🔓 Ataque de Diccionario a Archivos ZIP

Un script educativo en Python diseñado para ilustrar cómo funciona un ataque de diccionario simple contra un archivo .zip protegido por contraseña. El propósito de esta herramienta es puramente académico, ideal para estudiantes y entusiastas de la ciberseguridad que deseen comprender los conceptos básicos de la vulnerabilidad de contraseñas.

🚀 Características
Ataque por Diccionario: Prueba sistemáticamente cada contraseña de una lista proporcionada.

Barra de Progreso: Visualiza el progreso del ataque en tiempo real gracias a la librería tqdm.

Fácil de Usar: Código claro y comentado para facilitar el aprendizaje y la modificación.

Manejo de Errores: Incluye verificaciones básicas para archivos no encontrados.

Educativo: Creado específicamente para demostrar un concepto fundamental de la seguridad informática.

🛠️ Requisitos Previos
Para ejecutar este script, necesitarás tener instalado lo siguiente:

Python 3.6 o superior.

La librería tqdm.

⚙️ Instalación
Clona el repositorio:

Bash

git clone https://github.com/SERGMxL/AtaqueDiccionario.git
Navega al directorio del proyecto:

Bash

cd AtaqueDiccionario
Instala las dependencias necesarias:

Bash

pip install tqdm
📖 ¿Cómo Usarlo?
Prepara tus archivos:

Ten a la mano el archivo .zip que deseas probar.

Prepara un archivo de texto (.txt) que servirá como diccionario, con una contraseña por línea.

Configura el script:

Abre el archivo principal de Python (.py).

Modifica las siguientes variables con las rutas a tus archivos:

Python

# --- CONFIGURACIÓN ---
ruta_zip = "tu_archivo.zip" 
ruta_diccionario = "tu_diccionario.txt"
# ---------------------
Ejecuta el script:

Abre una terminal en el directorio del proyecto y ejecuta:

Bash

python unzip.py
El programa comenzará a probar las contraseñas del diccionario. Si encuentra la correcta, la mostrará en la terminal y finalizará.

⚠️ Descargo de Responsabilidad y Uso Ético
Esta herramienta ha sido creada con fines estrictamente educativos para demostrar una vulnerabilidad de seguridad.

NO utilices este script en archivos para los que no tienes permiso explícito.

El uso no autorizado de herramientas de este tipo es ilegal y no ético.

El autor de este repositorio no se hace responsable del mal uso de esta herramienta.

El conocimiento es poder. Úsalo de manera responsable.
