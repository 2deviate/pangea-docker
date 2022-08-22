"""
Copyright: Copyright (C) 2022 2DEVIATE Inc. - All Rights Reserved
Product: Standard
Description: Configuration file for the application.
Notifyees: craig@2deviate.com
Category: None
"""

import os
import json
import logging

basedir = os.path.abspath(os.path.dirname(__file__))  # pylint: disable=invalid-name

logger = logging.getLogger(__name__)


class Config(object):
    """
    Common configurations
    """
    # Should not be part of environment
    SECRET_KEY = os.getenv("SECRET_KEY", None)

    # Put any configurations here that are common across all environments
    LOGFILENAME = os.getenv("LOGFILENAME", "app.log")
    LOGLEVEL = os.getenv("LOGLEVEL", logging.INFO)    

    # Flask Environment
    FLASK_APP = os.getenv("FLASK_APP", None)
    FLASK_ENV = os.getenv("FLASK_ENV", None)
    FLASK_PORT = os.getenv("FLASK_PORT", None)
    FLASK_HOST = os.getenv("FLASK_HOST", None)
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", None)    

    # Application data paths
    FLASK_APP_TEMPLATE_NAME = os.getenv("FLASK_APP_TEMPLATE_NAME", None)
    FLASK_APP_UPLOAD_FOLDER = os.getenv("FLASK_APP_UPLOAD_FOLDER", None)
    FLASK_APP_DOWNLOAD_FOLDER = os.getenv("FLASK_APP_DOWNLOAD_FOLDER", None)    
    FLASK_FILE_UPLOAD_MAX_LENGTH = os.getenv("FLASK_APP_DOWNLOAD_FOLDER", None)

    # Cache Redis
    CACHE_REDIS_HOST = os.getenv("CACHE_REDIS_HOST", None)
    CACHE_REDIS_PORT = os.getenv("CACHE_REDIS_PORT", None)
    CACHE_REDIS_PASSWORD = os.getenv("CACHE_REDIS_PASSWORD", None)
    CACHE_REDIS_DB = os.getenv("CACHE_REDIS_DB", None)
    CACHE_REDIS_URL = os.getenv("CACHE_REDIS_URL", None)    
    CACHE_TYPE = os.getenv("CACHE_TYPE", None)
    CACHE_DEFAULT_TIMEOUT = os.getenv("CACHE_DEFAULT_TIMEOUT", None)

    # Local MySql configuration (NOT AWS RDS)
    MYSQL_USER = os.getenv("MYSQL_USER", None)
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", None)
    MYSQL_HOST = os.getenv("MYSQL_HOST", None)
    MYSQL_PORT = os.getenv("MYSQL_PORT", None)
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", None)
    MYSQL_ROOT_PASSWORD = os.getenv("MYSQL_DATABASE", None)

    # Docker Service configurations
    DOCKER_DB_NAME = os.getenv("DOCKER_DB_NAME", None)
    DOCKER_SERVER_NAME = os.getenv("DOCKER_SERVER_NAME", None)
    DOCKER_SERVER_PORT = os.getenv("DOCKER_SERVER_PORT", None)
    DOCKER_PROXY_NAME = os.getenv("DOCKER_PROXY_NAME", None)

    # Google Maps API Key
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", None)

    # SMTP configuration
    SMTP_USER = os.getenv("SMTP_USER", None)
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", None)
    SMTP_HOST = os.getenv("SMTP_HOST", None)
    SMTP_PORT = os.getenv("SMTP_PORT", None)

    ### Email Template
    EMAIL_FROM_ADDRESS = os.getenv("EMAIL_FROM_ADDRESS", None)
    EMAIL_CC_ADDRESSES = os.getenv("EMAIL_CC_ADDRESSES", None)
    EMAIL_BCC_ADDRESSES = os.getenv("EMAIL_BCC_ADDRESSES", None)
    EMAIL_ATTACHMENT = os.getenv("EMAIL_ATTACHMENT", None)
    EMAIL_SUBJECT = os.getenv("EMAIL_SUBJECT", None)

    ### Email Content
    EMAIL_TEMPLATE_TEXT = os.getenv("EMAIL_TEMPLATE_TEXT", None)
    EMAIL_TEMPLATE_HTML = os.getenv("EMAIL_TEMPLATE_HTML", None)
    
    EMAIL_TEMPLATE_SCHEMA = {
            "cli": "CLI",
            "site_postcode": "Site Post Code",
            "exchange_name": "Exchange Name",
            "exchange_code": "Exchange Code",
            "exchange_postcode": "Exchange Post Code",
            "avg_data_usage": "Average Data Usage (MB)",
            "stop_sell_date": "Stop Sell Date",    
            "exchange_product_name": "Product Name",
            "exchange_product_limit": "Product Limit" ,
            "exchange_product_unit": "Product Unit",
            "exchange_product_url": "Recommendation",    
            "exchange_product_price": "Price (GBP)",
            "exchange_product_term": "Term",
            "created_at": "Created At"
    }
    
    schema = os.getenv("EMAIL_TEMPLATE_SCHEMA", None)
    if schema and isinstance(schema, str):
        try:
            EMAIL_TEMPLATE_SCHEMA = json.loads(schema) # acts as an override
        except Exception as err:
            logger.error(f"Failed to parse template {schema=}, defaulting {EMAIL_TEMPLATE_SCHEMA=}", err)
        
    PROXY_SERVER = os.getenv("PROXY_SERVER", None)

class ProductionConfig(Config):
    """
    Production configurations
    """

    LOGLEVEL = logging.ERROR
    FLASK_DEBUG = False


class StagingConfig(Config):
    """
    Staging configurations
    """

    LOGLEVEL = logging.DEBUG
    FLASK_DEBUG = True


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    LOGLEVEL = logging.DEBUG
    FLASK_DEBUG = True


configs = {
    "dev": DevelopmentConfig,
    "uat": StagingConfig,
    "prod": ProductionConfig,
    "default": ProductionConfig,
}
