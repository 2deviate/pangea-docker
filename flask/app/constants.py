"""
Copyright: Copyright (C) 2022 2DEVIATE Inc. - All Rights Reserved
Product: Standard
Description: Constants
Notifyees: craig@2deviate.com
Category: None
"""
# ------------ General Constants -----------------
NODE_ALREADY_EXISTS = "Already Exists"
NODE_DOES_NOT_EXISTS = "Does Not Exists"
DATA_OPERATION_SUCCESSFUL = "Data Operation Successful"
DATA_OPERATION_UNSUCCESSFUL = "Data Operation Unsuccessful"
QUERY_MISSING_PARAMS = "Params Missing"
INVALID_DATA = "Invalid Data"
NO_DATA_RESULTS_FOUND = "No Data"
NOT_PROVIDED = "Not Provided"
NO_STOP_SELL_INFORMATION = "2023-09-01"
FILE_IO_ERROR = "File IO Error"
FILE_SAVE_SUCCESSFUL = "File Save Successful"
FILE_UPLOAD_SUCCESSFUL = "File Upload Successful"
FILE_UPLOAD_UNSUCCESSFUL = "File Upload Successful"

# ------------ Database Constants -----------------
FILE_STATUS_NEW = 1                     # New
FILE_STATUS_UPLOAD = 2                  # Upload
FILE_STATUS_PROCESS = 3                 # Process
FILE_STATUS_NOTIFY = 4                  # Notify
FILE_STATUS_SENT = 5                    # Sent
FILE_STATUS_COMPLETE = 6                # Complete
FILE_STATUS_EXCEPTION = 7               # Exception

EXCHANGE_QUERY_STATUS_WAIT = 1          # Wait
EXCHANGE_QUERY_STATUS_BUSY = 2          # Busy
EXCHANGE_QUERY_STATUS_DONE = 3          # Done
EXCHANGE_QUERY_STATUS_EXCEPTION = 4     # Exception

PRODUCT_STATUS_AVAILABLE = 1            # Available
PRODUCT_STATUS_UNAVAILABLE = 2          # Unavailable

# ------------ Stored Procedures -------------------

SP_INSERT_FILE_UPLOAD = "sp_insert_file_upload"
SP_UPDATE_FILE_UPLOAD_STATUS = "sp_update_file_upload_status"
SP_GET_FILE_UPLOAD_BY_STATUS = "sp_get_file_upload_by_status"

SP_INSERT_EXCHANGE_QUERY = "sp_insert_exchange_query"
SP_UPDATE_EXCHANGE_QUERY = "sp_update_exchange_query"
SP_UPDATE_EXCHANGE_QUERY_STATUS = "sp_update_exchange_query_status"
SP_GET_EXCHANGE_QUERY_BY_FILE_UPLOAD_ID = "sp_get_exchange_query_by_file_upload_id"

SP_GET_EXCHANGE_PRODUCT_DEFAULT_ID = "sp_get_exchange_product_default_id"

SP_INSERT_EXCHANGE_DECOM = "sp_insert_exchange_decom"
SP_TRUNCATE_EXCHANGE_DECOM = "sp_truncate_exchange_decom"
SP_GET_EXCHANGE_DECOM_COUNT = "sp_get_exchange_decom_count"

SP_GET_EXCHANGE_DECOM_BY_EXCHANGE_ID = "sp_get_exchange_decom_by_exchange_id"

SP_GET_EXCHANGE_DECOM_BY_SITE = "sp_get_exchange_decom_by_site"
SP_GET_EXCHANGE_DECOM_BY_LIMIT = "sp_get_exchange_decom_by_limit"
SP_GET_EXCHANGE_DECOM_BY_EXCHANGE_NAME = "sp_get_exchange_decom_by_exchange_name"
SP_GET_EXCHANGE_DECOM_BY_EXCHANGE_CODE = "sp_get_exchange_decom_by_exchange_code"
SP_GET_EXCHANGE_DECOM_BY_EXCHANGE_LOCATION = "sp_get_exchange_decom_by_exchange_location"

SP_GET_EXCHANGE_PRODUCT_BY_LIMIT = "sp_get_exchange_product_by_limit"
SP_GET_EXCHANGE_PRODUCT_PRICING_BY_LIMIT = "sp_get_exchange_product_pricing_by_limit"
SP_SET_EXCHANGE_PRODUCT_PRICING_BY_LIMIT = "sp_set_exchange_product_pricing_by_limit"

SP_GET_UPLOADED_FILES = "sp_get_uploaded_files"

SP_GET_EXCHANGE_QUERY_RESULTS = "sp_get_exchange_query_results"

SP_EXECUTE_SQL = "sp_execute_sql"

# ------------ Email Templates -------------------

EMAIL_ATTACHMENT = "Pangea Sales Planner.xlsx"
EMAIL_SUBJECT = "Pangea Exchange Stop Sell Information"

EMAIL_TEMPLATE_SCHEMA = {
    "cli": "CLI",
    "exchange_name": "Exchange Name",
    "avg_data_usage": "Average Data Usage (GB)",
    "file_email_address": "Email Address",
    "exchange_code": "Exchange Code",
    'redis_cache_result_key': "Cached Key",
    "stop_sell_date": "Exchange Stop Sell Date",    
    "exchange_query_status_id": "Exchange Query Status Id",
    "site_postcode": "Site Post Code",
    "file_upload_id": "File Upload Id",
    "exchange_query_id": "Exchange Query Id",
    "exchange_postcode": "Exchange Post Code",    
    "product_category": "Category",
    "product_limit": "Inclusive Data (GB)",
    "product_price": "Price (GBP)",
    "product_class": "Class",
    "product_name": "Product Name",
    "product_unit": "Product Unit",    
    "product_term": "Term",
}
