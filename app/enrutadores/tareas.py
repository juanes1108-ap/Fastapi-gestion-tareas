from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.modelos.tarea import Tarea, TareaCreate, TareaResponse
from app.modelos.usuario import Usuario

router = APIRouter(prefix="/tareas", tags=["Tareas"])


@router.post("/", response_model=TareaResponse, status_code=201)
def crear_tarea(tarea: TareaCreate, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, tarea.usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="El usuario indicado no existe")

    nueva_tarea = Tarea.model_validate(tarea)
    session.add(nueva_tarea)
    session.commit()
    session.refresh(nueva_tarea)
    return nueva_tarea


@router.get("/", response_model=list[TareaResponse])
def listar_tareas(session: Session = Depends(get_session)):
    return session.exec(select(Tarea)).all()


@router.get("/{tarea_id}", response_model=TareaResponse)
def obtener_tarea(tarea_id: int, session: Session = Depends(get_session)):
    tarea = session.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea


@router.put("/{tarea_id}", response_model=TareaResponse)
def editar_tarea(
    tarea_id: int, datos: TareaCreate, session: Session = Depends(get_session)
):
    tarea = session.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    usuario = session.get(Usuario, datos.usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="El usuario indicado no existe")

    for campo, valor in datos.model_dump().items():
        setattr(tarea, campo, valor)

    session.add(tarea)
    session.commit()
    session.refresh(tarea)
    return tarea


@router.delete("/{tarea_id}", status_code=204)
def eliminar_tarea(tarea_id: int, session: Session = Depends(get_session)):
    tarea = session.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    session.delete(tarea)
    session.commit()
