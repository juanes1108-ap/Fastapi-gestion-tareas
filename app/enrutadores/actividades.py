from fastapi import APIRouter, HTTPException

from app.almacenamiento import actividades_db, siguiente_id_actividad, tareas_db
from app.modelos.actividad import ActividadCreate, ActividadResponse, ActividadUpdate

router = APIRouter(tags=["Actividades"])


@router.post(
    "/tareas/{tarea_id}/actividades/",
    response_model=ActividadResponse,
    status_code=201,
)
def crear_actividad(tarea_id: int, actividad: ActividadCreate):
    if tarea_id not in tareas_db:
        raise HTTPException(status_code=404, detail="La tarea indicada no existe")

    nuevo_id = siguiente_id_actividad()
    datos = actividad.model_dump()
    datos["tarea_id"] = tarea_id  # el tarea_id viene de la URL, no del cuerpo
    nueva_actividad = {"id": nuevo_id, **datos}
    actividades_db[nuevo_id] = nueva_actividad
    return nueva_actividad


@router.get("/actividades/", response_model=list[ActividadResponse])
def listar_actividades():
    return list(actividades_db.values())


@router.get("/actividades/{actividad_id}", response_model=ActividadResponse)
def obtener_actividad(actividad_id: int):
    actividad = actividades_db.get(actividad_id)
    if not actividad:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    return actividad


@router.put("/actividades/{actividad_id}", response_model=ActividadResponse)
def editar_actividad(actividad_id: int, datos: ActividadCreate):
    actividad = actividades_db.get(actividad_id)
    if not actividad:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")

    if datos.tarea_id not in tareas_db:
        raise HTTPException(status_code=404, detail="La tarea indicada no existe")

    actividad.update(datos.model_dump())
    return actividad


@router.patch("/actividades/{actividad_id}", response_model=ActividadResponse)
def actualizar_estado_actividad(actividad_id: int, cambio: ActividadUpdate):
    actividad = actividades_db.get(actividad_id)
    if not actividad:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")

    actividad["completada"] = cambio.completada
    return actividad


@router.delete("/actividades/{actividad_id}", status_code=204)
def eliminar_actividad(actividad_id: int):
    if actividad_id not in actividades_db:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")

    del actividades_db[actividad_id]