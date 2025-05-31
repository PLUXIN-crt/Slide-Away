⚙️ Configuración del Entorno
📋 Requisitos Previos
Python 3.8+
Java 17+
Maven 3.6+
Git
🐍 Configuración del Entorno Virtual (Python)
Navega al directorio del proyecto Django:

cd ferraMasDjango
Crea el entorno virtual:

python -m venv env
Activa el entorno virtual:

.\env\Scripts\activate
🚀 Instalación y Ejecución
1️⃣ Servicio Django (Frontend/Tienda)
Instalación de dependencias
Actualiza pip:

py -m pip install --upgrade pip
Instala los requerimientos:

pip install -r requeriments.txt
Configuración de la base de datos
Crea las migraciones:

py manage.py makemigrations
Aplica las migraciones:

py manage.py migrate
Crea un superusuario (opcional):

py manage.py createsuperuser
Iniciar el servidor Django
py manage.py runserver
El servidor estará disponible en: http://localhost:8000

2️⃣ Servicio Spring Boot (Backend/Gestión)
Compilar el proyecto
Navega al directorio de gestión:

cd gestion
Compila el proyecto (si no existe el JAR):

mvn clean package
Iniciar el servicio
Navega a la carpeta target:

cd target
Ejecuta el JAR:

java -jar gestion-0.0.1-SNAPSHOT.jar
