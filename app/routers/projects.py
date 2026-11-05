from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, status
from app.schemas import ProjectCreate, ProjectRead

router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)

@router.post(
    "",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un proyecto"
)
def create_project(project: ProjectCreate) -> ProjectRead:
    return ProjectRead(
        id=1,
        name=project.name,
        description=project.description,
        created_at=datetime.now(timezone.utc)
    )

@router.get(
    "",
    response_model=List[ProjectRead],
    summary="Listar proyectos"
)
def get_projects() -> List[ProjectRead]:
    return [
        ProjectRead(
            id=1,
            name="Rediseño Web TaskFlow",
            description="Migración del backend a FastAPI",
            created_at=datetime.now(timezone.utc)
        )
    ]