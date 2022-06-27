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
NO_DATA_RESULTS_FOUND = "No Data Found"
FILE_IO_ERROR = "File IO Error"
FILE_SAVE_SUCCESSFUL = "File Save Successful"
FILE_UPLOAD_SUCCESSFUL = "File Upload Successful"
FILE_UPLOAD_UNSUCCESSFUL = "File Upload Successful"

# ------------ Database Constants -----------------
FILE_STATUS_NEW = "New"
FILE_STATUS_UPLOAD = "Upload"
FILE_STATUS_PROCESS = "Process"
FILE_STATUS_NOTIFY = "Notify"
FILE_STATUS_COMPLETE = "Complete"
FILE_STATUS_EXCEPTION = "Exception"

PRODUCT_STATUS_AVAILABLE = "Available"
PRODUCT_STATUS_UNAVAILABLE = "Unavailable"

# ------------ Stored Procedures -------------------

SP_GET_EXCHANGE_PRODUCT_DEFAULT_ID = "sp_get_exchange_product_default_id"
SP_UPDATE_FILE_STAGE_STATUS = "sp_update_file_stage_status"
SP_UPDATE_FILE_QUERY = "sp_update_file_query"
SP_GET_FILE_QUERY_BY_FILE_STAGE_ID = "sp_get_file_query_by_file_stage_id"
SP_INSERT_EXCHANGE_DECOM = "sp_insert_exchange_decom"
SP_GET_EXCHANGE_DECOM_COUNT = "sp_get_exchange_decom_count"
SP_TRUNCATE_EXCHANGE_DECOM = "sp_truncate_exchange_decom"
SP_GET_EXCHANGE_DECOM_BY_EXCHANGE_ID = "sp_get_exchange_decom_by_exchange_id"
SP_GET_FILE_STAGE_BY_STATUS = "sp_get_file_stage_by_status"
SP_GET_EXCHANGE_DECOM_BY_LIMIT = "sp_get_exchange_decom_by_limit"
SP_GET_EXCHANGE_DECOM_BY_SITE = "sp_get_exchange_decom_by_site"
SP_GET_EXCHANGE_DECOM_BY_EXCHANGE_NAME = "sp_get_exchange_decom_by_exchange_name"
SP_GET_EXCHANGE_DECOM_BY_EXCHANGE_CODE = "sp_get_exchange_decom_by_exchange_code"
SP_GET_EXCHANGE_DECOM_BY_EXCHANGE_LOCATION = "sp_get_exchange_decom_by_exchange_location"
SP_EXCHANGE_PRODUCT_FIND_BY_LIMIT = "sp_exchange_product_find_by_limit"
SP_INSERT_FILE_STAGE = "sp_insert_file_stage"
SP_INSERT_FILE_QUERY = "sp_insert_file_query"

SP_GET_UPLOADED_FILES = "sp_get_uploaded_files"
SP_GET_RECOMMENDATIONS = "sp_get_recommendations"

# ------------ Email Templates -------------------

EMAIL_ATTACHMENT = "StopSellInfo.csv"
EMAIL_SUBJECT = "Pangea Exchange Stop Sell Information"
EMAIL_TEMPLATE_SCHEMA = {
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





