"""
Almacenamiento en memoria que simula las tablas de la base de datos.
En la Actividad 3 (rama v-postgres) esto se reemplaza por PostgreSQL + SQLModel.
"""

usuarios_db: dict[int, dict] = {}
tareas_db: dict[int, dict] = {}
actividades_db: dict[int, dict] = {}

_contador_usuarios = 0
_contador_tareas = 0
_contador_actividades = 0


def siguiente_id_usuario() -> int:
    global _contador_usuarios
    _contador_usuarios += 1
    return _contador_usuarios


def siguiente_id_tarea() -> int:
    global _contador_tareas
    _contador_tareas += 1
    return _contador_tareas


def siguiente_id_actividad() -> int:
    global _contador_actividades
    _contador_actividades += 1
    return _contador_actividades
