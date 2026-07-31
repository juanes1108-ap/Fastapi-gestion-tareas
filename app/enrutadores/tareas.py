from fastapi import APIRouter, HTTPException

from app.almacenamiento import siguiente_id_tarea, tareas_db, usuarios_db
from app.modelos.tarea import TareaCreate, TareaResponse

router = APIRouter(prefix="/tareas", tags=["Tareas"])


@router.post("/", response_model=TareaResponse, status_code=201)
def crear_tarea(tarea: TareaCreate):
    if tarea.usuario_id not in usuarios_db:
        raise HTTPException(status_code=404, detail="El usuario indicado no existe")

    nuevo_id = siguiente_id_tarea()
    nueva_tarea = {"id": nuevo_id, **tarea.model_dump()}
    tareas_db[nuevo_id] = nueva_tarea
    return nueva_tarea


@router.get("/", response_model=list[TareaResponse])
def listar_tareas():
    return list(tareas_db.values())
