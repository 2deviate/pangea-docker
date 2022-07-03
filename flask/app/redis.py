"""
Copyright: Copyright (C) 2022 2DEVIATE Inc. - All Rights Reserved
Product: Standard
Description: Database connector.  Implementation of MySql data connector
Notifyees: craig@2deviate.com
Category: None
"""
import os
import logging
from flask_caching import Cache

logger = logging.getLogger(__name__)


class Redis(object):
    def __init__(self) -> None:
        self.cache = None
        self.cache_debug = None
        self.cache_type = None
        self.cache_default_timeout = None

    def init_app(self, app):
        config = app.config        
        logger.info(f"Init cache connection, {config=}")
        try:
            self.cache_debug = os.getenv("REDIS_CACHE_DEBUG", None)
            self.cache_type = os.getenv("REDIS_CACHE_TYPE", None)
            self.cache_default_timeout = os.getenv("CACHE_DEFAULT_TIMEOUT", None)

            config = {
                "DEBUG": self.cache_type,
                "CACHE_TYPE": self.cache_type,
                "CACHE_DEFAULT_TIMEOUT": self.cache_default_timeout,
            }            
            
            self.cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
            self.cache.init_app(app)
            
            logger.info(
                f"Redis cache initialized, {self.cache_debug=}, {self.cache_type=}, {self.cache_default_timeout=}"
            )
        except Exception as err:
            logger.error(err, exc_info=err)
            raise


redis = Redis()