import logging
import sys


def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Get a logger with the specified name and level.

    Args:
        name (str): The name of the logger.
        level (str): The logging level (default is "INFO").

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)

    # Set the logging level
    level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(level)

    # Create a formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Create a stream handler (outputs to console)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(stream_handler)

    return logger
