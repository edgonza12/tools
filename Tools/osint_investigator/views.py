# osint_investigator/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import InvestigationForm
from .models import InvestigationHistory
from .sherlock_wrapper import run_sherlock  # Importa la función wrapper de Sherlock

@login_required
def investigator_view(request):
    form = InvestigationForm()
    sherlock_results = {}
    investigation = None

    if request.method == 'POST':
        form = InvestigationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            full_name = form.cleaned_data.get('full_name')

            # Ejecutar Sherlock si se proporciona un nombre de usuario
            if username:
                sherlock_results = run_sherlock(username)

            # Guardar la investigación en historial
            investigation = InvestigationHistory.objects.create(
                user=request.user,
                username=username,
                email=email,
                full_name=full_name,
                result_summary="Búsqueda completada con Sherlock" if username else "Búsqueda sin nombre de usuario"
            )

            # Puedes almacenar resultados adicionales en el historial si quieres (otro paso)

    return render(request, 'osint_investigator/investigation_results.html', {
        'form': form,
        'sherlock_results': sherlock_results,
        'investigation': investigation,
    })