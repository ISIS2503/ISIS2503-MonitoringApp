import logging
import time
import re
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest

logger = logging.getLogger('middleware')

SQL_INJECTION_PATTERNS = [
    r"\bSELECT\b", r"\bUNION\b", r"\bINSERT\b", r"\bDELETE\b",
    r"\bDROP\b", r"--", r"\bOR\b.+=", r"' OR '", r"1=1", r"sleep\(", r"benchmark\("
]

def enviar_alerta_email(detalles_ataque):
    subject = "Alerta de Seguridad: Intento de Inyección SQL Detectado"
    message = f"Se detectó un intento de inyección SQL en la solicitud con los siguientes detalles:\n\n{detalles_ataque}"
    from_email = 'jfrc72@gmail.com'
    recipient_list = ['jf.rodriguezc1@uniandes.edu.co']
    send_mail(subject, message, from_email, recipient_list)

class RequestTimingAndSQLInjectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        query_string = ' '.join([str(value) for value in request.GET.values()])
        query_string += ' '.join([str(value) for value in request.POST.values()])

        for pattern in SQL_INJECTION_PATTERNS:
            if re.search(pattern, query_string, re.IGNORECASE):
                mensaje = f"Intento de inyección SQL detectado en la solicitud: {query_string}"
                enviar_alerta_email(mensaje)
                logger.warning(mensaje)
                return HttpResponseBadRequest("Solicitud inválida")

        response = self.get_response(request)

        end_time = time.time()
        processing_time = end_time - start_time

        logger.info(f"Request to {request.path} took {processing_time:.2f} seconds")

        return response