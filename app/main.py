from fastapi import FastAPI
from datetime import datetime, timezone
from fastapi import status
from app.schemas import TaskCreate, TaskRead

app = FastAPI(title="Taskflow API", description="API inicial para la gestión de tareas.")

@app.get("/health", summary="Estado del servidor", description="Verifica que el servicio está operativo.")
def get_health():
    return {"status": "ok"}

@app.get("/version", summary="Versión de la API", description="Devuelve la versión de despliegue actual.")
def get_version():
    return {"version": "1.0.0"}

@app.get("/ping", summary="Prueba de conectividad", description="Endpoint simple para probar latencia.")
def get_ping():
    return {"ping": "pong"}
@app.post(
    "/tasks",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear tarea temporal (Simulado)"
)
def create_task(task: TaskCreate) -> TaskRead:
    return TaskRead(
        id=1,
        title=task.title,
        description=task.description,
        project_id=task.project_id,
        completed=False,
        created_at=datetime.now(timezone.utc)
    )