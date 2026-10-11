from fastapi import FastAPI

app = FastAPI(title="Taskflow API", description="API inicial para la gestión de tareas.")

@app.get("/health", summary="Estado del servidor", description="Verifica que el servicio está operativo.")
def get_health():
    return {"status": "ok"}

@app.get("/version", summary="Versión de la API", description="Devuelve la versión de despliegue actual.")
def get_version():
    return {"version": "1.0.0"}

@app.get("/ping", summary="Prueba de conectividad", description="Endpoint simple para probar latencia.")
def get_ping():
    return {"ping": "pong"}