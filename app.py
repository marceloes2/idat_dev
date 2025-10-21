# app.py
"""
API REST básica con FastAPI para AWS Lambda
Cloud Computing y DevOps AWS
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from mangum import Mangum

# Crear aplicación FastAPI
app = FastAPI(
    title="API de Tareas - DevOps AWS",
    description="API REST simple para gestión de tareas",
    version="1.0.0"
)

# Modelo de datos
class Task(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., max_length=500)
    completed: bool = False

# Base de datos en memoria (simplificada)
tasks_db = [
    Task(id=1, title="Aprender FastAPI", description="Estudiar FastAPI para AWS Lambda", completed=False),
    Task(id=2, title="Configurar GitHub Actions", description="Crear pipeline CI/CD", completed=False),
    Task(id=3, title="Desplegar en AWS", description="Desplegar usando Lambda", completed=False)
]

# ============================================
# ENDPOINTS
# ============================================

@app.get("/")
def root():
    """Endpoint raíz"""
    return {
        "message": "API de Tareas - Cloud Computing y DevOps AWS",
        "version": "1.0.0",
        "endpoints": ["/tasks", "/tasks/{id}", "/health"]
    }

@app.get("/health")
def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "service": "fastapi-lambda",
        "tasks_count": len(tasks_db)
    }

@app.get("/tasks", response_model=List[Task])
def get_all_tasks():
    """Obtener todas las tareas"""
    return tasks_db

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    """Obtener una tarea por ID"""
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"Tarea {task_id} no encontrada")
    return task

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: Task):
    """Crear una nueva tarea"""
    # Generar ID automático
    new_id = max([t.id for t in tasks_db], default=0) + 1
    task.id = new_id
    tasks_db.append(task)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: Task):
    """Actualizar una tarea"""
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"Tarea {task_id} no encontrada")
    
    task.title = task_update.title
    task.description = task_update.description
    task.completed = task_update.completed
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Eliminar una tarea"""
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"Tarea {task_id} no encontrada")
    
    tasks_db.remove(task)
    return {"message": f"Tarea {task_id} eliminada exitosamente"}

# Handler para AWS Lambda
handler = Mangum(app)