"""
URL configuration for Tools project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path
# from accounts.views import register_view, login_view, logout_view, dashboard_view

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', dashboard_view, name='dashboard'),
#     path('login/', login_view, name='login'),
#     path('logout/', logout_view, name='logout'),
#     path('register/', register_view, name='register'),
# ]

from django.contrib import admin
from django.urls import path, include
from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', account_views.home, name='home'),
    path('', account_views.dashboard_view, name='dashboard'),
    path('login/', account_views.login_view, name='login'),
    path('logout/', account_views.logout_view, name='logout'),
    path('register/', account_views.register_view, name='register'),
    path('pdf/', include('pdf_tool.urls')),  # <- Agregado aquí
    path('scanner/', include('network_scanner.urls')),
    path('investigation/', include('osint_investigator.urls')),
]