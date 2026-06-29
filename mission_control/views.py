from django.shortcuts import render
from assets.models import Asset, AssetStatus
from core.models import Customer
from plugins.models import PluginResult


def dashboard(request):
    latest_results = PluginResult.objects.select_related(
        "check",
        "check__asset",
        "check__plugin",
    )[:20]

    context = {
        "customer_count": Customer.objects.count(),
        "asset_count": Asset.objects.count(),
        "online_count": Asset.objects.filter(status=AssetStatus.ONLINE).count(),
        "warning_count": Asset.objects.filter(status=AssetStatus.WARNING).count(),
        "critical_count": Asset.objects.filter(status=AssetStatus.CRITICAL).count(),
        "offline_count": Asset.objects.filter(status=AssetStatus.OFFLINE).count(),
        "unknown_count": Asset.objects.filter(status=AssetStatus.UNKNOWN).count(),
        "latest_results": latest_results,
    }
    return render(request, "mission_control/dashboard.html", context)
