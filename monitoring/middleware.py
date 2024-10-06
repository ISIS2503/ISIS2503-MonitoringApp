# monitoring/middleware.py

import time
import logging

logger = logging.getLogger('request_timing')

class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logger.info("Request Timing Middleware initialized.")  # Agrega un mensaje de prueba aquí

    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"Request to {request.path} took {duration:.2f} seconds")  # Este debe ir al log
        
        return response
