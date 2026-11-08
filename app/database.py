from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión para la base de datos SQLite local
SQLALCHEMY_DATABASE_URL = "sqlite:///./taskflow.db"

# Motor de base de datos (check_same_thread=False es necesario para SQLite en FastAPI)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Fábrica de sesiones locales para las peticiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para construir los modelos ORM
Base = declarative_base()


# Dependencia get_db: abre la sesión, la cede al endpoint y se asegura de cerrarla al terminar
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()