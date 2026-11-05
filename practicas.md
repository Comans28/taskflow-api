# Entregable Práctica 1.1

**Repositorio Git:** https://github.com/Comans28/taskflow-api.git

## Captura de /docs
![Captura Swagger UI](./captura.png)

---

## Práctica 1.2 — Modelado con Pydantic

### Concepto de Schema (Contrato de API) vs Modelo de Base de Datos (Persistencia)
* **Schema (Pydantic - Contrato de API):** Define la estructura, tipos de datos y reglas de validación que la API acepta en las peticiones de entrada (`TaskCreate`, `ProjectCreate`) y devuelve en las respuestas de salida (`TaskRead`, `ProjectRead`). Actúa como el contrato público de comunicación en formato JSON entre el cliente y el servidor.
* **Modelo de Base de Datos (ORM - Persistencia):** Representa las tablas físicas y relaciones dentro del motor de base de datos. Separar los schemas de los modelos de persistencia permite validar datos antes de tocar la base de datos y ocultar campos internos o sensibles sin acoplar la API al esquema de tablas.

### Pruebas de validación en Swagger (`POST /tasks`)

1. **Caso válido (`201 Created`):** Envío de un objeto `TaskCreate` cumpliendo las restricciones de `Field`, devolviendo el objeto `TaskRead` simulado.
![Caso válido 201](cap1.png)

2. **Caso inválido (`422 Unprocessable Content`):** Envío de `"title": ""` incumpliendo la restricción `Field(min_length=1, max_length=100)`.
![Caso inválido 422](cap2.png)
---

## Práctica 1.3 — Organización con APIRouter

### Modularización y Separación de Responsabilidades
* **Uso de APIRouter:** Se han separado las rutas por recurso creando los routers independientes `app/routers/projects.py` y `app/routers/tasks.py`, aplicando prefijos coherentes (`/projects`, `/tasks`) y etiquetas (`tags`).
* **Separación en `main.py`:** El archivo principal `main.py` se ha mantenido limpio de lógica de negocio, limitándose a instanciar la aplicación FastAPI y a registrar los routers mediante `app.include_router(...)`[cite: 10].

### Documentación en Swagger
Vista de la API con los endpoints organizados y agrupados por recursos:
![Swagger APIRouter](cap3.png)