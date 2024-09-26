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
        self.send_interval = config.get("send_interval", 30)
        self.stop_event = threading.Event()
        self.send_thread = None

    def start(self):
        """Start sending telemetry data at regular intervals."""
        if self.send_thread and self.send_thread.is_alive():
            logger.warning("Sender is already running.")
            return

        self.stop_event.clear()
        self.send_thread = threading.Thread(target=self._send_loop)
        self.send_thread.start()
        logger.info("Sender started.")

    def stop(self):
        """Stop sending telemetry data."""
        if self.send_thread:
            self.stop_event.set()
            self.send_thread.join()
            self.send_thread = None
            logger.info("Sender stopped.")

    def _send_loop(self):
        last_send_time = 0
        while not self.stop_event.is_set():
            current_time = time.time()
            if current_time - last_send_time >= self.send_interval:
                self.send_telemetry()
                last_send_time = current_time
            time.sleep(0.1)  # Sleep for a short interval

    def send_telemetry(self):
        """Send telemetry data immediately."""
        try:
            metrics = self.metrics_store.get_metrics()
            payload = {
                "identifier": self.device_id,
                "timestamp": datetime.now().isoformat(),
                "metrics": metrics,
            }
            response = requests.post(
                f"{self.api_url}/api/telemetry",
                json=payload,
                headers={"x-api-key": self.api_key},
            )
            response.raise_for_status()
            logger.info(f"Telemetry sent successfully: {response.json()}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error sending telemetry: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error while sending telemetry: {e}")
