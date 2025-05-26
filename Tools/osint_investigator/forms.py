from django import forms

class InvestigationForm(forms.Form):
    SEARCH_TYPE_CHOICES = [
        ('username', 'Nombre de Usuario'),
        ('email', 'Correo Electrónico'),
        ('name', 'Nombre Completo'),
    ]

    query = forms.CharField(label="Dato a investigar", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    search_type = forms.ChoiceField(label="Tipo de búsqueda", choices=SEARCH_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))