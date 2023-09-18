import logging.config

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger: logging.Logger = logging.getLogger(__name__)
