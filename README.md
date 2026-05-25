# Task Master IA — Flask + SQLite3

## Descripción

Este proyecto reproduce el ejercicio del video solicitado: una aplicación web CRUD desarrollada con Python, Flask y SQLite3. La aplicación permite crear, consultar, actualizar y eliminar tareas.

## Tecnologías usadas

- Python
- Flask
- Flask-SQLAlchemy
- SQLite3
- HTML
- CSS
- Jinja2
- Gunicorn
- Heroku (opción gratuita render.com)

## Personalización realizada

Además de reproducir el CRUD base del tutorial, se agregaron estos cambios personalizados:

1. Diseño oscuro moderno con CSS propio.
2. Campo de prioridad para cada tarea: Alta, Media o Baja.
3. Estado de tarea completada o pendiente.
4. Ruta adicional para cambiar el estado de una tarea.
5. Validación mínima: la tarea debe tener al menos 3 caracteres.
6. Bitácora de eventos con `logging`.

## Estructura del proyecto

```text
Task-Master/
│
├── app.py
├── requirements.txt
├── Procfile
├── README.md
├── runtime.txt
├── test.db
│
├── templates/
│   ├── base.html
│   ├── index.html
│   └── update.html
│
└── static/
    └── css/
        └── main.css
```

## Ejecución local

### 1. Crear entorno virtual

```bash
python -m venv env
```

### 2. Activar entorno virtual

Windows:

```bash
env\Scripts\activate
```

Mac/Linux:

```bash
source env/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar aplicación

```bash
python app.py
```

### 5. Abrir en navegador

```text
http://127.0.0.1:5000
```

## Despliegue en Heroku

### 1. Iniciar sesión

```bash
heroku login
```

### 2. Crear aplicación

```bash
heroku create nombre-de-tu-app
```

### 3. Subir proyecto

```bash
git init
git add .
git commit -m "Proyecto Flask CRUD"
git push heroku main
```

Si tu rama se llama `master`:

```bash
git push heroku master
```

### 4. Abrir aplicación

```bash
heroku open
```

## Enlace del proyecto desplegado

Pegar aquí el enlace generado por Heroku:

```text
https://TU-APP.herokuapp.com/
```
```text
render.com
https://task-master-flask.onrender.com/
```
## Nota

La base de datos SQLite3 se genera automáticamente al ejecutar `app.py`. Se incluye `test.db` como evidencia local del proyecto.

## 👨‍💻 Autor
Antonio Nicolás Toro González 🎓 Maestría en Inteligencia Artificial para la Transformación Digital 🏫 Instituto Internacional de Aguascalientes

## 👨‍🏫 Tutor Académico: Dr. Jonás Velasco Álvarez

## 📜 Licencia Académica
Material desarrollado con fines educativos y de formación avanzada en: Desarrollo e implementación de una aplicación web CRUD con Flask y SQLite3.
