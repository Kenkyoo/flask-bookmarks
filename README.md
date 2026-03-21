# 📌 Bookmarks Manager

Aplicación web para guardar y organizar marcadores (bookmarks) personales. Desarrollada con Flask y SQLite, con interfaz usando Bulma CSS.

## Descripción

Permite a los usuarios registrarse, iniciar sesión y gestionar sus propios marcadores: guardar el nombre del sitio y su URL, editarlos y eliminarlos.

**Tecnologías usadas:**
- Python / Flask
- SQLite
- Bulma CSS
- Waitress (WSGI server)

---

## Instalación local

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -e .
```

### 4. Inicializar la base de datos

```bash
flask --app flaskr init-db
```

### 5. Ejecutar la aplicación

```bash
flask --app flaskr run
```

Abrí el navegador en `http://localhost:5000`

---

## Deploy en Render

### 1. Subir el proyecto a GitHub

### 2. Crear un Web Service en [Render](https://render.com) conectado al repositorio

### 3. Configurar los comandos

| Campo | Valor |
|-------|-------|
| Build Command | `pip install -e . && flask --app flaskr init-db` |
| Start Command | `waitress-serve --host=0.0.0.0 --port=10000 wsgi:app` |

### 4. Agregar variable de entorno

| Clave | Valor |
|-------|-------|
| `SECRET_KEY` | un-valor-secreto-aleatorio |

> ⚠️ **Nota:** La base de datos SQLite es efímera en Render, los datos se borran al reiniciar el servicio. Apto para proyectos personales o portfolios.

---

## Screenshots

_Próximamente_

---

## Licencia

MIT
