# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse, HttpResponse
# from django.template.loader import render_to_string
# from django.contrib.auth.decorators import login_required
# from django.conf import settings
# from .forms import SherlockSearchForm
# import subprocess
# import json
# import tempfile
# import os

# @login_required
# def investigation_form(request):
#     form = SherlockSearchForm()
#     return render(request, 'osint_investigator/investigation_form.html', {'form': form})

# @login_required
# @csrf_exempt
# def sherlock_search(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         if not username:
#             return JsonResponse({'error': 'Se requiere un nombre de usuario'}, status=400)

#         try:
#             # Ejecutar Sherlock usando --print-found
#             result = subprocess.run(
#                 ['python3', 'osint_investigator/sherlock/sherlock_project/sherlock.py', username, '--print-found'],
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 text=True,
#                 timeout=90
#             )

#             if result.returncode != 0 and not result.stdout:
#                 return JsonResponse({
#                     'error': 'Error al ejecutar Sherlock',
#                     'stderr': result.stderr,
#                     'stdout': result.stdout
#                 }, status=500)

#             found_sites = []
#             for line in result.stdout.splitlines():
#                 if line.startswith("[+]"):  # Sherlock marca los resultados encontrados así
#                     found_sites.append(line[4:].strip())

#             return JsonResponse({'results': found_sites})

#         except subprocess.TimeoutExpired:
#             return JsonResponse({'error': 'Tiempo de espera agotado al ejecutar Sherlock'}, status=504)

#     return JsonResponse({'error': 'Método no permitido'}, status=405)

from django.shortcuts import render
from django.http import JsonResponse
from .forms import SherlockInvestigationForm
from .sherlock_wrapper import run_sherlock

def investigator_view(request):
    form = SherlockInvestigationForm()

    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        form = SherlockInvestigationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            results = run_sherlock(username)

            if 'error' in results:
                return JsonResponse({'html': f"<div class='alert alert-danger'>{results['error']}</div>"})

            return render(request, "osint_investigator/partials/sherlock_results.html", {
                'username': username,
                'results': results['results']
            })

        return JsonResponse({'html': "<div class='alert alert-danger'>Formulario inválido</div>"})

    return render(request, "osint_investigator/investigation_form.html", {'form': form})