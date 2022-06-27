"""
Copyright: Copyright (C) 2022 2DEVIATE Inc. - All Rights Reserved
Product: Standard
Description: Configuration file for the application.
Notifyees: craig@2deviate.com
Category: None
"""

import logging
import os

basedir = os.path.abspath(os.path.dirname(__file__))  # pylint: disable=invalid-name


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

    # Local MySql configuration (NOT AWS RDS)
    MYSQL_USER = os.getenv("MYSQL_USER", None)
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", None)
    MYSQL_HOST = os.getenv("MYSQL_HOST", None)
    MYSQL_PORT = os.getenv("MYSQL_PORT", None)
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", None)

    # Docker Service configurations
    DOCKER_DB_NAME = os.getenv("DOCKER_DB_NAME", None)
    DOCKER_SERVER_NAME = os.getenv("DOCKER_SERVER_NAME", None)
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
    EMAIL_ATTACHMENT = os.getenv("EMAIL_ATTACHMENT", None)
    EMAIL_SUBJECT = os.getenv("EMAIL_SUBJECT", None)
    
    DEFAULT_TEMPLATE_SCHEMA = {
            "client_id": "Client ID",
            "exchange_name": "Exchange Name",
            "exchange_code": "Exchange Code",
            "exchange_post_code": "Exchange Post Code",
            "avg_data_usage": "Average Data Usage (MB)",
            "stop_sell_date": "Stop Sell Date",    
            "exchange_product_name": "Product Name",
            "exchange_product_limit": "Product Limit (MB)" ,
            "exchange_product_unit": "Product Unit",
            "exchange_product_url": "Recommendation",    
            "exchange_product_price": "Price (GBP)",
            "created_at": "Created At"
    }
    EMAIL_TEMPLATE_SCHEMA = os.getenv("EMAIL_TEMPLATE_SCHEMA", DEFAULT_TEMPLATE_SCHEMA)
        
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
