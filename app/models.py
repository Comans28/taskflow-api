from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    """Modelo de Usuario en la base de datos."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Category(Base):
    """Modelo de Categoría para clasificar tareas."""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)

    tasks = relationship("Task", back_populates="category")


class Project(Base):
    """Modelo de Proyecto (contenedor de tareas)."""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")


class Task(Base):
    """Modelo de Tarea vinculado a un proyecto y opcionalmente a una categoría."""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True, nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Claves foráneas
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    # Relaciones ORM
    project = relationship("Project", back_populates="tasks")
    category = relationship("Category", back_populates="tasks")