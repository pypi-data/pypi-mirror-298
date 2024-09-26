# src/ticos_agent/utils/logging_setup.py
import logging
from logging.config import dictConfig
import yaml


def setup_logging(default_path="config/logging.yaml", default_level=logging.INFO):
    try:
        with open(default_path, "rt") as f:
            config = yaml.safe_load(f.read())
        dictConfig(config)
    except Exception as e:
        print(f"Error in Logging Configuration: {e}")
        logging.basicConfig(level=default_level)
