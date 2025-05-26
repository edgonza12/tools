from django.urls import path
from . import views

urlpatterns = [
    path('', views.descargar_pdf_view, name='descargar_pdf'),
]