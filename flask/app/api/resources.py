"""
Copyright: Copyright (C) 2022 2DEVIATE Inc. - All Rights Reserved
Product: Standard
Description: Resources for the Api
Notifyees: craig@2deviate.com
Category: None
"""
# third-party imports
import os
import logging
import pandas
from flask import redirect, request
from flask_restful import Resource, reqparse
from flask import current_app, safe_join, send_from_directory

# local imports
from app import constants

from .models import (    
    FttpExchange,
    Product,
    SamExchange,
    Location,
    FileResource,
    FileStage,
    Allocation,
    ScriptExecute,
)
from app.api.schemas import (
    decommissions_exchange_schema,
    decommission_exchange_schema,
    sam_exchanges_schema,
    sam_exchange_schema,
    fttp_exchanges_schema,
    fttp_exchange_schema,
    locations_schema,
    product_schema,
)
from app.utils import response_json

logger = logging.getLogger(__name__)


class HealthAPI(Resource):
    """
    This API represents health API
    """

    def __init__(self):        
        super(HealthAPI, self).__init__()
    
    def get(self):                
        return response_json(True, [], constants.DATA_OPERATION_SUCCESSFUL), 200

    def post(self):
        pass


class FttpExchangesAPI(Resource):
    """
    This class represents all FTTP Openreach exchanges API.
    The FTTP Priority Exchanges are a list of Exchanges where order restrictions will be /and are applied
    by date.
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()  # pylint: disable=invalid-name
        self.parser.add_argument("limit", type=int)
        super(FttpExchangesAPI, self).__init__()

    def get(self):
        args = self.parser.parse_args()
        limit = args["limit"]

        if not (limit):
            limit = 100

        results = None
        if limit:
            results, _ = FttpExchange.find_by_limit(limit)

        if results:
            return fttp_exchanges_schema.dump(
                [serialize_fttp_exchange(result) for result in results]
            )
        else:
            return response_json(True, results, constants.QUERY_MISSING_PARAMS)

    def put(self):
        pass


class FttpExchangeAPI(Resource):
    """
    This class represents a single FTTP Openreach exchange API
    FTTP Priority Exchanges: List of Exchanges  where order restrictions will be / are applied
    """

    def get(
        self,
        site_no=None,
        exchange_name=None,
        exchange_code=None,
        exchange_location=None,
    ):

        if not (site_no or exchange_name or exchange_code or exchange_location):
            return response_json(True, {}, constants.QUERY_MISSING_PARAMS)

        results = None

        if site_no:
            results, _ = FttpExchange.find_by_site_no(site_no)

        if exchange_name:
            results, _ = FttpExchange.find_by_exchange_name(exchange_name)

        if exchange_code:
            results, _ = FttpExchange.find_by_exchange_code(exchange_code)

        if exchange_location:
            results, _ = FttpExchange.find_by_exchange_location(exchange_location)

        if results and len(results) == 1:
            return fttp_exchange_schema.dump(serialize_fttp_exchange(results[0]))
        elif results and len(results) > 1:
            return fttp_exchanges_schema.dump(
                [serialize_fttp_exchange(result) for result in results]
            )
        else:
            return response_json(True, results, constants.NO_DATA_RESULTS_FOUND)

    def post(self):
        pass


class SamExchangeAPI(Resource):
    """
    This API represents a SamKnows Exchange API
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()  # pylint: disable=invalid-name
        self.parser.add_argument("query", type=str)
        self.parser.add_argument("exchange_code", type=str)
        super(SamExchangeAPI, self).__init__()

    def get(self):
        args = self.parser.parse_args()
        query = args["query"]
        exchange_code = args["exchange_code"]

        if not (query or exchange_code):
            return response_json(True, {}, constants.QUERY_MISSING_PARAMS)

        results = []

        if query:
            results = SamExchange.find_by_query(query)
            if results and len(results) == 1:
                return sam_exchange_schema.dump(serialize_sam_exchange(results[0]))
            elif results and len(results) > 1:
                return sam_exchanges_schema.dump(
                    [serialize_sam_exchange(result) for result in results]
                )
            else:
                return response_json(True, results, constants.NO_DATA_RESULTS_FOUND)

        if exchange_code:
            results = SamExchange.find_by_exchange_code(exchange_code)
            if results:
                return sam_exchange_schema.dump(
                    serialize_sam_exchange_location(results)
                )
            else:
                return response_json(True, results, constants.NO_DATA_RESULTS_FOUND)

    def post(self):
        pass


class DecommissionExchangeAPI(Resource):
    """
    This class represents a Decommissioned Exchange API
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()  # pylint: disable=invalid-name
        self.parser.add_argument("query", type=str)
        super(DecommissionExchangeAPI, self).__init__()

    def get(self):
        args = self.parser.parse_args()
        query = args["query"]

        if not (query):
            return response_json(True, {}, constants.QUERY_MISSING_PARAMS)

        # find exchange source data
        sam_exchanges = []
        sam_results = SamExchange.find_by_query(query)
        if sam_results and len(sam_results) == 1:
            sam_exchanges.append(serialize_sam_exchange(sam_results[0]))
        elif sam_results and len(sam_results) > 1:
            sam_exchanges = [
                serialize_sam_exchange(sam_result) for sam_result in sam_results
            ]

        # find fttp related data, if it exists then combine
        results = []
        for sam_exchange in sam_exchanges:
            fttp_results, _ = FttpExchange.find_by_exchange_code(
                sam_exchange["exchange_code"]
            )
            if fttp_results and len(fttp_results) == 1:
                results.append(
                    {**serialize_fttp_exchange(fttp_results[0]), **sam_exchange}
                )
            elif fttp_results and len(fttp_results) > 1:
                for fttp_result in fttp_results:
                    results.append(
                        {**serialize_fttp_exchange(fttp_result), **sam_exchange}
                    )

        for result in results:
            exchange_code = result["exchange_code"]
            if exchange_code:
                sam_results = SamExchange.find_by_exchange_code(exchange_code)
                result.update({**serialize_sam_exchange_location(sam_results)})

        if results and len(results) == 1:
            return decommission_exchange_schema.dump(results[0])
        elif results and len(results) > 1:
            return decommissions_exchange_schema.dump([result for result in results])
        else:
            return response_json(True, results, constants.NO_DATA_RESULTS_FOUND)

    def post(self):
        pass


class LocationAPI(Resource):
    """
    This API represents a geolocation lookup
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()  # pylint: disable=invalid-name
        self.parser.add_argument("postcode", type=str)
        super(LocationAPI, self).__init__()

    def get(self):
        args = self.parser.parse_args()
        postcode = args["postcode"]

        if not (postcode):
            return response_json(True, {}, constants.QUERY_MISSING_PARAMS)

        results = Location.find_by_postcode(postcode)

        if results:
            return locations_schema.dump(
                [serialize_map_location(result) for result in results]
            )
        else:
            return response_json(True, results, constants.NO_DATA_RESULTS_FOUND)

    def post(self):
        pass


class DownloadAPI(Resource):
    """
    This API represents a download API
    """

    def __init__(self):
        self.config = current_app.config
        super(DownloadAPI, self).__init__()

    def get(self):
        config = self.config
        download, template = FileResource.template(config)
        try:
            if download and template:            
                directory = safe_join(current_app.root_path, download) # running locally                
                #directory = safe_join(os.getcwd(), download) # running in docker container https://stackoverflow.com/questions/53725478/download-file-from-flask-application-running-in-docker-container
                logger.info(f"downloading path, {download=}, {template=}, {directory}=")
                return send_from_directory(directory=directory, path=template)
        except Exception as ex:
            logger.error(f"error downloading, {download=}, {template=}", ex)
            pass

    def post(self):
        pass


class UploadAPI(Resource):
    """
    This API represents an upload API
    """

    def __init__(self):
        self.config = current_app.config
        self.parser = reqparse.RequestParser()  # pylint: disable=invalid-name
        self.parser.add_argument("email", type=str)
        super(UploadAPI, self).__init__()

    def get(self):
        pass

    def post(self):
        args = self.parser.parse_args()
        email = args["email"]
        if "file" not in request.files:            
            return redirect(request.url)
        resource = request.files["file"]
        if resource.filename == "":            
            return redirect(request.url)
        path = os.path.join(current_app.root_path, self.config["FLASK_APP_UPLOAD_FOLDER"])
        try:
            results = FileResource.upload(path, resource)
            status = results.get("status", None)
            if status == "Success":
                filename = results.get("filename", None)
                if filename:
                    *_, last_bulk_row_id = FileStage.insert(email, filename)
                    if last_bulk_row_id and last_bulk_row_id > 0:
                        results["last_row_id"] = last_bulk_row_id
            else:  # failed to upload
                pass
        except IOError:
            pass
        except Exception as e:
            pass
        if results:
            return response_json(True, results, constants.DATA_OPERATION_SUCCESSFUL)


class RecommendationAPI(Resource):
    """
    This API represents a recommendation API
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()  # pylint: disable=invalid-name
        self.parser.add_argument("limit", type=str)
        super(RecommendationAPI, self).__init__()
    
    def get(self):
        args = self.parser.parse_args()
        limit = args["limit"]

        if not (limit):
            return response_json(True, {}, constants.QUERY_MISSING_PARAMS)

        results, _ = Product.find_by_limit(limit)

        if results:
            return product_schema.dump(serialize_product(results[0]))
        else:
            return response_json(True, results, constants.NO_DATA_RESULTS_FOUND)

    def post(self):
        pass


class AllocationAPI(Resource):
    """
    This API represents a resource allocation API
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()  # pylint: disable=invalid-name
        self.parser.add_argument("sql", type=str)
        super(AllocationAPI, self).__init__()

    def get(self):
        args = self.parser.parse_args()
        sql = args["sql"]

        if not (sql):
            return response_json(True, {}, constants.QUERY_MISSING_PARAMS)

        results, _ = Allocation.execute_sql(sql)

        if results:
            df = pandas.DataFrame(results)
            return response_json(True, df.to_json(), constants.DATA_OPERATION_SUCCESSFUL)
        
        return response_json(True, results, constants.DATA_OPERATION_SUCCESSFUL)

    def post(self):
        pass


class ScriptEtlAPI(Resource):
    """
    This API represents a script API
    """

    def __init__(self):
        self.script = f'/home/app/etl.sh'
        super(ScriptEtlAPI, self).__init__()

    def get(self):
        stdout = ScriptExecute.execute(self.script)        
        if stdout:
            return response_json(True, f'<pre>{stdout}</pre>', constants.DATA_OPERATION_SUCCESSFUL)        
        return response_json(True, [], constants.DATA_OPERATION_SUCCESSFUL)

    def post(self):
        pass


class ScriptNotifyAPI(Resource):
    """
    This API represents a script API
    """

    def __init__(self):
        self.script = f'/home/app/notifier.sh'
        super(ScriptNotifyAPI, self).__init__()

    def get(self):
        stdout = ScriptExecute.execute(self.script)        
        if stdout:
            return response_json(True, f'<pre>{stdout}</pre>', constants.DATA_OPERATION_SUCCESSFUL)        
        return response_json(True, [], constants.DATA_OPERATION_SUCCESSFUL)

    def post(self):
        pass    

def serialize_product(product):
    return {
        "product_id": product[0],
        "product_name": product[1],
        "product_limit": product[2],
        "product_unit": product[3],
        "product_url": product[4],
        "product_price": product[5],
        "product_default": ord(product[6]),
        "product_status": product[7],        
    }


def serialize_map_location(location):
    return {
        "address_components": location["address_components"],
        "formatted_address": location["formatted_address"],
        "geometry": location["geometry"],
        "place_id": location["place_id"],
        "types": location["types"],
    }


def serialize_fttp_exchange(exchange):
    return {
        "id": exchange[0],
        "site_no": exchange[1],
        "exchange_name": exchange[2],
        "exchange_location": exchange[3],
        "exchange_code": exchange[4],
        "implementation_date": exchange[5],
        "last_amended_date": str(exchange[6]),
        "tranche": exchange[7],
        "created_at": exchange[8],
    }


def serialize_sam_exchange(exchange):
    return {
        "exchange_name": exchange[0],
        "exchange_code": exchange[1],
        "exchange_county": exchange[2],
        "exchange_region": exchange[3],
    }


def serialize_sam_exchange_location(exchange):
    return {
        "exchange_name": exchange["Exchange name"],
        "exchange_code": exchange["Exchange code"],
        "exchange_location": exchange["Location"],
        "exchange_postcode": exchange["Postcode"],
        "exchange_maps": exchange["Maps"],
        "exchange_serves": exchange["Serves (approx)"],
    }
