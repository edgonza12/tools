# accounts/context_processors.py
from .models import Module, UserModulePermission
from django.urls import resolve

def dynamic_menu(request):
    if not request.user.is_authenticated:
        return {}

    # Filtra solo módulos activos con permiso
    permissions = UserModulePermission.objects.filter(
        user=request.user, can_access=True
    ).select_related('module')

    modules = [perm.module for perm in permissions if perm.module.is_active]

    parent_modules = {}
    for mod in modules:
        if mod.parent is None:
            parent_modules[mod] = []

    for mod in modules:
        if mod.parent in parent_modules:
            parent_modules[mod.parent].append(mod)

    # Intentar obtener el módulo activo según la URL
    try:
        current_url_name = resolve(request.path_info).url_name
        active_module = next((mod for mod in modules if mod.url_name == current_url_name), None)
    except:
        active_module = None

    return {
        'menu_modules': parent_modules,
        'active_module': active_module,
    }