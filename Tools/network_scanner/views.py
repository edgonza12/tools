import nmap, csv, tempfile
from django.template.loader import get_template, render_to_string
from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .forms import NetworkScanForm, ScanHistoryFilterForm
from .models import ScanHistory, ScanHostResult, OpenPort, ScanHistory

@login_required
def scan_network_view(request):
    form = NetworkScanForm()
    results = []

    if request.method == 'POST':
        form = NetworkScanForm(request.POST)
        if form.is_valid():
            network = form.cleaned_data['network_range']
            scanner = nmap.PortScanner()

            try:
                scanner.scan(hosts=network, arguments='-T4 -F')  # Fast scan, detect puertos comunes
                scan_history = ScanHistory.objects.create(
                    user=request.user,
                    target_network=network,
                    total_hosts=len(scanner.all_hosts())
                )

                for host in scanner.all_hosts():
                    ip = host
                    status = scanner[host].state()
                    hostname = scanner[host].hostname()
                    mac = scanner[host]['addresses'].get('mac', '')
                    vendor = scanner[host]['vendor'].get(mac, '') if 'vendor' in scanner[host] else ''

                    host_result = ScanHostResult.objects.create(
                        history=scan_history,
                        ip=ip,
                        hostname=hostname,
                        mac=mac,
                        vendor=vendor
                    )

                    # Guardar puertos abiertos
                    for proto in scanner[host].all_protocols():
                        ports = scanner[host][proto].keys()
                        for port in ports:
                            port_info = scanner[host][proto][port]
                            OpenPort.objects.create(
                                host=host_result,
                                port=port,
                                protocol=proto,
                                service=port_info.get('name', '')
                            )

                    results.append({
                        'ip': ip,
                        'status': status,
                        'hostname': hostname,
                        'mac': mac,
                        'vendor': vendor,
                        'ports': host_result.ports.all()
                    })

            except Exception as e:
                results.append({'ip': 'Error', 'status': str(e)})

    return render(request, 'network_scanner/scan.html', {
        'form': form,
        'results': results
    })

@login_required
def scan_network_ajax_view(request):
    if request.method == 'POST':
        form = NetworkScanForm(request.POST)
        results = []

        if form.is_valid():
            network = form.cleaned_data['network_range']
            scanner = nmap.PortScanner()

            try:
                scanner.scan(hosts=network, arguments='-T4 -F')
                scan_history = ScanHistory.objects.create(
                    user=request.user,
                    target_network=network,
                    total_hosts=len(scanner.all_hosts())
                )

                for host in scanner.all_hosts():
                    ip = host
                    status = scanner[host].state()
                    hostname = scanner[host].hostname()
                    mac = scanner[host]['addresses'].get('mac', '')
                    vendor = scanner[host]['vendor'].get(mac, '') if 'vendor' in scanner[host] else ''

                    host_result = ScanHostResult.objects.create(
                        history=scan_history,
                        ip=ip,
                        hostname=hostname,
                        mac=mac,
                        vendor=vendor
                    )

                    for proto in scanner[host].all_protocols():
                        ports = scanner[host][proto].keys()
                        for port in ports:
                            port_info = scanner[host][proto][port]
                            OpenPort.objects.create(
                                host=host_result,
                                port=port,
                                protocol=proto,
                                service=port_info.get('name', '')
                            )

                    results.append({
                        'ip': ip,
                        'status': status,
                        'hostname': hostname,
                        'mac': mac,
                        'vendor': vendor,
                        'ports': host_result.ports.all()
                    })

            except Exception as e:
                results.append({'ip': 'Error', 'status': str(e)})

            html = render_to_string('network_scanner/partials/scan_results.html', {'results': results})
            return HttpResponse(html)

    return HttpResponse("Solicitud inválida", status=400)


class ScanHistoryListView(ListView):
    model = ScanHistory
    template_name = 'network_scanner/history_list.html'
    context_object_name = 'scans'

    def get_queryset(self):
        return ScanHistory.objects.filter(user=self.request.user).order_by('-date')


class ScanHistoryDetailView(DetailView):
    model = ScanHistory
    template_name = 'network_scanner/history_detail.html'
    context_object_name = 'scan'

    def get_queryset(self):
        return ScanHistory.objects.filter(user=self.request.user)
    

class ScanHistoryListView(ListView):
    model = ScanHistory
    template_name = 'network_scanner/history_list.html'
    context_object_name = 'scans'

    def get_queryset(self):
        queryset = ScanHistory.objects.filter(user=self.request.user).order_by('-date')
        self.form = ScanHistoryFilterForm(self.request.GET)

        if self.form.is_valid():
            start_date = self.form.cleaned_data.get('start_date')
            end_date = self.form.cleaned_data.get('end_date')
            target_network = self.form.cleaned_data.get('target_network')

            if start_date:
                queryset = queryset.filter(date__gte=start_date)
            if end_date:
                queryset = queryset.filter(date__lte=end_date)
            if target_network:
                queryset = queryset.filter(target_network__icontains=target_network)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.form
        return context
    

@login_required
def export_scan_csv(request, pk):
    scan = ScanHistory.objects.filter(user=request.user, pk=pk).first()
    if not scan:
        return HttpResponse("No autorizado", status=403)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="scan_{scan.pk}.csv"'

    writer = csv.writer(response)
    writer.writerow(['IP', 'Hostname', 'MAC', 'Vendor', 'Puerto', 'Protocolo', 'Servicio'])

    for host in scan.hosts.all():
        for port in host.ports.all():
            writer.writerow([
                host.ip,
                host.hostname,
                host.mac,
                host.vendor,
                port.port,
                port.protocol,
                port.service
            ])

    return response

@login_required
def export_scan_pdf(request, pk):
    scan = ScanHistory.objects.filter(user=request.user, pk=pk).first()
    if not scan:
        return HttpResponse("No autorizado", status=403)

    template = get_template('network_scanner/pdf_template.html')
    html = template.render({'scan': scan})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="scan_{scan.pk}.pdf"'

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        response.write(result.getvalue())
        return response
    else:
        return HttpResponse("Error al generar el PDF", status=500)