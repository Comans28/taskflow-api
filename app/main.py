from fastapi import FastAPI
from app.routers import projects, tasks

app = FastAPI(
    title="TaskFlow API",
    description="API modularizada con APIRouter - Práctica 1.3",
    version="1.3.0"
)

# Registro de routers por recurso
app.include_router(projects.router)
app.include_router(tasks.router)

@app.get("/health", tags=["system"], summary="Estado del servidor")
def health_check():
    return {"status": "ok"}