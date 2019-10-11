import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class AppLogger:

    @staticmethod
    def info(msg, *args, **kwargs):
        logger.info(msg, args, kwargs)

    @staticmethod
    def debug(msg, *args, **kwargs):
        logger.debug(msg, args, kwargs)

    @staticmethod
    def critical(msg, *args, **kwargs):
        logger.critical(msg, args, kwargs)

    @staticmethod
    def error(msg, *args, **kwargs):
        logger.info(msg, args, kwargs)

    @staticmethod
    def exception(msg, *args, **kwargs):
        logger.exception(msg, args, kwargs)
