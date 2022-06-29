"""
Copyright: Copyright (C) 2022 2DEVIATE Inc. - All Rights Reserved
Product: Standard
Description: Init file for flask and initializing of globals
Notifyees: craig@2deviate.com
Category: None
"""

# third-party imports
from flask import Flask
from flask_marshmallow import Marshmallow

# local imports
from . import api
from .db import db
from .map import maps


def create_app(config):
    app = Flask(__name__, static_url_path="/static/")    
    # load configurations
    app.config.from_object(config)    
    # setup serializers
    Marshmallow(app)
    # initialize app database
    db.init_app(app)
    # initialize maps
    maps.init_app(app)
    # initialize api app
    api.init_app(app)
    # return instance
    return app
