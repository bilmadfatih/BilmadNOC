import socket
import time

from .base import BaseMonitoringPlugin, PluginExecutionResult


def _elapsed_ms(start):
    return max(1, int((time.perf_counter() - start) * 1000))


class TcpPlugin(BaseMonitoringPlugin):
    code = 'tcp'
    name = 'TCP Port'

    def run(self, monitoring_check):
        target = monitoring_check.effective_target
        port = monitoring_check.port
        timeout_seconds = monitoring_check.timeout_seconds or 3
        if not target or not port:
            return PluginExecutionResult(False, 'offline', None, 'TCP hedef veya port boş', {'target': target, 'port': port})
        start = time.perf_counter()
        try:
            with socket.create_connection((target, int(port)), timeout=timeout_seconds):
                elapsed = _elapsed_ms(start)
                return PluginExecutionResult(True, 'online', elapsed, f'TCP {port} OPEN ({elapsed} ms)', {'target': target, 'port': port})
        except Exception as exc:
            elapsed = _elapsed_ms(start)
            return PluginExecutionResult(False, 'offline', elapsed, f'TCP {port} CLOSED/TIMEOUT: {exc}', {'target': target, 'port': port, 'error': str(exc)})
