from django import forms

class PDFDownloadForm(forms.Form):
    pdf_url = forms.URLField(
        label='URL del PDF',
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://ejemplo.com/archivo.pdf'
        })
    )