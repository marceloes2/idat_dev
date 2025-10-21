# Script: deploy.sh
cat > deploy.sh << 'EOF'
#!/bin/bash
set -e

FUNCTION_NAME="fastapi-tasks-api"
REGION="us-east-1"

echo " Empaquetando aplicación..."
make package

echo " Desplegando a AWS Lambda..."
aws lambda update-function-code \
  --function-name $FUNCTION_NAME \
  --zip-file fileb://lambda.zip \
  --region $REGION

echo " Despliegue completado"
EOF

chmod +x deploy.sh