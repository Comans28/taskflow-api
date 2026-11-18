from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)

@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED, summary="Crear un proyecto")
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    db_project = db.query(models.Project).filter(models.Project.name == project.name).first()
    if db_project:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El proyecto ya existe")
    
    new_project = models.Project(name=project.name, description=project.description)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.get("", response_model=List[ProjectRead], summary="Listar proyectos")
def get_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = db.query(models.Project).offset(skip).limit(limit).all()
    return projects

@router.get("/{id}", response_model=ProjectRead, summary="Detalle de un proyecto con sus tareas")
def get_project(id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")
    return project

@router.put("/{id}", response_model=ProjectRead, summary="Actualizar un proyecto")
def update_project(id: int, project_update: ProjectUpdate, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")
    
    if project_update.name is not None:
        project.name = project_update.name
    if project_update.description is not None:
        project.description = project_update.description

    db.commit()
    db.refresh(project)
    return project

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar un proyecto")
def delete_project(id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")
    
    db.delete(project)
    db.commit()
    return None