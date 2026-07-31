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


@router.get("/{tarea_id}", response_model=TareaResponse)
def obtener_tarea(tarea_id: int):
    tarea = tareas_db.get(tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea


@router.put("/{tarea_id}", response_model=TareaResponse)
def editar_tarea(tarea_id: int, datos: TareaCreate):
    tarea = tareas_db.get(tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    if datos.usuario_id not in usuarios_db:
        raise HTTPException(status_code=404, detail="El usuario indicado no existe")

    tarea.update(datos.model_dump())
    return tarea


@router.delete("/{tarea_id}", status_code=204)
def eliminar_tarea(tarea_id: int):
    if tarea_id not in tareas_db:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    del tareas_db[tarea_id]
