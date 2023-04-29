from django.http import JsonResponse
from django.shortcuts import render
from historias.logic.historia_logic import get_historia_by_name
from .logic.logic_cita import get_citas, get_plantillas_by_historia, create_cita


def cita_list(request):
    citas = get_citas()
    context = list(citas.values())
    return JsonResponse(context, safe=False)

def generate_cita(request, historia_name):
    historia = get_historia_by_name(historia_name)
    plantillas = get_plantillas_by_historia(historia_name)
    createcita = False
    upperPlantilla = None
    for plantilla in plantillas:
        if plantilla.especificacion == 'Emergencia':
            createCita = True
            upperPlantilla = plantilla
    if createcita:
        cita = create_cita(historia, plantilla)
        return JsonResponse(cita.toJson(), safe=False)
    else:
        return JsonResponse({'message': 'No cita created'}, status=200)