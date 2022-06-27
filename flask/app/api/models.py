"""
Copyright: Copyright (C) 2022 2DEVIATE Inc. - All Rights Reserved
Product: Standard
Description: Models for the Api app
Notifyees: craig@2deviate.com
Category: None
"""

# local imports
import os
import csv
import uuid
import logging
import phonenumbers
import datetime
import app.constants as const
from decimal import Decimal
from dateutil import parser
from app.sam import sam
from app.map import maps
from app.db import db
from pymysql import NULL
from ukpostcodeutils import validation
from werkzeug.utils import secure_filename


logger = logging.getLogger(__name__)


class FttpExchange(object):
    """
    This class represents an simple fttp exchange object
    """

    def __init__(self, **kwargs):
        self.identity = kwargs.get("id", None)
        self.site_no = kwargs.get("site_no", None)
        self.exchange_name = kwargs.get("exchange_name", None)
        self.exchange_location = kwargs.get("exchange_location", None)
        self.exchange_code = kwargs.get("exchange_code", None)
        self.implementation_date = kwargs.get("implementation_date", None)
        self.last_amended_date = kwargs.get("last_amended_date", None)
        self.tranche = kwargs.get("tranche", None)
        self.created_at = kwargs.get("created_at", None)

    def __repr__(self):
        return "<id: {}>".format(self.identity)

    @staticmethod
    def find_by_limit(limit):
        return db.execute(const.SP_GET_EXCHANGE_DECOM_BY_LIMIT, limit)

    @staticmethod
    def find_by_site_no(site_no):
        return db.execute(const.SP_GET_EXCHANGE_DECOM_BY_SITE, site_no)

    @staticmethod
    def find_by_exchange_name(exchange_name):
        return db.execute(const.SP_GET_EXCHANGE_DECOM_BY_EXCHANGE_NAME, exchange_name)

    @staticmethod
    def find_by_exchange_code(exchange_code):        
        return db.execute(const.SP_GET_EXCHANGE_DECOM_BY_EXCHANGE_CODE, exchange_code)

    @staticmethod
    def find_by_exchange_location(exchange_location):        
        return db.execute(const.SP_GET_EXCHANGE_DECOM_BY_EXCHANGE_LOCATION, exchange_location)


class SamExchange(object):
    """
    This class represents an SamKnows Exchange object
    """

    def __init__(self, **kwargs):
        self.exchange = kwargs.get("exchange", None)

    def __repr__(self):
        return "<exchange: {}>".format(self.exchange)

    @staticmethod
    def find_by_query(query):
        url = "https://availability.samknows.com/broadband/exchange_search"
        return sam.request(method="POST", query=query, url=url, scraper=sam.scrape_info)

    @staticmethod
    def find_by_exchange_code(exchange_code):
        url = f"https://availability.samknows.com/broadband/exchange/{exchange_code}"
        return sam.request(method="GET", url=url, scraper=sam.scrape_exchange)


class Exchange(object):
    """
    This class represents an simple Exchange object
    """

    def __init__(self, **kwargs):
        self.postcode = kwargs.get("postcode", None)
        self.telephone = kwargs.get("telephone", None)

    def __repr__(self):
        return "<postcode: {}>".format(self.postcode)

    @staticmethod
    def find_by_postcode(postcode):
        return sam.request(postcode)

    @staticmethod
    def find_by_telephone(telephone):
        return sam.request(telephone)

    @staticmethod
    def validate_postcode(postcode):
        return validation.is_valid_postcode(postcode)

    @staticmethod
    def validate_telephone(telephone):
        is_valid = False
        try:
            # try and parse into telephone number
            number = phonenumbers.parse(telephone, "GB")
            if isinstance(number, phonenumbers.PhoneNumber):
                is_valid = True
        except phonenumbers.NumberParseException as ex:
            logger.error("Invalid telephone", ex)
        return is_valid


class Product(object):
    """
    This class represents an simple Product object
    """

    def __init__(self, **kwargs):
        self.usage = kwargs.get("limit", None)

    def __repr__(self):
        return "<limit: {}>".format(self.limit)

    @staticmethod
    def find_by_limit(limit):
        return db.execute(const.SP_EXCHANGE_PRODUCT_FIND_BY_LIMIT, limit, const.PRODUCT_STATUS_AVAILABLE)        


class Location(object):
    """
    This class represents an simple geolocation object
    """

    def __init__(self, **kwargs):
        self.postcode = kwargs.get("postcode", None)

    def __repr__(self):
        return "<postcode: {}>".format(self.postcode)

    @staticmethod
    def find_by_postcode(postcode):
        return maps.request(postcode)


class FileResource(object):
    """
    This class represents a file resource object
    """

    @staticmethod
    def template(config):
        download = config.get("FLASK_APP_DOWNLOAD_FOLDER", None)
        template = config.get("FLASK_APP_TEMPLATE_NAME", None)        
        return download, template

    @staticmethod
    def upload(folder, resource):
        if resource and FileResource.is_allowed_extension(resource.filename):
            temp_name = FileResource.get_temporary_name(prefix="", suffix=".csv")
            secure_name = secure_filename(temp_name)
            filename = os.path.join(folder, secure_name)
            try:
                resource.save(filename)
            except IOError:
                raise
            return {"filename": filename, "status": "Success"}

    @staticmethod
    def is_allowed_extension(filename):
        return "." in filename and filename.rsplit(".", 1)[1].lower() in ["csv"]

    @staticmethod
    def get_temporary_name(prefix, suffix):
        unique = uuid.uuid4().hex
        name = unique[:3] + unique[:2]
        return prefix + name + suffix


class FileStage(object):
    """
    This class represents a file stage object
    """
        
    class Row(object):
        def __init__(self, *args) -> None:
            self.client_id = args[0] if args[0] else None
            self.exchange_name = args[1] if args[1] else None
            self.exchange_code = args[2] if args[2] else None
            self.exchange_post_code = args[3] if args[3] else None
            self.avg_data_usage = args[4] if args[4] else None
            self.file_stage_fk = args[5] if args[5] else None
            # implemented place holder fields
            self.stop_sell_date = None
            self.exchange_product_fk = None            

        def values(self):
            client_id = str(self.client_id) if self.client_id else None
            exchange_name = str(self.exchange_name) if self.exchange_name else None
            exchange_code = str(self.exchange_code) if self.exchange_code else None
            exchange_post_code = str(self.exchange_post_code) if self.exchange_post_code else None
            avg_data_usage = int(self.avg_data_usage) if self.avg_data_usage else None
            
            stop_sell_date = None
            try:
                if self.stop_sell_date or self.stop_sell_date is not None:
                    stop_sell_date = (parser.parse(self.stop_sell_date).date().strftime("""%Y-%m-%d"""))
            except parser.ParserError as err:
                pass                
            
            file_stage_fk = int(self.file_stage_fk) if self.file_stage_fk else None             
            exchange_product_fk = int(self.exchange_product_fk) if self.exchange_product_fk else None

            return (client_id, exchange_name, exchange_code, exchange_post_code, avg_data_usage, stop_sell_date, file_stage_fk, exchange_product_fk)

    @staticmethod
    def find_by_status(status):        
        return db.execute(const.SP_GET_FILE_STAGE_BY_STATUS, status)                

    @staticmethod
    def insert(email, filename):
        if email and os.path.exists(filename):            
            file_path = os.path.dirname(filename)
            file_name = os.path.basename(filename)
            file_stage_status = const.FILE_STATUS_NEW
            file_size, modified_date = FileStage.get_resource_attributes(filename)            
            file_modified_date = datetime.datetime.fromtimestamp(modified_date)
            
            # insert file stage record            
            args = (email, file_name, file_path, file_size, file_modified_date, file_stage_status, None)
            _, params = db.execute(const.SP_INSERT_FILE_STAGE, *args)
            # unpack params for file_stage_id
            *_, file_stage_id = params
            
            # insert bulk query record from csv
            if file_stage_id:
                try:                   
                    with open(filename) as f:
                        csv_reader = csv.reader(f, delimiter=",")
                        line_count = 0
                        for line in csv_reader:
                            line_count += 1
                            if line_count == 1:
                                continue
                            if line:
                                row_obj = FileStage.Row(*line, file_stage_id)
                                args = row_obj.values()
                                
                                _ , params = db.execute(const.SP_INSERT_FILE_QUERY, *args, None)

                except Exception as err:
                    logger.error(f"Unable to load file {filename}", err)
                    raise

    @staticmethod
    def get_resource_attributes(filename):
        if filename and os.path.exists(filename):
            stats = os.stat(filename)
            return stats.st_size, stats.st_mtime
