## ⚙️ Configuración del Entorno

### 📋 Requisitos Previos
- **Python 3.8+**
- **Java 17+**
- **Maven 3.6+**
- **Git**

---

### 🐍 Configuración del Entorno Virtual (Python)

Navega al directorio del proyecto Django:

```bash
cd ferraMasDjango
Crea el entorno virtual:

bash
Copiar
Editar
python -m venv env
Activa el entorno virtual:

En Windows (PowerShell):

powershell
Copiar
Editar
.\env\Scripts\Activate.ps1
En Windows (CMD):

cmd
Copiar
Editar
.\env\Scripts\activate.bat
En Linux/macOS:

bash
Copiar
Editar
source env/bin/activate
🚀 Instalación y Ejecución
1️⃣ Servicio Django (Frontend/Tienda)
Instalación de dependencias
Actualiza pip:

bash
Copiar
Editar
py -m pip install --upgrade pip
Instala los requerimientos:

bash
Copiar
Editar
pip install -r requeriments.txt
Configuración de la base de datos
Crea las migraciones:

bash
Copiar
Editar
py manage.py makemigrations
Aplica las migraciones:

bash
Copiar
Editar
py manage.py migrate
(Opcional) Crea un superusuario:

bash
Copiar
Editar
py manage.py createsuperuser
Iniciar el servidor Django
bash
Copiar
Editar
py manage.py runserver
El servidor estará disponible en: http://localhost:8000

2️⃣ Servicio Spring Boot (Backend/Gestión)
Compilar el proyecto
Navega al directorio de gestión:

bash
Copiar
Editar
cd gestion
Compila el proyecto (si aún no existe el JAR):

bash
Copiar
Editar
mvn clean package
Iniciar el servicio
Navega a la carpeta target:

bash
Copiar
Editar
cd target
Ejecuta el JAR:

bash
Copiar
Editar
java -jar gestion-0.0.1-SNAPSHOT.jar
