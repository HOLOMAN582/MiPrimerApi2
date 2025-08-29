## Blog API (FastAPI)

API de ejemplo para gestionar usuarios, posts y comentarios usando FastAPI. Utiliza una base de datos en memoria (los datos se pierden al reiniciar) e incluye documentación interactiva.

### Características
- **Usuarios**: crear, listar y obtener por ID
- **Posts**: crear, listar (filtros por tag y autor), obtener, actualizar, eliminar
- **Comentarios**: crear y listar por post
- **Interacciones**: likes y conteo de vistas
- **Búsqueda**: por título, contenido y tags
- **Estadísticas**: totales y promedios

### Requisitos
- Python 3.10+
- pip

### Instalación
1. Abre una terminal en la carpeta raíz del proyecto.
2. Crea y activa un entorno virtual:
   - Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - Linux / macOS (bash/zsh):
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```
3. Instala dependencias:
   ```bash
   pip install fastapi uvicorn
   ```

### Ejecución
Ejecuta el servidor con Uvicorn desde la raíz del proyecto:
```bash
uvicorn mi_primer_api.blog_api:app --reload
```

- Base URL: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Estructura
```text
.
├── mi_primer_api/
│   ├── blog_api.py
│   └── main.py
└── README.md
```

### Endpoints
- **Usuarios**
  - `POST /users`: crear usuario
  - `GET /users`: listar usuarios (`skip`, `limit`)
  - `GET /users/{user_id}`: obtener usuario por ID
- **Posts**
  - `POST /posts`: crear post
  - `GET /posts`: listar posts (filtros `tag`, `author_id`; paginación `skip`, `limit`)
  - `GET /posts/{post_id}`: obtener post (incrementa `views`)
  - `PUT /posts/{post_id}`: actualizar post
  - `DELETE /posts/{post_id}`: eliminar post (borra también sus comentarios)
- **Comentarios**
  - `POST /comments`: crear comentario
  - `GET /posts/{post_id}/comments`: listar comentarios de un post
- **Otros**
  - `POST /posts/{post_id}/like`: dar like a un post
  - `GET /search?q=texto`: buscar por título, contenido o tags
  - `GET /stats`: estadísticas generales
  - `GET /`: información de bienvenida y rutas útiles

### Ejemplos rápidos (cURL)
- Crear usuario:
  ```bash
  curl -X POST "http://127.0.0.1:8000/users" \
       -H "Content-Type: application/json" \
       -d '{
             "username": "alice",
             "email": "alice@example.com",
             "full_name": "Alice Doe",
             "password": "secreto123"
           }'
  ```
- Crear post (usa el `id` del usuario como `author_id`):
  ```bash
  curl -X POST "http://127.0.0.1:8000/posts" \
       -H "Content-Type: application/json" \
       -d '{
             "title": "Mi primer post",
             "content": "Contenido del post...",
             "tags": ["fastapi", "ejemplo"],
             "author_id": "<USER_ID>"
           }'
  ```
- Listar posts con filtros y paginación:
  ```bash
  curl "http://127.0.0.1:8000/posts?tag=fastapi&skip=0&limit=10"
  ```
- Dar like a un post:
  ```bash
  curl -X POST "http://127.0.0.1:8000/posts/<POST_ID>/like"
  ```

### Notas
- La base de datos es en memoria; los datos se reinician al apagar el servidor.
- Usa `skip` y `limit` para paginación donde aplique.

### Mejoras sugeridas
- Persistencia con SQLite/PostgreSQL (SQLModel/SQLAlchemy)
- Autenticación JWT
- Validaciones adicionales (por ejemplo, `EmailStr` para emails)
- Tests automatizados y `requirements.txt`
