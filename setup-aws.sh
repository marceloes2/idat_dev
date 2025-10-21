# Script: setup-aws.sh
cat > setup-aws.sh << 'EOF'
#!/bin/bash
set -e

FUNCTION_NAME="fastapi-tasks-api"
ROLE_NAME="lambda-fastapi-role"
REGION="us-east-1"

echo " Configurando AWS Lambda..."

# 1. Crear rol IAM
echo "→ Creando rol IAM..."
aws iam create-role \
  --role-name $ROLE_NAME \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }' || echo "Rol ya existe"

# 2. Adjuntar política básica
echo "→ Adjuntando política..."
aws iam attach-role-policy \
  --role-name $ROLE_NAME \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Esperar a que el rol esté disponible
sleep 10

# 3. Obtener ARN del rol
ROLE_ARN=$(aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text)

# 4. Crear función Lambda
echo "→ Creando función Lambda..."
aws lambda create-function \
  --function-name $FUNCTION_NAME \
  --runtime python3.11 \
  --role $ROLE_ARN \
  --handler app.handler \
  --zip-file fileb://lambda.zip \
  --timeout 30 \
  --memory-size 256 \
  --region $REGION || echo "Función ya existe"

# 5. Crear API Gateway
echo "→ Creando API Gateway..."
API_ID=$(aws apigatewayv2 create-api \
  --name "FastAPI Tasks API" \
  --protocol-type HTTP \
  --target arn:aws:lambda:$REGION:$(aws sts get-caller-identity --query Account --output text):function:$FUNCTION_NAME \
  --query 'ApiId' \
  --output text)

# 6. Dar permiso a API Gateway
aws lambda add-permission \
  --function-name $FUNCTION_NAME \
  --statement-id apigateway-invoke \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn "arn:aws:execute-api:$REGION:$(aws sts get-caller-identity --query Account --output text):$API_ID/*/*" || echo "Permiso ya existe"

echo ""
echo " Configuración completada"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " URL de la API:"
echo "https://$API_ID.execute-api.$REGION.amazonaws.com"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
EOF

chmod +x setup-aws.sh