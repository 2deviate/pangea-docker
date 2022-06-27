"""
Copyright: Copyright (C) 2022 2DEVIATE Inc. - All Rights Reserved
Product: Standard
Description: Schema Class.  Implementation of Data Schemas
Notifyees: craig@2deviate.com
Category: None
"""
from marshmallow import Schema, fields


class SamExchangeSchema(Schema):
    exchange_name = fields.String()
    exchange_code = fields.String()
    exchange_county = fields.String()
    exchange_region = fields.String()
    exchange_postcode = fields.String()
    exchange_serves = fields.String()


sam_exchange_schema = SamExchangeSchema()
sam_exchanges_schema = SamExchangeSchema(many=True)


class FttpExchangeSchema(Schema):
    id = fields.Integer()
    site_no = fields.String()
    exchange_name = fields.String()
    exchange_location = fields.String()
    exchange_code = fields.String()
    implementation_date = fields.String()
    last_amended_date = fields.String()
    tranche = fields.String()
    created_at = fields.DateTime()


fttp_exchange_schema = FttpExchangeSchema()
fttp_exchanges_schema = FttpExchangeSchema(many=True)


class DecommissionedExchangeSchema(FttpExchangeSchema, SamExchangeSchema):
    pass


decommission_exchange_schema = DecommissionedExchangeSchema()
decommissions_exchange_schema = DecommissionedExchangeSchema(many=True)


class LocationSchema(Schema):
    address_components = fields.List(fields.Dict())
    formatted_address = fields.String()
    geometry = fields.Dict()
    places_id = fields.String()
    types = fields.List(fields.String())


location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)


class ProductSchema(Schema):
    product_id = fields.String()
    product_name = fields.String()
    product_limit = fields.Integer()
    product_unit = fields.String()
    product_url = fields.String()
    product_status = fields.String()
    product_price = fields.Float()
    product_default = fields.Integer()


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
