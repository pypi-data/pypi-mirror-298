import threading
from typing import Dict, Any


class MetricsStore:
    def __init__(self):
        self.metrics = {}
        self.lock = threading.Lock()

    def add_metric(self, key: str, value: Any):
        with self.lock:
            self.metrics[key] = value

    def remove_metric(self, key: str):
        with self.lock:
            self.metrics.pop(key, None)

    def get_metrics(self) -> Dict[str, Any]:
        with self.lock:
            return self.metrics.copy()

    def clear_metrics(self):
        with self.lock:
            self.metrics.clear()

    def store_metrics(self, device_info: Dict[str, Any], data: Dict[str, Any]):
        with self.lock:
            device_name = device_info.get('name', 'unknown_device')
            if device_name not in self.metrics:
                self.metrics[device_name] = {}
            self.metrics[device_name].update(data)

    def __str__(self):
        return f"MetricsStore(metrics={self.get_metrics()})"

    def __repr__(self):
        return self.__str__()