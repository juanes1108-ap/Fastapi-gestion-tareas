from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modelos.actividad import Actividad
    from app.modelos.usuario import Usuario


class TareaBase(SQLModel):
    nombre: str
    descripcion: str
    estado: str
    porcentaje_avance: float
    fecha_inicio: date
    fecha_final: date
    usuario_id: int = Field(foreign_key="usuarios.id")


class Tarea(TareaBase, table=True):
    __tablename__ = "tareas"

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario: "Usuario" = Relationship(back_populates="tareas")
    actividades: list["Actividad"] = Relationship(
        back_populates="tarea",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class TareaCreate(TareaBase):
    pass


class TareaResponse(TareaBase):
    id: int
