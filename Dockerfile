FROM python:3.9-slim

# Configuración de variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . .

# Crear directorios para archivos estáticos ANTES de collectstatic
RUN mkdir -p /app/static
RUN mkdir -p /app/staticfiles
RUN mkdir -p /app/media

# Crear un archivo vacío para evitar errores
RUN touch /app/static/.keep

# Intentar recolectar archivos estáticos, pero continuar si falla
RUN python manage.py collectstatic --noinput || true

# Puerto en el que escucha Cloud Run
EXPOSE 8080

# Comando para iniciar la aplicación
CMD exec gunicorn --bind :$PORT --workers 2 --threads 8 --timeout 0 medical_system.wsgi:application
