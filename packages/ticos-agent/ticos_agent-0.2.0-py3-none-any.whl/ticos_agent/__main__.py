# src/ticos_agent/__main__.py

import argparse
import signal
import sys
from .core.agent import Agent
from .services.logger import get_logger

logger = get_logger(__name__)


def signal_handler(signum, frame):
    logger.info("Received signal to stop: %s", signum)
    agent.stop()
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="Ticos Agent")
    parser.add_argument("--config", help="Path to configuration file", required=True)
    args = parser.parse_args()

    global agent
    agent = Agent(args.config)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        agent.start()
        # Keep the main thread alive
        signal.pause()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    finally:
        agent.stop()


if __name__ == "__main__":
    main()
