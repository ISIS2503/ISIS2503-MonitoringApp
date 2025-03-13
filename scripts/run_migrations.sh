#!/bin/bash
set -e

# Variables de entorno
PROJECT_ID="arquisoft-453601"
REGION="us-central1"
INSTANCE_NAME="django-db-instance"

# Realizar las migraciones
echo "Ejecutando makemigrations..."
DJANGO_SETTINGS_MODULE=monitoring.settings_prod python manage.py makemigrations

echo "Ejecutando migrate..."
# Ejecutar migraciones
DJANGO_SETTINGS_MODULE=monitoring.settings_prod python manage.py migrate

# Detener el proxy cuando terminemos
kill $PROXY_PID
echo "Proxy detenido."
