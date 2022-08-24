"""
Copyright: Copyright (C) 2022 2DEVIATE Inc. - All Rights Reserved
Product: Standard
Description: Models for the Api app
Notifyees: craig@2deviate.com
Category: None
"""

# local imports
import re
import os
import csv
import uuid
import logging
import subprocess
import phonenumbers
import datetime
import app.constants as const
from app.sam import sam
from app.map import maps
from app.db import db
from app.redis import store
from ukpostcodeutils import validation
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)

def cache_key(path, *args, **kwargs):
    key = str(tuple([path] + ['?'] + [str(v) for v in sorted(args)] + [(k, kwargs[k]) for k in sorted(kwargs.keys())]))
    return key

def cached(func):
    def wrapper(*args, **kwargs):
        path = func.__qualname__
        key = cache_key(path, *args, **kwargs)
        if store.get(key):
            return store.get(key)
        result = func(*args, **kwargs)
        store.set(key, result)
        return result
    return wrapper


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

    @cached
    @staticmethod
    def find_by_query(query):
        url = "https://availability.samknows.com/broadband/exchange_search"
        return sam.request(method="POST", query=query, url=url, scraper=sam.scrape_info)

    @cached
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
        try:
            # try and parse into telephone number
            number = phonenumbers.parse(telephone, "GB")
            return isinstance(number, phonenumbers.PhoneNumber)                
        except phonenumbers.NumberParseException as ex:
            logger.error("Invalid telephone", ex)
            return False


class Product(object):
    """
    This class represents an simple Product object
    """

    def __init__(self, **kwargs):
        self.limit = kwargs.get("limit", None)

    def __repr__(self):
        return "<limit: {}>".format(self.limit)

    @cached
    @staticmethod    
    def find_by_limit(limit):
        return  db.execute(const.SP_GET_EXCHANGE_PRODUCT_BY_LIMIT, limit)        


class Pricing(object):
    """
    This class represents an Pricing object
    """

    def __init__(self, **kwargs):
        self.limit = kwargs.get("limit", None)
        self.exchange_query_id = kwargs.get("exchange_query_id", None)

    def __repr__(self):
        return "<limit: {}>".format(self.data_usage)

    @cached
    @staticmethod
    def find_by_limit(limit):
        return db.execute(const.SP_GET_EXCHANGE_PRODUCT_PRICING_BY_LIMIT, limit)

    @staticmethod
    def set_by_limit(limit, store_id):
        result_key = cache_key("Pricing.find_by_limit", limit)   # TODO: derive instead of magic string
        if store_id:            
            return db.execute(const.SP_SET_EXCHANGE_PRODUCT_PRICING_BY_LIMIT, store_id, result_key)

    @staticmethod
    def get_recommendations(file_upload_id):
        return db.execute(const.SP_GET_EXCHANGE_QUERY_RESULTS, file_upload_id)


class Location(object):
    """
    This class represents an simple geolocation object
    """

    def __init__(self, **kwargs):
        self.postcode = kwargs.get("postcode", None)

    def __repr__(self):
        return "<postcode: {}>".format(self.postcode)

    @cached
    @staticmethod
    def find_by_postcode(postcode):
        return maps.request(postcode)


class FileResource(object):
    """
    This class represents a file resource object
    """

    @staticmethod
    def template(config):
        download = config["FLASK_APP_DOWNLOAD_FOLDER"]
        template = config["FLASK_APP_TEMPLATE_NAME"]
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
            self.args = args
            try:
                #CLI,POST_CODE,EXCHANGE_CODE,DATA_USAGE
                self.cli = self.args[0] if self.args[0] else None
                self.site_postcode = self.args[1] if self.args[1] else None
                self.exchange_code = self.args[2] if self.args[2] else None
                self.avg_data_usage = self.args[3] if self.args[3] else None                                
                self.file_upload_fk = self.args[4] if self.args[4] else None
                self.exchange_query_status_fk = self.args[5] if self.args[5] else None
                # implemented place holder fields
            except Exception as err:
                logger.error(f"Row init exception,", err)
                raise

        def values(self):
            cli = str(self.cli) if self.cli else None                        
            site_postcode = str(self.site_postcode) if self.site_postcode else None
            exchange_code = str(self.exchange_code) if self.exchange_code else None            
            
            avg_data_usage = 0.0
            if self.avg_data_usage:
                try:
                    avg_data_usage = float(self.avg_data_usage)
                except ValueError as err:
                    logger.warning(f"Unable to parse avg_data_usage as float, {self.args=}", err)                    
                    pass            
            
            file_upload_fk = self.file_upload_fk
            exchange_query_status_fk = self.exchange_query_status_fk
            
            return (cli, site_postcode, None, exchange_code, None, avg_data_usage, None, file_upload_fk, exchange_query_status_fk)

    @staticmethod
    def find_by_status(status):        
        return db.execute(const.SP_GET_FILE_UPLOAD_BY_STATUS, status)                

    @staticmethod
    def insert(email, filename):
        logger.info(f"Processing file for insert into db, {email=}, {filename=}")
        
        if email and FileStage.validate_email(email) and os.path.exists(filename):            
            file_path = os.path.dirname(filename)
            file_name = os.path.basename(filename)
            file_upload_status = const.FILE_STATUS_NEW
            file_size, modified_date = FileStage.get_resource_attributes(filename)            
            file_modified_date = datetime.datetime.fromtimestamp(modified_date)
            
            # insert file stage record            
            proc = const.SP_INSERT_FILE_UPLOAD
            args = (email, file_name, file_path, file_size, file_modified_date, file_upload_status, None)
            logger.info(f"Insert call, {proc=}, {args=}")
            _, params = db.execute(proc, *args)
            # unpack params for file_upload_id
            *_, file_upload_id = params
            
            # insert bulk query record from csv
            if file_upload_id:
                try:
                    proc = const.SP_INSERT_EXCHANGE_QUERY
                    logger.info(f"Open file, {filename=}")
                    with open(filename) as f:
                        csv_reader = csv.reader(f, delimiter=",")
                        line_count = 0
                        for line in csv_reader:
                            line_count += 1
                            if line_count == 1:
                                continue
                            if line:
                                logger.info(f"Inserting Row, {line=}")
                                row_obj = FileStage.Row(*line, file_upload_id, const.EXCHANGE_QUERY_STATUS_WAIT)
                                
                                args = row_obj.values()
                                
                                logger.info(f"Insert call, {proc=}, {args=}")
                                _ , params = db.execute(proc, *args, None)

                except Exception as err:
                    logger.error(f"Unable to import file into db {filename=}", err)
                    proc = const.SP_UPDATE_FILE_UPLOAD_STATUS
                    args = file_upload_id, const.FILE_STATUS_EXCEPTION
                    logger.info(f"Updating status, {proc=}, {args=}")
                    db.execute(proc, *args)
                    raise
                finally:                    
                    # completed importing, remove temp file
                    try:
                        os.remove(filename)
                    except Exception as err:
                        logger.error(f"Unable to delete temp file {filename=}", err)
                        proc = const.SP_UPDATE_FILE_UPLOAD_STATUS
                        args = file_upload_id, const.FILE_STATUS_EXCEPTION
                        logger.info(f"Updating status, {proc=}, {args=}")
                        db.execute(proc, *args)
                        raise
            return params

    @staticmethod
    def get_resource_attributes(filename):
        if filename and os.path.exists(filename):
            stats = os.stat(filename)
            return stats.st_size, stats.st_mtime

    @staticmethod
    def validate_email(email):
        regexp = re.compile(r'[^@]+@[^@]+\.[^@]+')        
        try:            
            return True if regexp.match(email) else False
        except Exception as ex:
            logger.error(f"Invalid email, {email=}", ex)
            raise


class ScriptExecute(object):
    """
    This class represents an simple script class
    """
    @staticmethod
    def execute(script):
        #sudo -E su root -c 'sh /home/app/notifier.sh'
        exec_cmd = ["sudo", "-E", "su", "root", "-c", f"'sh {script}'"]
        logger.info(f"Invoking script, {script=}, as exec_cmd={' '.join(exec_cmd)}")
        return subprocess.run(exec_cmd, capture_output=True)

