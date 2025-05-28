# osint_investigator/urls.py
from django.urls import path
from .views import investigator_view

urlpatterns = [
    #path('', investigator_view, name='investigator'),
    #path('', views.investigation_form, name='investigation'),
    #path('search/', views.sherlock_search, name='sherlock_search'),
    path('', investigator_view, name='investigation'),
]
