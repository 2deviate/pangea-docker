"""
Copyright: Copyright (C) 2022 2DEVIATE Inc. - All Rights Reserved
Product: Standard
Description: Map Class.  Implementation of Google mapping client
Notifyees: craig@2deviate.com
Category: None
"""
import logging
import googlemaps

logger = logging.getLogger(__name__)


class Maps(object):
    def __init__(self):
        self.client = None

    def init_app(self, app):
        key = app.config.get("GOOGLE_MAPS_API_KEY", None)
        self.client = googlemaps.Client(key=key) if key else None

    def request(self, query):
        result = None
        try:
            if self.client:
                result = self.client.geocode(query)
        except Exception as err:
            logger.error(err, exc_info=err)
        return result


maps = Maps()
