from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modelos.tarea import Tarea


class ActividadBase(SQLModel):
    nombre: str
    descripcion: str
    estado: str
    fecha: date
    completada: bool = False
    tarea_id: int = Field(foreign_key="tareas.id")


class Actividad(ActividadBase, table=True):
    __tablename__ = "actividades"

    id: Optional[int] = Field(default=None, primary_key=True)
    tarea: "Tarea" = Relationship(back_populates="actividades")


class ActividadCreate(ActividadBase):
    pass


class ActividadResponse(ActividadBase):
    id: int


class ActividadUpdate(SQLModel):
    completada: bool
