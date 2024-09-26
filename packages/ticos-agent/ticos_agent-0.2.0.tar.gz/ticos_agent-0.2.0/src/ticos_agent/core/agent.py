# src/ticos_agent/core/agent.py

from .config import Config
from .collector import Collector
from .sender import Sender
from ..services import get_logger, MetricsStore

logger = get_logger(__name__)


class Agent:
    def __init__(self, config_path):
        self.config = Config(config_path)
        self.metrics_store = MetricsStore()
        self.collector = Collector(self.config, self.metrics_store)
        self.sender = Sender(self.config, self.metrics_store)

    def start(self):
        logger.info("Starting Ticos Agent")
        self.collector.start()
        self.sender.start()

    def stop(self):
        logger.info("Stopping Ticos Agent")
        self.collector.stop()
        self.sender.stop()
