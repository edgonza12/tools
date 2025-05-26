# osint_investigator/urls.py
from django.urls import path
from .views import investigator_view

urlpatterns = [
    path('', investigator_view, name='investigator'),
]