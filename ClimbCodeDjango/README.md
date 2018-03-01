# Proyecto Django de ClimbCode

- Requisitos

	- Base de datos -> Postgres 10
	- Python 3

- Instrucciones

	1) Instalar virtualenv
	python -m pip install virtualenv
	
	2) En la carpeta que se haya elegido para los entornos
	python -m venv nombre_entorno_virtual
	
	3) Entrar en la carpeta creada, y dentro, a la carpeta Scripts
	cd nombre_entorno_virtual\Scripts
	
	4) Ejecutar el script activate para activar el entorno virtual. De esta manera, las dependencias del paso 5 se instalan en este 	entorno virtual. 	
	activate
	
	5) Instalar las dependencias del proyecto a partir del archivo requirements.txt del repositorio
	pip install -r requirements.txt
	
	6) Cambiar settings.py para adecuarlo a las credenciales de base de datos del entorno en el que se vaya a desarrollar. Debe ser 	Postgres 10, existir una base de datos con nombre climbcode, y un usuario con nombre climbcode (elegir contraseña y ponerla en 	settings.py en el apartado DATABASES)	
	
	7) Arrancar servidor desde la ruta del proyecto donde esté el archivo manage.py
	python manage.py runserver
	
	8) Migrar modelos a la base de datos si es necesario
	python manage.py migrate
	
	9) Crear usuario admin para poder entrar a la parte de administración de la app web
	python manage.py createsuperuser
	
	10) Se debería poder acceder a la aplicación en localhost:8000/web o localhost:8000/admin