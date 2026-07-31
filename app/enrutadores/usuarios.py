from fastapi import APIRouter, HTTPException

from app.almacenamiento import siguiente_id_usuario, tareas_db, usuarios_db
from app.modelos.usuario import UsuarioConTareas, UsuarioCreate, UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=UsuarioResponse, status_code=201)
def crear_usuario(usuario: UsuarioCreate):
    correo_existente = any(u["correo"] == usuario.correo for u in usuarios_db.values())
    if correo_existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    nuevo_id = siguiente_id_usuario()
    nuevo_usuario = {"id": nuevo_id, **usuario.model_dump()}
    usuarios_db[nuevo_id] = nuevo_usuario
    return nuevo_usuario


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios():
    return list(usuarios_db.values())


@router.get("/{usuario_id}", response_model=UsuarioConTareas)
def obtener_usuario(usuario_id: int):
    usuario = usuarios_db.get(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    tareas_usuario = [t for t in tareas_db.values() if t["usuario_id"] == usuario_id]
    return {**usuario, "tareas": tareas_usuario}
