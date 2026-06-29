from django.shortcuts import get_object_or_404, render
from assets.models import Asset, AssetStatus
from core.models import Customer


def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    assets = Asset.objects.filter(customer=customer).select_related("site", "manufacturer", "location")

    context = {
        "customer": customer,
        "assets": assets,
        "asset_count": assets.count(),
        "online_count": assets.filter(status=AssetStatus.ONLINE).count(),
        "warning_count": assets.filter(status=AssetStatus.WARNING).count(),
        "critical_count": assets.filter(status=AssetStatus.CRITICAL).count(),
        "offline_count": assets.filter(status=AssetStatus.OFFLINE).count(),
    }
    return render(request, "customer360/detail.html", context)
