from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

# NOTA ARQUITECTÓNICA (Contrato de API vs Persistencia):
# Los schemas definen el contrato de entrada/salida de la API (validación JSON),
# separándolo de los modelos de base de datos (que gestionan la persistencia en tablas).


class ProjectCreate(BaseModel):
    """Schema de entrada para crear un proyecto."""
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombre del proyecto",
        examples=["Rediseño Web TaskFlow"]
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Descripción opcional del proyecto",
        examples=["Migración del backend a FastAPI"]
    )


class ProjectRead(ProjectCreate):
    """Schema de salida para leer un proyecto."""
    id: int = Field(..., description="ID único del proyecto", examples=[1])
    created_at: datetime = Field(..., description="Fecha de creación")

    model_config = ConfigDict(from_attributes=True)


class TaskCreate(BaseModel):
    """Schema de entrada para crear una tarea."""
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Título de la tarea (1 a 100 caracteres)",
        examples=["Modelado con Pydantic"]
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Descripción opcional de la tarea",
        examples=["Crear schemas TaskCreate y TaskRead"]
    )
    project_id: int = Field(
        ...,
        gt=0,
        description="ID del proyecto asociado",
        examples=[1]
    )


class TaskRead(TaskCreate):
    """Schema de salida para leer una tarea."""
    id: int = Field(..., description="ID único de la tarea", examples=[1])
    completed: bool = Field(default=False, description="Estado de la tarea")
    created_at: datetime = Field(..., description="Fecha de creación")

    model_config = ConfigDict(from_attributes=True)