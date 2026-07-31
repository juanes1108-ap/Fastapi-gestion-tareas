from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.modelos.tarea import TareaResponse

if TYPE_CHECKING:
    from app.modelos.tarea import Tarea


class UsuarioBase(SQLModel):
    nombre: str
    correo: str = Field(unique=True, index=True)


class Usuario(UsuarioBase, table=True):
    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)
    tareas: list["Tarea"] = Relationship(
        back_populates="usuario",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioResponse(UsuarioBase):
    id: int


class UsuarioConTareas(UsuarioResponse):
    tareas: list[TareaResponse] = []
