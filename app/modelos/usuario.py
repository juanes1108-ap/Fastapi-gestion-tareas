from pydantic import BaseModel, EmailStr

from app.modelos.tarea import TareaResponse


class UsuarioCreate(BaseModel):
    nombre: str
    correo: EmailStr


class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    correo: EmailStr


class UsuarioConTareas(UsuarioResponse):
    tareas: list[TareaResponse] = []
