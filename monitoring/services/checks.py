"""Backward compatible monitoring service facade.

Sprint 2.5 ile gerçek akış monitoring.engine + plugin registry altına taşındı.
Eski view/task importları bozulmasın diye bu dosya facade olarak korunuyor.
"""
from types import SimpleNamespace

from monitoring.engine.dispatcher import dispatch_all_enabled, dispatch_check, dispatch_device
from monitoring.plugins.http import HttpPlugin
from monitoring.plugins.ping import PingPlugin
from monitoring.plugins.tcp import TcpPlugin
from monitoring.services.provisioning import ensure_default_checks


def ping_target(target, timeout_seconds=3):
    dummy = SimpleNamespace(effective_target=target, timeout_seconds=timeout_seconds)
    result = PingPlugin().run(dummy)
    return result.success, result.response_time_ms, result.message, result.raw_data


def tcp_check(target, port, timeout_seconds=3):
    dummy = SimpleNamespace(effective_target=target, port=port, timeout_seconds=timeout_seconds)
    result = TcpPlugin().run(dummy)
    return result.success, result.response_time_ms, result.message, result.raw_data


def http_check(target, path='/', timeout_seconds=5):
    dummy = SimpleNamespace(effective_target=target, path=path, timeout_seconds=timeout_seconds)
    result = HttpPlugin().run(dummy)
    return result.success, result.response_time_ms, result.message, result.raw_data


def run_check(check):
    return dispatch_check(check)


def run_device_checks(device):
    return dispatch_device(device)


def run_all_enabled_checks():
    return dispatch_all_enabled()
