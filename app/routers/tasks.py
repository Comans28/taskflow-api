from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED, summary="Crear una tarea")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # Verificar que el proyecto asociado existe
    project = db.query(models.Project).filter(models.Project.id == task.project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El proyecto asociado no existe")
    
    # Si incluye categoría, verificar que existe
    if task.category_id:
        category = db.query(models.Category).filter(models.Category.id == task.category_id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La categoría asociada no existe")

    new_task = models.Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        project_id=task.project_id,
        category_id=task.category_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("", response_model=List[TaskRead], summary="Listar tareas con filtros y paginación")
def get_tasks(
    project_id: Optional[int] = None,
    completed: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.Task)
    
    # Aplicar filtros si se proporcionan en los query params
    if project_id is not None:
        query = query.filter(models.Task.project_id == project_id)
    if completed is not None:
        query = query.filter(models.Task.completed == completed)
        
    tasks = query.offset(skip).limit(limit).all()
    return tasks

@router.get("/{id}", response_model=TaskRead, summary="Detalle de una tarea")
def get_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return task

@router.put("/{id}", response_model=TaskRead, summary="Actualizar una tarea")
def update_task(id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.completed is not None:
        task.completed = task_update.completed
    if task_update.project_id is not None:
        # Verificar proyecto si se actualiza
        project = db.query(models.Project).filter(models.Project.id == task_update.project_id).first()
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El nuevo proyecto asociado no existe")
        task.project_id = task_update.project_id
    if task_update.category_id is not None:
        category = db.query(models.Category).filter(models.Category.id == task_update.category_id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La nueva categoría asociada no existe")
        task.category_id = task_update.category_id

    db.commit()
    db.refresh(task)
    return task

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar una tarea")
def delete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    
    db.delete(task)
    db.commit()
    return None