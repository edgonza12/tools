from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import InvestigationForm
from .models import InvestigationHistory
from .services import perform_investigation  # lógica que centraliza la búsqueda
from django.http import JsonResponse
from django.template.loader import render_to_string

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

from .sherlock_wrapper import search_username

@login_required
def username_search_view(request):
    result = None

    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            result = search_username(username)

    return render(request, 'osint_investigator/username_search.html', {
        'result': result
    })