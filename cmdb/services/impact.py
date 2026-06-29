from cmdb.models import AssetRelationship, BusinessService, Dependency


def impacted_assets(asset):
    """Return assets directly impacted by a given asset."""
    return AssetRelationship.objects.select_related('target').filter(source=asset, is_active=True)


def impacted_services(asset):
    """Return business services that depend on the asset."""
    return BusinessService.objects.filter(dependencies__asset=asset, dependencies__is_active=True, is_active=True).distinct()


def calculate_asset_impact(asset):
    """Small RCA helper for future AI/root-cause screens."""
    service_count = Dependency.objects.filter(asset=asset, is_active=True).count()
    relation_count = AssetRelationship.objects.filter(source=asset, is_active=True).count()
    score = min(100, (service_count * 30) + (relation_count * 10))
    return {
        'service_count': service_count,
        'relationship_count': relation_count,
        'impact_score': score,
    }
