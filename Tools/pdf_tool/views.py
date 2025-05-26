import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import PDFDownloadForm

@login_required
def descargar_pdf_view(request):
    form = PDFDownloadForm()
    if request.method == 'POST':
        form = PDFDownloadForm(request.POST)
        if form.is_valid():
            pdf_url = form.cleaned_data['pdf_url']
            try:
                response = requests.get(pdf_url)
                response.raise_for_status()  # Lanza error si status != 200
                content_type = response.headers.get('Content-Type')
                if 'application/pdf' not in content_type:
                    return HttpResponse("La URL no parece apuntar a un archivo PDF.", status=400)

                filename = pdf_url.split('/')[-1] or "documento.pdf"
                return HttpResponse(
                    response.content,
                    content_type='application/pdf',
                    headers={'Content-Disposition': f'attachment; filename="{filename}"'}
                )
            except requests.exceptions.RequestException:
                return HttpResponse("No se pudo descargar el PDF. Verifica la URL.", status=400)

    return render(request, 'pdf_tool/descargar_pdf.html', {'form': form})