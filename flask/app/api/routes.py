"""
Copyright: Copyright (C) 2022 2DEVIATE Inc. - All Rights Reserved
Product: Standard
Description: Routing urls for the Api
Notifyees: craig@2deviate.com
Category: None
"""

# third-party imports
from flask import Blueprint
from flask_restful import Api

# local imports
from .resources import (
    FttpExchangesAPI,
    FttpExchangeAPI,
    SamExchangeAPI,
    DecommissionExchangeAPI,
    LocationAPI,
    DownloadAPI,
    UploadAPI,
    RecommendationAPI,
)

# pylint: disable=invalid-name
api_bp = Blueprint("api/", __name__)

api = Api(api_bp)

# Openreach FTTP API - fetches all decommission data loaded in MySQL from Openreach
api.add_resource(
    FttpExchangesAPI, "/v1.0/pangea/fttp/exchanges", methods=["GET"], endpoint="/"
)

# Openreach FTTP API - fetches decommisioned exchange data based on lookup site, name, code and location
# http://localhost:5000/api/v1.0/pangea/fttp/exchange/site/5
api.add_resource(
    FttpExchangeAPI,
    "/v1.0/pangea/fttp/exchange/site/<site_no>",
    methods=["GET"],
    endpoint="site",
)
# http://localhost:5000/api/v1.0/pangea/fttp/exchange/name/Failsworth
api.add_resource(
    FttpExchangeAPI,
    "/v1.0/pangea/fttp/exchange/name/<exchange_name>",
    methods=["GET"],
    endpoint="name",
)
# http://localhost:5000/api/v1.0/pangea/fttp/exchange/code/NICTY
api.add_resource(
    FttpExchangeAPI,
    "/v1.0/pangea/fttp/exchange/code/<exchange_code>",
    methods=["GET"],
    endpoint="code",
)
# http://localhost:5000/api/v1.0/pangea/fttp/exchange/location/Belfast
api.add_resource(
    FttpExchangeAPI,
    "/v1.0/pangea/fttp/exchange/location/<exchange_location>",
    methods=["GET"],
    endpoint="location",
)

# Sam Exchange API - searches sam knows api (curl) for exchange related data
# http://localhost:5000/api/v1.0/pangea/sam/exchange/info?query=London
# http://localhost:5000/api/v1.0/pangea/sam/exchange/info?exchange_code=WSKIL
api.add_resource(
    SamExchangeAPI, "/v1.0/pangea/sam/exchange/info", methods=["GET"], endpoint="info"
)

# Decommission Exchange API - searches sam knows api (curl) for exchange related data
# http://localhost:5000/api/v1.0/pangea/decommission/exchange/search?query=morley
api.add_resource(
    DecommissionExchangeAPI,
    "/v1.0/pangea/decommission/exchange/search",
    methods=["GET"],
    endpoint="search",
)

# Geolocation API - searches geolocations for location data given a location
# http://localhost:5000/api/v1.0/pangea/location/search?postcode=BR33RF
api.add_resource(
    LocationAPI, "/v1.0/pangea/location/search", methods=["GET"], endpoint="postcode"
)

# Download API - downloads template for bulk queries
# http://localhost:5000/api/v1.0/pangea/download/template
api.add_resource(
    DownloadAPI, "/v1.0/pangea/download/template", methods=["GET"], endpoint="template"
)

# Upload API - uploads template for bulk queries
# http://localhost:5000/api/v1.0/pangea/upload/file/{form}
api.add_resource(
    UploadAPI, "/v1.0/pangea/upload/file", methods=["POST"]
)

# Recommendation API - recommends a product based on usage
# http://localhost:5000/api/v1.0/pangea/recommendation/product/usage?limit=130
api.add_resource(
    RecommendationAPI, "/v1.0/pangea/recommendation/product/usage", methods=["GET"], endpoint="usage"    
)

