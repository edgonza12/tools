from django import forms

class SherlockSearchForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese el nombre de usuario'
    }))