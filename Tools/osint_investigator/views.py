from django.shortcuts import render
from .utils import run_sherlock

def investigator_view(request):
    results = None
    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            output = run_sherlock(username)
            results = output.splitlines()
    return render(request, 'investigator.html', {'results': results})