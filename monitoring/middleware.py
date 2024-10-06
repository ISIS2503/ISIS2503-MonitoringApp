import logging
import time

logger = logging.getLogger(__name__)

class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()

        processing_time = end_time - start_time
        
        # Medir el tiempo de registro
        log_start_time = time.time()
        logger.info(f"Request to {request.path} took {processing_time:.2f} seconds")
        log_end_time = time.time()

        log_time = log_end_time - log_start_time
        logger.info(f"Logging took {log_time:.6f} seconds")  # Cambié a 6 decimales para mayor precisión

        return response
