import threading
import time
import requests
from datetime import datetime

from ticos_agent.utils.helpers import get_mac_address
from ..services import get_logger

logger = get_logger(__name__)


class Sender:
    def __init__(self, config, metrics_store):
        self.config = config
        self.metrics_store = metrics_store
        self.api_url = config.get("api_url")
        self.api_key = config.get("api_key")
        self.device_id = config.get("device_id", get_mac_address())
        self.send_interval = config.get("send_interval", 60)
        self.stop_event = threading.Event()
        self.send_thread = None
        self.running = False

    def start(self):
        """Start sending telemetry data at regular intervals."""
        if self.running:
            logger.warning("Sender is already running.")
            return

        self.running = True
        self.stop_event.clear()
        self.send_thread = threading.Thread(target=self._send_loop)
        self.send_thread.start()
        logger.info("Sender started.")

    def stop(self):
        """Stop sending telemetry data."""
        if not self.running:
            logger.warning("Sender is not running.")
            return

        self.running = False
        self.stop_event.set()
        if self.send_thread:
            self.send_thread.join()
        self.send_thread = None
        logger.info("Sender stopped.")

    def _send_loop(self):
        while self.running:
            start_time = time.time()

            self.send_telemetry()

            elapsed_time = time.time() - start_time
            remaining_time = max(0, self.send_interval - elapsed_time)

            # Wait for the remaining time or until stop is called
            self.stop_event.wait(timeout=remaining_time)

    def send_telemetry(self):
        """Send telemetry data immediately."""
        try:
            metrics = self.metrics_store.get_metrics()
            payload = {
                "identifier": self.device_id,
                "timestamp": datetime.now().isoformat(),
                "data": metrics,
                "telemetry_type": "metrics",
            }
            response = requests.post(
                f"{self.api_url}/api/telemetry",
                json=payload,
                headers={"x-api-key": self.api_key},
                timeout=30,  # Add a timeout to the request
            )
            response.raise_for_status()
            logger.info(f"Telemetry sent successfully: {response.json()}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error sending telemetry: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error while sending telemetry: {e}")
