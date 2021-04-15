from loguru import logger


def setup_loguru():
    logger.add("logs/backend.log", level="INFO", rotation="100 MB")
    logger.add("logs/debug.log", level="DEBUG", rotation="100 MB")
    logger.add("logs/error.log", level="ERROR", rotation="100 MB")
