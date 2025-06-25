#  Event Manager API

Sistema de Gestión de Eventos desarrollado como parte del Trabajo Práctico Integrador de Laboratorio IV.

Permite a los usuarios registrarse, iniciar sesión, inscribirse a eventos y ver sus inscripciones activas o históricas. Los administradores pueden crear, editar y eliminar eventos, así como gestionar las categorías disponibles.

---

## Tecnologías utilizadas

### Backend

- **[FastAPI](https://fastapi.tiangolo.com/)** – Framework para construir la API REST
- **[Pydantic](https://docs.pydantic.dev/)** – Validación de datos
- **[SQLAlchemy](https://www.sqlalchemy.org/)** – ORM para acceso a base de datos
- **JWT (JSON Web Tokens)** – Autenticación segura con tokens
- **PostgreSQL** – Base de datos relacional

### Frontend

- **[Vite](https://vitejs.dev/)** – Herramienta de construcción rápida para proyectos React
- **[React](https://react.dev/)** – Librería para construir interfaces de usuario
- **[Material UI (MUI)](https://mui.com/)** – Framework de componentes para un diseño moderno y accesible

---

##  Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tuusuario/event-manager.git
   cd event-manager

2. Inatala los requerimientos
   ```bash
   pip install -r requirements.txt

3. Correr el servidor de la Api
   ```bash
   python main.py
