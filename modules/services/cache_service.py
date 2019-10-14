import os
import redis
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
    cache = redis.from_url(Config.get_config_val(key="cache", key_1depth="redis_url")) # instead use a wrapper and retrieve from os.environ.get("REDIS_URL")

    # create a cache service
    # cache = TTLCache(maxsize=cache_max_size, ttl=cache_ttl)

    @classmethod
    def get_object(cls, key):
        """
        retrieves the object from cache
        :param key:
        :return:
        """
        value = None
        try:
            if cls.cache.exists(key) == 1:
                value = cls.cache.get(key).decode("utf-8")
            else:
                value = None
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
        cls.cache.set(key, value, ex=cls.cache_ttl)

    @classmethod
    def remove_objects(cls, key):
        try:
            logger.info("removing value from cache for : {0}".format(key))
            cls.cache.delete(key)
        except KeyError as ke:
            logger.error("already removed from cache for key : {0}. Exception is : {1}".format(key, ke))