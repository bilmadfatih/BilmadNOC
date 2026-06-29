import time
from urllib import request as urllib_request
from urllib.error import HTTPError, URLError

from .base import BaseMonitoringPlugin, PluginExecutionResult


def _elapsed_ms(start):
    return max(1, int((time.perf_counter() - start) * 1000))


class HttpPlugin(BaseMonitoringPlugin):
    code = 'http'
    name = 'HTTP'

    def run(self, monitoring_check):
        target = monitoring_check.effective_target
        path = monitoring_check.path or '/'
        timeout_seconds = max(monitoring_check.timeout_seconds or 5, 5)
        if not target:
            return PluginExecutionResult(False, 'offline', None, 'HTTP hedef boş', {'target': target})

        url = target if target.startswith(('http://', 'https://')) else f'http://{target}'
        if path and path != '/' and not url.endswith(path):
            url = url.rstrip('/') + '/' + path.lstrip('/')

        start = time.perf_counter()
        try:
            req = urllib_request.Request(url, headers={'User-Agent': 'BilmadNOC/0.5'})
            with urllib_request.urlopen(req, timeout=timeout_seconds) as resp:
                elapsed = _elapsed_ms(start)
                code = int(getattr(resp, 'status', 0))
                ok = 200 <= code < 400
                return PluginExecutionResult(ok, 'online' if ok else 'warning', elapsed, f'HTTP {code} ({elapsed} ms)', {'url': url, 'status_code': code})
        except HTTPError as exc:
            elapsed = _elapsed_ms(start)
            ok = 200 <= int(exc.code) < 400
            return PluginExecutionResult(ok, 'online' if ok else 'warning', elapsed, f'HTTP {exc.code} ({elapsed} ms)', {'url': url, 'status_code': exc.code})
        except URLError as exc:
            elapsed = _elapsed_ms(start)
            return PluginExecutionResult(False, 'offline', elapsed, f'HTTP hata: {exc.reason}', {'url': url, 'error': str(exc.reason)})
        except Exception as exc:
            elapsed = _elapsed_ms(start)
            return PluginExecutionResult(False, 'offline', elapsed, f'HTTP hata: {exc}', {'url': url, 'error': str(exc)})
