# FastAPI Lambda - API de Tareas

API REST básica con FastAPI desplegada en AWS Lambda.

##  Inicio Rápido
```bash
# Instalar dependencias
make install

# Ejecutar tests
make test

# Ejecutar localmente
uvicorn app:app --reload
```

##  Comandos Make
```bash
make install   # Instalar dependencias
make test      # Ejecutar tests
make lint      # Análisis de código
make security  # Auditoría de seguridad
make package   # Empaquetar para Lambda
make all       # Ejecutar pipeline completo
```

##  Desplegar en AWS

### 1. Configuración inicial
```bash
# Empaquetar
make package

# Configurar AWS
./setup-aws.sh
```

### 2. Configurar secrets en GitHub

En GitHub: Settings → Secrets → New repository secret
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

### 3. Push a GitHub
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

##  Probar la API
```bash
# Health check
curl https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/health

# Obtener todas las tareas
curl https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/tasks

# Crear tarea
curl -X POST https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Nueva tarea","description":"Test","completed":false}'
```

##  Pipeline CI/CD

El pipeline incluye:
-  Instalación de dependencias
-  Linting con Pylint
-  Auditoría de seguridad con Bandit
-  Tests automatizados con Pytest
-  Empaquetado para Lambda
-  Despliegue automático a AWS

##  Estructura del Proyecto
```
fastapi-lambda-basic/
├── app.py                 # Aplicación FastAPI
├── requirements.txt       # Dependencias
├── requirements-dev.txt   # Deps de desarrollo
├── Makefile              # Automatización
├── pytest.ini            # Config de tests
├── tests/
│   └── test_app.py       # Tests
└── .github/
    └── workflows/
        └── main.yml      # GitHub Actions
```

##  Autor

Cloud Computing y DevOps AWS