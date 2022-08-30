"""
Copyright: Copyright (C) 2022 2DEVIATE Inc. - All Rights Reserved
Product: Standard
Description: Celery Tasks
Notifyees: craig@2deviate.com
Category: None
"""
import logging
from celery import Celery

logger = logging.getLogger(__name__)


class Scheduler(object):
    def __init__(self):
        self.cache = None
        self.cache_redis_host = None
        self.cache_redis_port = None
        self.cache_redis_db = None

    def init_app(self, app):
        celery.app = app
        config = app.config        
        logger.info(f"Init async tasks, {config=}")
        try:            
            logger.info(
                f"Celery initialized, {self.cache_redis_host=}, {self.cache_redis_port=}, {self.cache_redis_db=}"
            )
        except Exception as err:
            logger.error(err, exc_info=err)
            raise

scheduler = Scheduler()
