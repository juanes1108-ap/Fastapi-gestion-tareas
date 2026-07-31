from datetime import date

from pydantic import BaseModel


class ActividadCreate(BaseModel):
    nombre: str
    descripcion: str
    estado: str
    fecha: date
    completada: bool = False
    tarea_id: int


class ActividadResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str
    estado: str
    fecha: date
    completada: bool
    tarea_id: int


class ActividadUpdate(BaseModel):
    completada: bool
