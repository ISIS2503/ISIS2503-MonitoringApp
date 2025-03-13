from .settings import *
import os
import google.auth
from google.cloud import secretmanager

# Cargar secretos desde Secret Manager
def access_secret_version(secret_id, version_id="latest"):
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/arquisoft-453601/secrets/{secret_id}/versions/{version_id}"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        print(f"Error accediendo al secreto {secret_id}: {e}")
        return None

# Configuración para producción
DEBUG = False

# Cargar SECRET_KEY desde Secret Manager
SECRET_KEY = access_secret_version("django-secret-key") or SECRET_KEY

# Permitir hosts de Cloud Run
ALLOWED_HOSTS = ['*']

# Configuración de base de datos para desarrollo/pruebas
# Esto es temporal hasta que configures Cloud SQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Configuración para WhiteNoise
MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware'] + MIDDLEWARE

# Ajustes para archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuración para archivos de medios
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
