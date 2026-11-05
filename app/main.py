import time
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routers import projects, tasks

app = FastAPI(
    title="TaskFlow API",
    description="API modularizada con Middleware y Manejo de Excepciones - Práctica 1.4",
    version="1.4.0"
)

# 1. Configuración de CORS permitiendo el origen del frontend
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 2. Middleware personalizado para medir el tiempo de respuesta (X-Process-Time)
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Middleware transversal que calcula el tiempo transcurrido 
    durante el procesamiento de la petición y añade la cabecera X-Process-Time en ms.
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time"] = f"{process_time:.2f} ms"
    return response


# 3. Manejador global de excepciones no controladas
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Captura cualquier excepción no controlada en la API, evitando 
    exponer el stacktrace al cliente y devolviendo un JSON seguro con código 500.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Ocurrió un error interno en el servidor."}
    )


# Registro de routers por recurso
app.include_router(projects.router)
app.include_router(tasks.router)

@app.get("/health", tags=["system"], summary="Estado del servidor")
def health_check():
    return {"status": "ok"}


# Endpoint auxiliar para probar el exception handler (fuerza un error 500 controlado)
@app.get("/error-test", tags=["system"], summary="Forzar error 500")
def trigger_error():
    raise ValueError("Error interno simulado para pruebas")