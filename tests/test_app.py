"""
Tests básicos para la API de tareas
"""
import pytest
from fastapi.testclient import TestClient
from app import app

# Cliente de pruebas
client = TestClient(app)

def test_root():
    """Test del endpoint raíz"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    """Test del health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_get_all_tasks():
    """Test obtener todas las tareas"""
    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert len(tasks) >= 3

def test_get_task_by_id():
    """Test obtener tarea por ID"""
    response = client.get("/tasks/1")
    assert response.status_code == 200
    task = response.json()
    assert task["id"] == 1
    assert "title" in task

def test_get_task_not_found():
    """Test tarea no encontrada"""
    response = client.get("/tasks/999")
    assert response.status_code == 404

def test_create_task():
    """Test crear nueva tarea"""
    new_task = {
        "title": "Nueva tarea de prueba",
        "description": "Descripción de prueba",
        "completed": False
    }
    response = client.post("/tasks", json=new_task)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == new_task["title"]
    assert "id" in data

def test_update_task():
    """Test actualizar tarea"""
    update_data = {
        "title": "Tarea actualizada",
        "description": "Nueva descripción",
        "completed": True
    }
    response = client.put("/tasks/1", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["completed"] == True

def test_delete_task():
    """Test eliminar tarea"""
    # Primero crear una tarea para eliminar
    new_task = {
        "title": "Tarea a eliminar",
        "description": "Para borrar",
        "completed": False
    }
    create_response = client.post("/tasks", json=new_task)
    task_id = create_response.json()["id"]
    
    # Eliminar la tarea
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    
    # Verificar que ya no existe
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404

def test_create_task_validation():
    """Test validación al crear tarea"""
    invalid_task = {
        "title": "",  # Título vacío (inválido)
        "description": "Test"
    }
    response = client.post("/tasks", json=invalid_task)
    assert response.status_code == 422  # Validation error