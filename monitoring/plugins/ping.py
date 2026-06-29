import platform
import subprocess
import time

from .base import BaseMonitoringPlugin, PluginExecutionResult


def _elapsed_ms(start):
    return max(1, int((time.perf_counter() - start) * 1000))


class PingPlugin(BaseMonitoringPlugin):
    code = 'ping'
    name = 'Ping'

    def run(self, monitoring_check):
        target = monitoring_check.effective_target
        timeout_seconds = monitoring_check.timeout_seconds or 3
        if not target:
            return PluginExecutionResult(False, 'offline', None, 'Hedef IP/hostname boş', {'target': target})

        system = platform.system().lower()
        if 'windows' in system:
            cmd = ['ping', '-n', '1', '-w', str(timeout_seconds * 1000), target]
        else:
            cmd = ['ping', '-c', '1', '-W', str(timeout_seconds), target]

        start = time.perf_counter()
        try:
            completed = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_seconds + 2)
            elapsed = _elapsed_ms(start)
            output = (completed.stdout or completed.stderr or '').strip()[-700:]
            if completed.returncode == 0:
                return PluginExecutionResult(True, 'online', elapsed, f'Ping OK ({elapsed} ms)', {'cmd': cmd, 'output': output})
            return PluginExecutionResult(False, 'offline', elapsed, 'Ping timeout veya erişilemez', {'cmd': cmd, 'output': output, 'returncode': completed.returncode})
        except Exception as exc:
            return PluginExecutionResult(False, 'offline', None, f'Ping hata: {exc}', {'cmd': cmd, 'error': str(exc)})
