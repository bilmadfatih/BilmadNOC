from django.utils import timezone


def calculate_asset_health(asset):
    score = 100
    reasons = []

    if asset.status == 'warning':
        score -= 15
        reasons.append('Durum uyarı')
    elif asset.status == 'offline':
        score -= 35
        reasons.append('Offline')
    elif asset.status == 'critical':
        score -= 50
        reasons.append('Kritik')
    elif asset.status == 'unknown':
        score -= 10
        reasons.append('Durum bilinmiyor')

    if asset.is_critical and asset.status in ('offline', 'critical'):
        score -= 15
        reasons.append('Kritik asset etkisi')

    open_alerts = asset.alerts.filter(is_resolved=False).count()
    if open_alerts:
        penalty = min(open_alerts * 8, 32)
        score -= penalty
        reasons.append(f'{open_alerts} açık alarm')

    failed_recent = asset.check_results.filter(success=False)[:10].count()
    if failed_recent:
        penalty = min(failed_recent * 3, 24)
        score -= penalty
        reasons.append(f'Son kontrollerde {failed_recent} hata')

    if asset.last_checked_at:
        minutes = (timezone.now() - asset.last_checked_at).total_seconds() / 60
        if minutes > 60:
            score -= 10
            reasons.append('Son kontrol eski')
    else:
        score -= 12
        reasons.append('Henüz kontrol yok')

    return max(min(score, 100), 0), reasons


def score_class(score):
    if score >= 85:
        return 'good'
    if score >= 65:
        return 'warn'
    return 'bad'
