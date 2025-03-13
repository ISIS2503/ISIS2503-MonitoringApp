#!/bin/bash
set -e

echo "Instalando dependencias para migraciones..."
pip install psycopg2-binary google-cloud-secret-manager django

echo "Configurando proxy SQL..."
# Cloud Build tiene permisos implícitos, así que no necesita autenticación adicional
wget https://dl.google.com/cloudsql/cloud-sql-proxy.linux.amd64 -O cloud-sql-proxy
chmod +x cloud-sql-proxy
./cloud-sql-proxy "${PROJECT_ID}:${_REGION}:django-db-instance" &
PROXY_PID=$!

# Esperar a que el proxy se inicie
sleep 5

echo "Ejecutando migraciones..."
# Ejecutar migraciones
DJANGO_SETTINGS_MODULE=monitoring.settings_prod python manage.py migrate

# Detener el proxy cuando terminemos
kill $PROXY_PID
