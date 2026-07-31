import os

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://usuario:contraseña@localhost:5432/gestion_tareas",
)

engine = create_engine(DATABASE_URL, echo=True)


def crear_tablas() -> None:
    """Crea las tablas en la base de datos a partir de los modelos SQLModel."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependencia de FastAPI: abre una sesión y la cierra al terminar el request."""
    with Session(engine) as session:
        yield session
