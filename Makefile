# Makefile
.PHONY: help install test lint security clean package all

PYTHON := python3
PIP := pip3

help:
	@echo "════════════════════════════════════════════"
	@echo "  FastAPI Lambda - Comandos Disponibles"
	@echo "════════════════════════════════════════════"
	@echo "  make install   - Instalar dependencias"
	@echo "  make test      - Ejecutar tests"
	@echo "  make lint      - Análisis de código"
	@echo "  make security  - Auditoría de seguridad"
	@echo "  make package   - Empaquetar para Lambda"
	@echo "  make clean     - Limpiar archivos"
	@echo "  make all       - Ejecutar todo"
	@echo ""

install:
	@echo " Instalando dependencias..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-dev.txt
	@echo " Instalación completada"

test:
	@echo " Ejecutando tests..."
	pytest tests/ -v --cov=app --cov-report=term --cov-report=html
	@echo " Tests completados"

lint:
	@echo " Analizando código..."
	pylint app.py --disable=C0114,C0116 || true
	@echo " Análisis completado"

security:
	@echo " Auditoría de seguridad..."
	bandit -r . -ll --exclude ./tests,./venv || true
	@echo " Auditoría completada"

package:
	@echo " Empaquetando para Lambda..."
	@rm -rf package lambda.zip
	@mkdir -p package
	@pip install -r requirements.txt -t package/
	@cp app.py package/
	@cd package && zip -r ../lambda.zip . -q
	@echo " Paquete creado: lambda.zip"

clean:
	@echo " Limpiando..."
	@rm -rf __pycache__ .pytest_cache htmlcov .coverage
	@rm -rf package lambda.zip
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo " Limpieza completada"

all: install lint security test package
	@echo " Pipeline completo ejecutado"
