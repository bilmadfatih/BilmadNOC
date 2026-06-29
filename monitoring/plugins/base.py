from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class PluginExecutionResult:
    success: bool
    status: str
    response_time_ms: Optional[int] = None
    message: str = ''
    raw_data: Dict[str, Any] = field(default_factory=dict)


class BaseMonitoringPlugin:
    code = 'base'
    name = 'Base Plugin'

    def run(self, monitoring_check):
        raise NotImplementedError('Plugin run() method must be implemented.')
