"""Helpers module."""
import logging


def setup_logger(name: str, log_level: int = logging.INFO) -> logging.Logger:
    """Prepare useful logging.
    """
    logging.basicConfig(level=log_level)
    logging_handler: logging.StreamHandler = logging.StreamHandler()
    logging_handler.setFormatter(logging.Formatter("%(message)s"))
    prepared_logger: logging.Logger = logging.getLogger(name)
    prepared_logger.propagate = False
    prepared_logger.addHandler(logging_handler)
    return prepared_logger
