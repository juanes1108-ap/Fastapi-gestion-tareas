# fastapi-gestion-tareas

API RESTful desarrollada con FastAPI para la gestión de usuarios, tareas y
actividades. Proyecto realizado como parte del Plan de Mejoramiento de la
competencia 38368 (Análisis y Desarrollo de Software - SENA, ficha 3407181).

## Descripción

El proyecto se desarrolla en dos fases de persistencia:

1. **Fase en memoria** (`v-memoria`): los datos se almacenan en listas/diccionarios
   de Python mientras se valida la lógica y los esquemas con Pydantic.
2. **Fase con PostgreSQL** (`v-postgres`): se migra la persistencia a una base de
   datos real usando SQLModel como ORM.

## Modelo de datos

- **Usuarios**: id, nombre, correo (único)
- **Tareas**: id, nombre, descripción, estado, porcentaje de avance, fecha de
  inicio, fecha final — asociadas a un usuario
- **Actividades**: id, nombre, descripción, estado, fecha, completada —
  asociadas a una tarea

### Diagrama Entidad-Relación (MER)

```mermaid
erDiagram
    USUARIOS ||--o{ TAREAS : tiene
    TAREAS ||--o{ ACTIVIDADES : contiene
    USUARIOS {
        int id PK
        string nombre
        string correo UK
    }
    TAREAS {
        int id PK
        int usuario_id FK
        string nombre
        string descripcion
        string estado
        float porcentaje_avance
        date fecha_inicio
        date fecha_final
    }
    ACTIVIDADES {
        int id PK
        int tarea_id FK
        string nombre
        string descripcion
        string estado
        date fecha
        bool completada
    }
```

## Estructura de ramas

- `main`: rama principal, solo contiene código estable después de los merges.
- `v-memoria`: desarrollo de la Actividad 2 (persistencia en memoria).
- `v-postgres`: desarrollo de la Actividad 3 (migración a PostgreSQL).

## Estructura del proyecto

```
fastapi-gestion-tareas/
├── app/
│   ├── modelos/       # Esquemas Pydantic / modelos SQLModel
│   ├── enrutadores/    # Endpoints agrupados por recurso
│   └── main.py         # Punto de entrada de la aplicación
├── requirements.txt
├── .gitignore
├── .env                # (solo en v-postgres, no versionado)
└── README.md
```

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/juanes1108-ap/fastapi-gestion-tareas.git
   cd fastapi-gestion-tareas
   ```

2. Crear y activar el entorno virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # Linux / Mac
   .venv\Scripts\activate         # Windows
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecutar el servidor de desarrollo:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Documentación interactiva disponible en `http://127.0.0.1:8000/docs`.

## Configuración de base de datos (rama v-postgres)

Crear un archivo `.env` en la raíz del proyecto con la variable de conexión:

```
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_bd
```

## Autor

Juan Esteban Angulo Perez — ficha 3407181, Tecnología en Análisis y
Desarrollo de Software, SENA.
