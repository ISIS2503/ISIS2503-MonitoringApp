#!/bin/bash
set -e

# Variables de entorno
PROJECT_ID="arquisoft-453601"
REGION="us-central1"
INSTANCE_NAME="django-db-instance"

echo "Instalando dependencias para migraciones..."
pip install psycopg2-binary google-cloud-secret-manager django

echo "Configurando Cloud SQL Proxy..."
# Descargar el proxy
wget https://dl.google.com/cloudsql/cloud-sql-proxy.linux.amd64 -O cloud-sql-proxy
chmod +x cloud-sql-proxy

# Iniciar el proxy en segundo plano
./cloud-sql-proxy "${PROJECT_ID}:${REGION}:${INSTANCE_NAME}" &
PROXY_PID=$!

# Esperar a que el proxy se inicie
echo "Esperando a que el proxy se inicie..."
sleep 5

# Realizar las migraciones
echo "Ejecutando makemigrations..."
DJANGO_SETTINGS_MODULE=monitoring.settings_prod python manage.py makemigrations

echo "Ejecutando migrate..."
# Ejecutar migraciones
DJANGO_SETTINGS_MODULE=monitoring.settings_prod python manage.py migrate

# Detener el proxy cuando terminemos
kill $PROXY_PID
echo "Proxy detenido."
