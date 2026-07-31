from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.modelos.actividad import (
    Actividad,
    ActividadCreate,
    ActividadResponse,
    ActividadUpdate,
)
from app.modelos.tarea import Tarea

router = APIRouter(tags=["Actividades"])


@router.post(
    "/tareas/{tarea_id}/actividades/",
    response_model=ActividadResponse,
    status_code=201,
)
def crear_actividad(
    tarea_id: int, actividad: ActividadCreate, session: Session = Depends(get_session)
):
    tarea = session.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="La tarea indicada no existe")

    datos = actividad.model_dump()
    datos["tarea_id"] = tarea_id  # el tarea_id viene de la URL, no del cuerpo
    nueva_actividad = Actividad(**datos)
    session.add(nueva_actividad)
    session.commit()
    session.refresh(nueva_actividad)
    return nueva_actividad


@router.get("/actividades/", response_model=list[ActividadResponse])
def listar_actividades(session: Session = Depends(get_session)):
    return session.exec(select(Actividad)).all()


@router.get("/actividades/{actividad_id}", response_model=ActividadResponse)
def obtener_actividad(actividad_id: int, session: Session = Depends(get_session)):
    actividad = session.get(Actividad, actividad_id)
    if not actividad:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    return actividad


@router.put("/actividades/{actividad_id}", response_model=ActividadResponse)
def editar_actividad(
    actividad_id: int,
    datos: ActividadCreate,
    session: Session = Depends(get_session),
):
    actividad = session.get(Actividad, actividad_id)
    if not actividad:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")

    tarea = session.get(Tarea, datos.tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="La tarea indicada no existe")

    for campo, valor in datos.model_dump().items():
        setattr(actividad, campo, valor)

    session.add(actividad)
    session.commit()
    session.refresh(actividad)
    return actividad


@router.patch("/actividades/{actividad_id}", response_model=ActividadResponse)
def actualizar_estado_actividad(
    actividad_id: int, cambio: ActividadUpdate, session: Session = Depends(get_session)
):
    actividad = session.get(Actividad, actividad_id)
    if not actividad:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")

    actividad.completada = cambio.completada
    session.add(actividad)
    session.commit()
    session.refresh(actividad)
    return actividad


@router.delete("/actividades/{actividad_id}", status_code=204)
def eliminar_actividad(actividad_id: int, session: Session = Depends(get_session)):
    actividad = session.get(Actividad, actividad_id)
    if not actividad:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    session.delete(actividad)
    session.commit()
