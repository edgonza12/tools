from django.urls import path
from .views import scan_network_view, ScanHistoryListView, ScanHistoryDetailView, export_scan_csv, export_scan_pdf, scan_network_ajax_view

urlpatterns = [
    path('', scan_network_view, name='scan_network'),
    path('history/', ScanHistoryListView.as_view(), name='scan_history'),
    path('history/<int:pk>/', ScanHistoryDetailView.as_view(), name='scan_detail'),
    path('history/<int:pk>/export_csv/', export_scan_csv, name='export_scan_csv'),
    path('history/<int:pk>/export_pdf/', export_scan_pdf, name='export_scan_pdf'),
    path('scanner/ajax/', scan_network_ajax_view, name='scan_network_ajax'),
]