import subprocess
import json
from .models import InvestigationHistory

def perform_investigation(query, search_type, user=None):
    results = {}

    # Guardar en historial
    if user:
        InvestigationHistory.objects.create(
            user=user,
            search_type=search_type,
            query=query
        )

    if search_type == 'username':
        try:
            # Ejecutar Sherlock desde el sistema (asegúrate de que esté clonado localmente)
            output = subprocess.check_output(
                ['python3', 'sherlock/sherlock.py', query, '--print-found', '--json'],
                stderr=subprocess.DEVNULL,
                universal_newlines=True
            )
            sherlock_data = json.loads(output)
            results = {
                'type': 'username',
                'data': sherlock_data
            }
        except Exception as e:
            results = {
                'error': f'Error al ejecutar Sherlock: {str(e)}'
            }

    else:
        # Placeholder para otros tipos de búsqueda (email, nombre)
        results = {
            'type': search_type,
            'data': f'Búsqueda para {search_type} aún no está implementada.'
        }

    return results