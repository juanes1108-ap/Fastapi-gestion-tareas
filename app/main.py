from fastapi import FastAPI

from app.database import crear_tablas
from app.enrutadores import actividades, tareas, usuarios

app = FastAPI(title="Gestión de Tareas", version="1.0.0")


@app.on_event("startup")
def al_iniciar():
    crear_tablas()


app.include_router(usuarios.router)
app.include_router(tareas.router)
app.include_router(actividades.router)


@app.get("/")
def raiz():
    return {"mensaje": "API de gestión de tareas funcionando"}
