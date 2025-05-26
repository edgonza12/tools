from django.contrib import admin
from .models import CustomUser, Module, UserModulePermission
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm
from django.utils.translation import gettext_lazy as _
# Desregistra el modelo si ya está registrado
try:
    admin.site.unregister(Module)
except admin.sites.NotRegistered:
    pass
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'url_name', 'parent', 'is_active')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'url_name')
    autocomplete_fields = ['parent']  # permite buscar el módulo padre

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'is_staff']
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)

class ModuleAdmin(admin.ModelAdmin):
    search_fields = ['name']

class UserModulePermissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'module', 'can_access']
    list_filter = ['user', 'module', 'can_access']
    autocomplete_fields = ['user', 'module']  # necesita search_fields en ambos modelos

admin.site.register(CustomUser, CustomUserAdmin)
#admin.site.register(Module, ModuleAdmin)
admin.site.register(UserModulePermission, UserModulePermissionAdmin)