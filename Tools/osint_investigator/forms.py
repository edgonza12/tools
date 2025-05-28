# from django import forms

# class SherlockSearchForm(forms.Form):
#     username = forms.CharField(label='Nombre de usuario', max_length=100, widget=forms.TextInput(attrs={
#         'class': 'form-control',
#         'placeholder': 'Ingrese el nombre de usuario'
#     }))
# osint_investigator/forms.py

from django import forms

class InvestigationForm(forms.Form):
    query = forms.CharField(
        label="Nombre de usuario",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej. admin'
        })
    )
    search_type = forms.ChoiceField(
        choices=[('username', 'Nombre de usuario')],
        initial='username',
        widget=forms.HiddenInput()
    )