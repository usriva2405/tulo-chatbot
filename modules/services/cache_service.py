from cachetools import TTLCache, cached
from modules.utils.yaml_parser import Config

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class CacheService:

    # retrieve caching properties from config
    cache_ttl = int(Config.get_config_val(key="cache", key_1depth="ttl"))
    cache_max_size = int(Config.get_config_val(key="cache", key_1depth="max_size"))

    # create a cache service
    cache = TTLCache(maxsize=cache_max_size, ttl=cache_ttl)

    @classmethod
    def get_object(cls, key):
        """
        retrieves the object from cache
        :param key:
        :return:
        """
        value = None
        try:
            value = cls.cache[key]
        except KeyError as ke:
            logger.error("Either key expired or not present : {0}".format(ke))
            value = None
        except Exception as e:
            logger.error("internal exception while using cache : {0}".format(e))
            value = None
        return value

    @classmethod
    def set_object(cls, key, value):
        logger.info("key : {0}, value : {1}".format(key, value))
        cls.cache[key] = value

    @classmethod
    def remove_objects(cls, key):
        try:
            logger.info("removing value from cache for : {0}".format(key))
            cls.cache.pop(key)
        except KeyError as ke:
            logger.error("already removed from cache for key : {0}. Exception is : {1}".format(key, ke))