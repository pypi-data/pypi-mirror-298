# src/ticos_agent/core/collector.py

import importlib
import sys
from threading import Thread
import time
from ..services.logger import get_logger

logger = get_logger(__name__)


class Collector:
    def __init__(self, config, metrics_store):
        self.config = config
        self.metrics_store = metrics_store
        self.devices = self._load_devices()
        self.running = False
        self.thread = None

    def _load_devices(self):
        devices = []
        for device_config in self.config.devices:
            if device_config["type"] == "builtin":
                module = importlib.import_module(
                    f"robots.{device_config['model']}.robot"
                )
                device_class = getattr(module, device_config["class_name"])
            elif device_config["type"] == "custom":
                if self.config.custom_robots_path not in sys.path:
                    sys.path.insert(0, self.config.custom_robots_path)

                module = importlib.import_module(device_config["path"])
                device_class = getattr(module, device_config["class_name"])
            else:
                raise ValueError(f"Unknown device type: {device_config['type']}")

            device = device_class()
            device.setup_telemetry(self.config)
            devices.append(device)
        return devices

    def start(self):
        self.running = True
        self.thread = Thread(target=self._collect_loop)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def _collect_loop(self):
        while self.running:
            for device in self.devices:
                try:
                    data = device.collect_data()
                    self.metrics_store.store_metrics(device.get_device_info(), data)
                except Exception as e:
                    logger.error(
                        f"Error collecting data from device {device.get_device_info()['name']}: {str(e)}"
                    )
            time.sleep(self.config.collection_interval)
