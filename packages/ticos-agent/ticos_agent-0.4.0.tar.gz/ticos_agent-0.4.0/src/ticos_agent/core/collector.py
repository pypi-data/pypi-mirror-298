# src/ticos_agent/core/collector.py

import importlib
import sys
from threading import Thread, Event
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
        self.collect_interval = config.get("collect_interval", 60)
        self.stop_event = Event()

    def _load_devices(self):
        devices = []
        for device_config in self.config.devices:
            try:
                if device_config["type"] == "builtin":
                    module = importlib.import_module(
                        f"ticos_agent.robots.{device_config['model']}.robot"
                    )
                elif device_config["type"] == "custom":
                    if self.config.custom_robots_path not in sys.path:
                        sys.path.insert(0, self.config.custom_robots_path)
                    module = importlib.import_module(device_config["path"])
                else:
                    raise ValueError(f"Unknown device type: {device_config['type']}")

                device_class = getattr(module, device_config["class_name"])
                device = device_class()
                device.setup_telemetry(self.config)
                devices.append(device)
            except Exception as e:
                logger.error(f"Error loading device {device_config['name']}: {str(e)}")
        return devices

    def start(self):
        if not self.running:
            self.running = True
            self.stop_event.clear()
            self.thread = Thread(target=self._collect_loop)
            self.thread.start()
            logger.info("Collector started")

    def stop(self):
        if self.running:
            self.running = False
            self.stop_event.set()
            if self.thread:
                self.thread.join()
            logger.info("Collector stopped")

    def _collect_loop(self):
        while self.running:
            start_time = time.time()

            for device in self.devices:
                if not self.running:
                    break
                try:
                    data = device.collect_data()
                    self.metrics_store.store_metrics(device.get_device_info(), data)
                except Exception as e:
                    logger.error(
                        f"Error collecting data from device {device.get_device_info()['name']}: {str(e)}"
                    )

            elapsed_time = time.time() - start_time
            remaining_time = max(0, self.collect_interval - elapsed_time)

            # Wait for the remaining time or until stop is called
            self.stop_event.wait(timeout=remaining_time)
