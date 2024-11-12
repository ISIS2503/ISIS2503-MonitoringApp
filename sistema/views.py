from django.shortcuts import render
import os  # Asegúrate de incluir esta línea
from django.conf import settings
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def log_monitor(request):
    log_file_path = os.path.join(settings.BASE_DIR, 'logs', 'request_timing.log')
    with open(log_file_path, 'r') as f:
        logs = f.readlines()
    return render(request, 'log_monitor.html', {'logs': logs})