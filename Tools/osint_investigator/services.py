from .models import InvestigationHistory

def perform_investigation(query, search_type, user=None):
    results = []

    # Aquí podrías usar APIs o librerías reales como Sherlock, EmailRep, etc.
    if search_type == 'username':
        results.append({'label': 'GitHub', 'value': f'Perfil potencial de {query}', 'url': f'https://github.com/{query}'})
        results.append({'label': 'Twitter', 'value': f'Twitter potencial: @{query}', 'url': f'https://twitter.com/{query}'})
    elif search_type == 'email':
        results.append({'label': 'HaveIBeenPwned', 'value': 'Consulta en bases de datos filtradas', 'url': f'https://haveibeenpwned.com/unifiedsearch/{query}'})
    elif search_type == 'name':
        results.append({'label': 'Google', 'value': 'Búsqueda directa en Google', 'url': f'https://www.google.com/search?q={query.replace(" ", "+")}'})

    if user:
        InvestigationHistory.objects.create(user=user, query=query, search_type=search_type)

    return results