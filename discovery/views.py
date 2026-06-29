from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DiscoveryRunForm
from .models import DiscoveryRun
from .services import import_hosts_to_devices, run_discovery


def discovery_home(request):
    runs = DiscoveryRun.objects.select_related('company', 'location').all()[:12]
    form = DiscoveryRunForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        run = DiscoveryRun.objects.create(
            company=form.cleaned_data['company'],
            location=form.cleaned_data.get('location'),
            cidr=form.cleaned_data['cidr'],
            scan_tcp=form.cleaned_data['scan_tcp'],
        )
        run_discovery(run)
        messages.success(request, 'Keşif taraması tamamlandı.')
        return redirect('discovery_detail', pk=run.pk)
    return render(request, 'discovery/home.html', {'form': form, 'runs': runs})


def discovery_detail(request, pk):
    run = get_object_or_404(DiscoveryRun.objects.select_related('company', 'location'), pk=pk)
    hosts = run.hosts.select_related('imported_device').all()
    return render(request, 'discovery/detail.html', {'run': run, 'hosts': hosts})


def discovery_import(request, pk):
    run = get_object_or_404(DiscoveryRun, pk=pk)
    host_ids = request.POST.getlist('hosts')
    count = import_hosts_to_devices(run, host_ids=host_ids or None)
    messages.success(request, f'{count} cihaz varlık listesine aktarıldı.')
    return redirect('discovery_detail', pk=run.pk)
