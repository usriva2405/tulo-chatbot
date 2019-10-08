import logging


class AppLogger:

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    logger = logging.getLogger(__name__)

    @classmethod
    def info(cls, msg, *args, **kwargs):
        cls.logger.info(msg, args, kwargs)

    @classmethod
    def debug(cls, msg, *args, **kwargs):
        cls.logger.debug(msg, args, kwargs)

    @classmethod
    def critical(cls, msg, *args, **kwargs):
        cls.logger.critical(msg, args, kwargs)

    @classmethod
    def error(cls, msg, *args, **kwargs):
        cls.logger.info(msg, args, kwargs)

    @classmethod
    def exception(cls, msg, *args, **kwargs):
        cls.logger.exception(msg, args, kwargs)
