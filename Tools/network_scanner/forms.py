from django import forms

class NetworkScanForm(forms.Form):
    network_range = forms.CharField(
        label='Rango de red (ej: 192.168.1.0/24)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '192.168.1.0/24'
        })
    )
class ScanHistoryFilterForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    target_network = forms.CharField(required=False, label="Red escaneada")