# main.py
# =============================================================================
# API de ejemplo construida con FastAPI.
# Objetivo: exponer un CRUD básico para "usuarios" empleando una lista en memoria.
# Este archivo incluye comentarios detallados que explican cada apartado.
# =============================================================================

# -----------------------------
# 1) IMPORTACIONES
# -----------------------------
# FastAPI: framework para crear APIs. HTTPException: permite devolver errores con códigos HTTP (400, 404, etc.).
from fastapi import FastAPI, HTTPException

# Pydantic (BaseModel, Field): define y valida estructuras de datos de entrada/salida (esquemas).
from pydantic import BaseModel, Field

# typing.List: para anotaciones de tipos (listas de User).
from typing import List


# -----------------------------
# 2) INSTANCIA DE LA APLICACIÓN
# -----------------------------
# Creamos la app FastAPI y configuramos metadatos que se mostrarán en la documentación (Swagger/ReDoc).
app = FastAPI(
    title="API de ejemplo para documentación",            # Título visible en /docs
    description="Ejemplo de una API con autodocumentación y Swagger",  # Descripción en /docs
    version="1.0.0"                                       # Versión de la API
)


# -----------------------------
# 3) MODELO DE DATOS (ESQUEMA)
# -----------------------------
# Definimos la clase User, que representa el cuerpo (payload) esperado en POST/PUT.
# BaseModel activa la validación automática: si llega algo que no cumple el tipo, FastAPI responde 422.
class User(BaseModel):
    # id: entero requerido; Field(...): elipsis ( ... ) indica "obligatorio".
    # examples: se muestra como ejemplo en la documentación de Swagger.
    id: int = Field(..., examples=[1])

    # name: string requerido
    name: str = Field(..., examples=["David Múnera"])

    # email: string requerido (no se valida formato de email aquí; si quieres,
    # podrías usar pydantic EmailStr)
    email: str = Field(..., examples=["david.munera@gmail.com"])


# -----------------------------
# 4) "BASE DE DATOS" EN MEMORIA
# -----------------------------
# Lista que almacenará instancias de User temporalmente (se pierde al reiniciar).
user_db: List[User] = []


# -----------------------------
# 5) ENDPOINT: GET /users
# -----------------------------
# - path: "/users" → ruta del recurso.
# - response_model=List[User]: FastAPI serializa la respuesta según el esquema (lista de User).
# - summary/description/tags: metadatos mostrados en /docs para mejor UX.
# - responses: documentación adicional de posibles respuestas (códigos y descripciones).
@app.get(
    "/users",
    response_model=List[User],
    summary="Obtener todos los usuarios",
    description="Devuelve una lista con todos los usuarios registrados.",
    tags=["Usuarios"],
    responses={
        200: {"description": "Lista de usuarios recuperada exitosamente."}
    }
)
def get_users() -> List[User]:
    """
    Lógica:
    - Retorna la lista completa de usuarios que vive en memoria (user_db).
    - Si no hay usuarios, devuelve lista vacía [] con estado 200.
    """
    return user_db


# -----------------------------
# 6) ENDPOINT: POST /users
# -----------------------------
# - status_code=201: indica creación exitosa.
# - El parámetro "user: User" indica que el cuerpo del request debe coincidir con el modelo User.
# - Validamos que no se repita el 'id' antes de insertar.
@app.post(
    "/users",
    status_code=201,
    summary="Crear un usuario",
    description="Agrega un nuevo usuario a la base de datos simulada.",
    tags=["Usuarios"],
    responses={
        201: {"description": "Usuario creado exitosamente."},
        400: {"description": "ID duplicado."}
    }
)
def crear_user(user: User) -> User:
    """
    Lógica:
    1) Recibe un objeto 'user' (id, name, email) que ya viene validado por Pydantic.
    2) Recorre la 'BD' (lista) para comprobar si el id ya existe.
       - Si existe → lanza HTTP 400 (Bad Request) con mensaje "El ID ya existe".
       - Si no existe → agrega el nuevo usuario a la lista y lo retorna.
    """
    for cada_usuario in user_db:
        if cada_usuario.id == user.id:
            # HTTPException genera una respuesta JSON con {"detail": "..."} y código 400.
            raise HTTPException(status_code=400, detail="El ID ya existe")

    user_db.append(user)
    return user


# -----------------------------
# 7) ENDPOINT: PUT /users/{user_id}
# -----------------------------
# - Ruta con parámetro de path {user_id} → llega como int a la función.
# - update_user: cuerpo con el objeto User completo que reemplazará al existente.
# - response_model=User: devolvemos el objeto actualizado con el mismo esquema.
@app.put(
    "/users/{user_id}",
    response_model=User,
    summary="Actualizar un usuario",
    description="Actualiza completamente un usuario identificado por su ID.",
    tags=["Usuarios"],
    responses={
        200: {"description": "Usuario actualizado correctamente."},
        404: {"description": "ID de usuario no encontrado."}
    }
)
def actualizar_usuario(user_id: int, update_user: User) -> User:
    """
    Lógica:
    1) Buscamos en la lista un usuario con id == user_id.
    2) Si lo encontramos, reemplazamos su entrada por 'update_user' y devolvemos este.
       (Es una actualización total: sobrescribe el registro con el objeto recibido.)
    3) Si no se encuentra, lanzamos HTTP 404 (Not Found).
    """
    for index, usuario_existente in enumerate(user_db):
        if usuario_existente.id == user_id:
            user_db[index] = update_user
            return update_user

    # Si el bucle termina sin retorno, no se halló el usuario.
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


# -----------------------------
# 8) ENDPOINT: DELETE /users/{user_id}
# -----------------------------
# - Elimina el usuario cuyo id coincida con user_id.
# - Devuelve un mensaje de confirmación si existía; 404 si no.
@app.delete(
    "/users/{user_id}",
    summary="Eliminar un usuario",
    description="Elimina un usuario de la base de datos por su ID.",
    tags=["Usuarios"],
    responses={
        200: {"description": "Usuario eliminado correctamente."},
        404: {"description": "ID de usuario no encontrado."}
    }
)
def eliminar_usuario(user_id: int) -> dict:
    """
    Lógica:
    1) Recorremos la lista en busca del usuario con id == user_id.
    2) Si existe → lo eliminamos usando 'del user_db[index]' y retornamos un JSON con mensaje.
    3) Si no existe → levantamos HTTP 404.
    """
    for index, usuario_existente in enumerate(user_db):
        if usuario_existente.id == user_id:
            del user_db[index]
            return {"message": "Usuario eliminado correctamente"}

    raise HTTPException(status_code=404, detail="Usuario no encontrado")


# -----------------------------
# 9) CÓMO EJECUTAR ESTE ARCHIVO
# -----------------------------
# Prerrequisitos (una sola vez):
#   pip install fastapi uvicorn
#
# Ejecutar el servidor (desde la carpeta del archivo):
#   uvicorn main:app --reload
#     - 'main' es el nombre de este archivo sin la extensión .py
#     - 'app' es la variable FastAPI creada arriba
#     - '--reload' recarga automático al guardar cambios (útil en desarrollo)
#
# Endpoints de documentación (se generan solos):
#   Swagger UI: http://127.0.0.1:8000/docs
#   ReDoc:      http://127.0.0.1:8000/redoc
# -----------------------------
