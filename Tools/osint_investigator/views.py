import subprocess
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import InvestigationForm
from .models import InvestigationHistory
from .services import perform_investigation  # lógica que centraliza la búsqueda
from django.http import JsonResponse
from django.template.loader import render_to_string
from .sherlock_wrapper import search_username

@login_required
def investigator_view(request):
    if request.method == 'POST':
        form = InvestigationForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_type = form.cleaned_data['search_type']

            results = perform_investigation(query, search_type, user=request.user)

            html = render_to_string('osint_investigator/partials/investigation_results.html', {'results': results})
            return JsonResponse({'html': html})

    else:
        form = InvestigationForm()

    return render(request, 'osint_investigator/investigator.html', {'form': form})

@login_required
def investigation_view(request):
    form = InvestigationForm()
    results = {}

    if request.method == 'POST':
        form = InvestigationForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_type = form.cleaned_data['search_type']

            # Guardar en historial
            InvestigationHistory.objects.create(
                user=request.user,
                search_type=search_type,
                query=query
            )

            if search_type == 'username':
                # Ejecuta Sherlock desde el sistema
                try:
                    output = subprocess.check_output(
                        ['python3', 'sherlock/sherlock.py', query, '--print-found', '--json'],
                        stderr=subprocess.DEVNULL,
                        universal_newlines=True
                    )
                    sherlock_data = json.loads(output)
                    results = {'type': 'username', 'data': sherlock_data}
                except Exception as e:
                    results = {'error': f'Error al ejecutar Sherlock: {e}'}
            else:
                # Placeholder para búsquedas futuras (email, nombre completo)
                results = {'type': search_type, 'data': f'Búsqueda para {search_type} aún no implementada.'}

    return render(request, 'osint_investigator/investigation_results.html', {
        'form': form,
        'results': results
    })
