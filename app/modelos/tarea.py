from datetime import date

from pydantic import BaseModel


class TareaCreate(BaseModel):
    nombre: str
    descripcion: str
    estado: str
    porcentaje_avance: float
    fecha_inicio: date
    fecha_final: date
    usuario_id: int


class TareaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str
    estado: str
    porcentaje_avance: float
    fecha_inicio: date
    fecha_final: date
    usuario_id: int
