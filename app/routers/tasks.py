from datetime import datetime, timezone
from fastapi import APIRouter, status
from app.schemas import TaskCreate, TaskRead

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.post(
    "",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una tarea"
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