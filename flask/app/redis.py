"""
Copyright: Copyright (C) 2022 2DEVIATE Inc. - All Rights Reserved
Product: Standard
Description: Redis Cache connector.  Implementation of Redis Cache objects
Notifyees: craig@2deviate.com
Category: None
"""
import os
import redis
import pickle
import logging


logger = logging.getLogger(__name__)


class RedisStore(object):
    def __init__(self):
        self.cache = None
        self.cache_redis_host = None
        self.cache_redis_port = None
        self.cache_redis_db = None

    def init_app(self, app):
        config = app.config
        logger.info(f"Init cache connection, {config=}")
        try:

            self.cache_redis_host = os.getenv("CACHE_REDIS_HOST", None)
            self.cache_redis_port = os.getenv("CACHE_REDIS_PORT", None)
            self.cache_redis_password = os.getenv("CACHE_REDIS_PASSWORD", None)
            self.cache_redis_db = os.getenv("CACHE_REDIS_DB", None)
            self.cache_redis_url = os.getenv("CACHE_REDIS_URL", None)
            self.cache_type = os.getenv("CACHE_TYPE", None)
            self.cache_default_timeout = os.getenv("CACHE_DEFAULT_TIMEOUT", None)

            self.config = {
                "CACHE_REDIS_HOST": self.cache_redis_host,
                "CACHE_REDIS_PORT": self.cache_redis_port,
                "CACHE_REDIS_PASSWORD": self.cache_redis_password,
                "CACHE_REDIS_DB": self.cache_redis_db,
                "CACHE_REDIS_URL": self.cache_redis_url,
                "CACHE_TYPE": self.cache_type,
                "CACHE_DEFAULT_TIMEOUT": self.cache_default_timeout
            }

            pool = redis.ConnectionPool(
                host=self.cache_redis_host,
                port=self.cache_redis_port,
                db=self.cache_redis_db,
            )
            self.cache = redis.Redis(connection_pool=pool)

            logger.info(
                f"Redis cache initialized, {self.cache_redis_host=}, {self.cache_redis_port=}, {self.cache_redis_db=}"
            )
        except Exception as err:
            logger.error(err, exc_info=err)
            raise

    def get(self, key, ignore_expired=False):
        if not ignore_expired:
            obj = self.cache.get(key)
            if obj:
                return pickle.loads(obj)

    def set(self, key, value):
        obj = pickle.dumps(value)
        if obj:
            self.cache.set(key, obj)


store = RedisStore()
