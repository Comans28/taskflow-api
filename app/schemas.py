from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

# --- SCHEMAS DE USUARIO ---
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- SCHEMAS DE CATEGORÍA ---
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None

class CategoryRead(CategoryBase):
    id: int

    class Config:
        from_attributes = True


# --- SCHEMAS DE TAREA ---
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    project_id: int
    category_id: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    project_id: Optional[int] = None
    category_id: Optional[int] = None

class TaskRead(TaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- SCHEMAS DE PROYECTO ---
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectRead(ProjectBase):
    id: int
    created_at: datetime
    tasks: list[TaskRead] = []  # Permite listar las tareas asociadas al proyecto

    class Config:
        from_attributes = True


# Actualizamos la referencia circular de CategoryRead para que devuelva sus tareas asociadas
class CategoryReadWithTasks(CategoryRead):
    tasks: list[TaskRead] = []

    class Config:
        from_attributes = True