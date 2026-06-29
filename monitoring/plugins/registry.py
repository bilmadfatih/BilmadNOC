from .http import HttpPlugin
from .ping import PingPlugin
from .tcp import TcpPlugin

PLUGIN_REGISTRY = {
    PingPlugin.code: PingPlugin(),
    HttpPlugin.code: HttpPlugin(),
    TcpPlugin.code: TcpPlugin(),
}


def get_plugin(check_type):
    return PLUGIN_REGISTRY.get(check_type)


def available_plugins():
    return PLUGIN_REGISTRY
