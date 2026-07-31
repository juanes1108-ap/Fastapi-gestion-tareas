from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.modelos.usuario import Usuario, UsuarioConTareas, UsuarioCreate, UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=UsuarioResponse, status_code=201)
def crear_usuario(usuario: UsuarioCreate, session: Session = Depends(get_session)):
    correo_existente = session.exec(
        select(Usuario).where(Usuario.correo == usuario.correo)
    ).first()
    if correo_existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    nuevo_usuario = Usuario.model_validate(usuario)
    session.add(nuevo_usuario)
    session.commit()
    session.refresh(nuevo_usuario)
    return nuevo_usuario


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(session: Session = Depends(get_session)):
    return session.exec(select(Usuario)).all()


@router.get("/{usuario_id}", response_model=UsuarioConTareas)
def obtener_usuario(usuario_id: int, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def editar_usuario(
    usuario_id: int, datos: UsuarioCreate, session: Session = Depends(get_session)
):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    correo_en_uso = session.exec(
        select(Usuario).where(Usuario.correo == datos.correo, Usuario.id != usuario_id)
    ).first()
    if correo_en_uso:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    usuario.nombre = datos.nombre
    usuario.correo = datos.correo
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


@router.delete("/{usuario_id}", status_code=204)
def eliminar_usuario(usuario_id: int, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    session.delete(usuario)
    session.commit()
