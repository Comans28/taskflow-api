from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import CategoryCreate, CategoryRead, CategoryReadWithTasks, CategoryUpdate

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED, summary="Crear una categoría")
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.name == category.name).first()
    if db_category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La categoría ya existe")
    
    new_category = models.Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("", response_model=List[CategoryRead], summary="Listar categorías")
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = db.query(models.Category).offset(skip).limit(limit).all()
    return categories

@router.get("/{id}", response_model=CategoryReadWithTasks, summary="Detalle de una categoría con sus tareas")
def get_category(id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    return category

@router.put("/{id}", response_model=CategoryRead, summary="Actualizar una categoría")
def update_category(id: int, category_update: CategoryUpdate, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    
    if category_update.name is not None:
        category.name = category_update.name

    db.commit()
    db.refresh(category)
    return category

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar una categoría")
def delete_category(id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    
    db.delete(category)
    db.commit()
    return None