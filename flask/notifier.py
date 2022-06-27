"""
Copyright: Copyright (C) 2022 2DEVIATE Inc. - All Rights Reserved
Product: Standard
Description: Notifier Script to query exchange data and send notifications (email)
Notifyees: craig@2deviate.com
Category: None

"""
import re
import logging
import os
import json
import pandas
import urllib3
import time
import argparse
import tempfile
from run import create_app
from app.db import db
from config import configs
import app.constants as const

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


logger = logging.getLogger(__name__)
dir_path = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(
    filename="/".join([dir_path, "notifier.log"]),
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s",
    force=True,
)

# script globals
docker_db_name = None
docker_server_name = None
docker_proxy_name = None

email_from_address = None
email_cc_address = None
email_attachment = None
email_subject = None
smtp_user = None
smtp_password = None
smtp_host = None
smtp_port = None
email_template_schema = None

def get_data(method, url=None, headers=None, body=None, **attrs):
    result = None
    try:
        http = urllib3.PoolManager()
        if method == "POST":
            payload = payload
            encoded = urllib3.request.urlencode(payload)
            body = encoded.encode("ascii")
            request = http.request(method=method, url=url, body=body, headers=headers)
        elif method == "GET":
            request = http.request(method=method, url=url, headers=headers)
        return request.data
    except Exception as err:
        logger.error(err, exc_info=err)
    return result


def send_mail(from_addr, to_addrs, cc_addrs, df):

    text = "Pangea bulk query results"
    html = df.to_html(index=False)

    text_part = MIMEText(text, 'plain')
    html_part = MIMEText(html, 'html')

    msg_alternative = MIMEMultipart('alternative')
    msg_alternative.attach(text_part)
    msg_alternative.attach(html_part)

    tmp = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    logger.error(f"created tmpfile {tmp.name=}")
    
    df.to_csv(tmp, index=False)
    
    fp=open(tmp.name,'rb')
    attachment = MIMEApplication(fp.read(),_subtype="csv")
    fp.close()

    attachment.add_header('Content-Disposition', 'attachment', filename=tmp.name)

    msg_mixed = MIMEMultipart('mixed')
    msg_mixed.attach(msg_alternative)
    msg_mixed.attach(attachment)
    
    msg_mixed['From'] = from_addr
    msg_mixed['To'] = "".join(to_addrs) if isinstance(to_addrs, list) else to_addrs
    msg_mixed['CC'] = ",".join(cc_addrs) if isinstance(cc_addrs, list) else cc_addrs
    msg_mixed['Subject'] = email_subject

    try:
        smtp_obj = smtplib.SMTP_SSL(host=smtp_host, port=smtp_port)
        smtp_obj.ehlo()
        smtp_obj.login(smtp_user, smtp_password)
        smtp_obj.sendmail(from_addr, to_addrs, msg_mixed.as_string())
        smtp_obj.quit()
    except Exception as err:
        logger.error(err, exc_info=err)
        raise err


def normalize_query(query: str) -> str:
    return re.sub("\s\s+", " ", query).strip()


def execute_query(query):
    query = normalize_query(query)
    logger.info(f"Executing query {query}")
    try:
        return db.execute(query)
    except Exception as err:
        logger.error(f"Error executing {query}", err)
        raise err


def set_status(*args):
    proc = const.SP_UPDATE_FILE_STAGE_STATUS
    try:
        db.execute(proc, *args)
        logger.info(f"executed {proc=}, args {args=}")
    except Exception as err:
        logger.error(f"Error executing {proc=}, {args=}", err)
        raise err


def parse_data(data_obj):
    try:
        data = json.loads(data_obj)
        data = data.get("response", data)
        if data and isinstance(data, dict):
            return data
        return None
    except Exception as err:
        logger.error(f"Error parsing data {data_obj=}", err)
        raise err


def process_query(query, dry_run):    
    (
        file_query_id,
        _,
        exchange_name,
        exchange_code,
        exchange_post_code,
        avg_data_usage,
        stop_sell_date,
        file_stage_fk,
        exchange_product_fk,
        _,
    ) = query
    
    if not dry_run:
        args = (file_stage_fk, const.FILE_STATUS_PROCESS)
        set_status(*args)

    url = f"http://{docker_server_name}:8000/api/v1.0/pangea/recommendation/product/usage?limit={avg_data_usage}"
    data_obj = get_data(method="GET", url=url)
    data = parse_data(data_obj)
    if data:
        exchange_product_fk = data.get("product_id", None)

    criterion = (exchange_code if exchange_code else exchange_post_code)
    url = f"http://{docker_server_name}:8000/api/v1.0/pangea/decommission/exchange/search?query={criterion}"
    data_obj = get_data(method="GET", url=url)
    data = parse_data(data_obj)
    if data:
        exchange_name = data.get("exchange_name", None)
        exchange_code = data.get("exchange_code", None)        
        exchange_post_code = data.get("exchange_postcode", None)
        stop_sell_date = data.get("implementation_date", None)

    args = (file_query_id, exchange_name, exchange_code, exchange_post_code, avg_data_usage, stop_sell_date, exchange_product_fk)
    proc = const.SP_UPDATE_FILE_QUERY
    
    try:        
        affected, _ = db.execute(proc, *args)
        logger.info(f"Executed {proc=}, {args=}, {affected=}")
    except Exception as err:
        logger.error(f"Error updating, {proc=}, {args=}", err)
        raise err


def process_upload(upload, dry_run):
    file_stage_id, *_ = upload

    if not dry_run:
        args = (file_stage_id, const.FILE_STATUS_UPLOAD)
        set_status(*args)

    proc = const.SP_GET_FILE_QUERY_BY_FILE_STAGE_ID
    if not dry_run:
        try:
            queries, _ = db.execute(proc, file_stage_id)
            logger.info(
                f"fetched builk queries, proc={proc}, {file_stage_id=}, {dry_run=}"
            )
        except Exception as err:
            logger.error(f"Error uploading, proc={proc}, raising err", err)
            if not queries and not dry_run:
                args = (file_stage_id, const.FILE_STATUS_EXCEPTION)
                set_status(*args)
            raise err

    for query in queries:
        logger.info(f"processing {query=}")
        process_query(query, dry_run)

    if not dry_run:
        args = (file_stage_id, const.FILE_STATUS_NOTIFY)
        set_status(*args)

        return True


def process_uploads(dry_run):
    try:
        if not dry_run:
            proc, args = const.SP_GET_UPLOADED_FILES, const.FILE_STATUS_NEW
            uploads, _ = db.execute(proc, args)
            for upload in uploads:
                process_upload(upload, dry_run)
        logger.info(f"fetched uploads, {dry_run=}")
    except Exception as err:
        logger.error(f"Error processing uploads, raising err", err)
        raise err


def process_notification(notification, dry_run):
    file_stage_id, email_address, *_ = notification
    try:
        proc, args = const.SP_GET_RECOMMENDATIONS, file_stage_id
        recommedations, _ = db.execute(proc, args)
        logger.info(f"executed {proc=}, {args=}, {recommedations=}, {dry_run=}")
    except Exception as err:
        logger.info(f"Error executing  {proc=}, {args=}, {dry_run=}")        
        raise err
    try:        
        cc = email_cc_address
        from_addr = email_from_address
        to_addrs = email_address
        df_cols = email_template_schema.values()
        df = pandas.DataFrame(recommedations, columns=df_cols)
        logger.info(f"sending mail {from_addr=}, {to_addrs=}, {cc=}")
        args = (file_stage_id, const.FILE_STATUS_COMPLETE)
        if not dry_run:                
            send_mail(from_addr, to_addrs, cc, df=df)
            set_status(*args)
        logger.info(f"sent mail {args=}, {df=}")
        return True
    except Exception as err1:
        if not dry_run:
            args = (file_stage_id, const.FILE_STATUS_EXCEPTION)
            set_status(*args)
            logger.warning(f"Error sending mail, {args=}")
            raise err1

def process_notifications(dry_run):
    try:
        if not dry_run:            
            proc, args = const.SP_GET_UPLOADED_FILES, const.FILE_STATUS_NOTIFY
            notifications, _ = db.execute(proc, args)
            for notification in notifications:
                process_notification(notification, dry_run)
        logger.info(f"fetched notifications, {dry_run=}")
    except Exception as err:
        logger.error(f"Error processing notification, raising err", err)
        raise err


def _main(**kwargs):
    dry_run = kwargs.get("dry_run", None)
    try:
        process_uploads(dry_run)
        process_notifications(dry_run)
    except Exception as ex:
        logger.error(ex)
        return 1
    return 0


if __name__ == "__main__":
    """Script args for querying templates and notifications"""
    start = time.time()
    logger.info(f"__main__ call")
    logger.info(f"Started clock {start=}")
    # setup environment, get flask config
    env = os.environ.get("FLASK_ENV", "default")
    config = configs[env]
    # setup app for config keys
    app = create_app(config=config)
    # setup mysql server
    docker_db_name = app.config['DOCKER_DB_NAME']
    docker_server_name = app.config['DOCKER_SERVER_NAME']
    docker_proxy_name = app.config['DOCKER_PROXY_NAME']    
    # setup smtp and email
    email_from_address = app.config['EMAIL_FROM_ADDRESS']
    email_cc_address = app.config['EMAIL_CC_ADDRESSES']
    email_attachment = app.config['EMAIL_ATTACHMENT']
    email_subject = app.config['EMAIL_SUBJECT']
    smtp_user = app.config['SMTP_USER']    
    smtp_password = app.config['SMTP_PASSWORD']
    smtp_host = app.config['SMTP_HOST']
    smtp_port = app.config['SMTP_PORT']
    email_template_schema = app.config['EMAIL_TEMPLATE_SCHEMA']
    # parse args, invoke main
    p = argparse.ArgumentParser(description="Process command line parameters")
    p.add_argument(
        "--dry-run",
        action=argparse.BooleanOptionalAction,
        help="dry run flag, if set to True no writes",
    )
    args = p.parse_args()
    status = _main(**vars(args))
    # capture wall time and status
    end = time.time()
    elapsed = end - start
    logger.info(f"Completed, {elapsed=}, {status=}")
