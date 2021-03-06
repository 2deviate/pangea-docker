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
import asyncio
from run import create_app
from app.db import db
from config import configs
import app.constants as const
from dateutil import parser
from functools import reduce

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email_validator import validate_email, EmailNotValidError

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
docker_server_port = None
docker_proxy_name = None

email_from_address = None
email_cc_address = None
email_bcc_address = None
email_attachment = None
email_subject = None

smtp_user = None
smtp_password = None
smtp_host = None
smtp_port = None

email_template_text = None
email_template_html = None
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


def send_mail(from_addr, to_addrs, cc_addrs, bcc_addrs, df):

    logger.info(f"sending mail, {from_addr=}, {to_addrs=}, {cc_addrs=}, {bcc_addrs=}")

    text = email_template_text if email_template_text else ""
    html = email_template_html if email_template_html else df.to_html(index=False)

    text_part = MIMEText(text, "plain")
    html_part = MIMEText(html, "html")

    msg_alternative = MIMEMultipart("alternative")
    msg_alternative.attach(text_part)
    msg_alternative.attach(html_part)

    msg_mixed = MIMEMultipart("mixed")
    msg_mixed.attach(msg_alternative)

    if not df.empty:
        with tempfile.NamedTemporaryFile(suffix=".csv") as tmp:            
            logger.info(f"created tmp file {tmp.name=}")                
            df.to_csv(tmp, index=False)
            fp = open(tmp.name, "rb")
            attachment = MIMEApplication(fp.read(), _subtype="csv")
            fp.close()
            attachment.add_header("Content-Disposition", "attachment", filename=email_attachment)    
            msg_mixed.attach(attachment)

    to_addrs = [addrs for addrs in set(to_addrs) if validate_addrs(addrs) is not None]
    cc_addrs = [addrs for addrs in set(cc_addrs) if validate_addrs(addrs) is not None]
    bcc_addrs = [addrs for addrs in set(bcc_addrs) if validate_addrs(addrs) is not None]
    
    msg_mixed["From"] = from_addr
    msg_mixed["To"] = ",".join(to_addrs)
    msg_mixed["Cc"] = ",".join(cc_addrs)
    msg_mixed["Bcc"] = ",".join(bcc_addrs)
    msg_mixed["Subject"] = email_subject    

    try:
        logger.info(f"login to smpt sever {smtp_host=}, {smtp_port=}") 
        smtp_obj = smtplib.SMTP_SSL(host=smtp_host, port=smtp_port)
        smtp_obj.ehlo()
        smtp_obj.login(smtp_user, smtp_password)
        logger.debug(f"send mail {from_addr=}, {to_addrs=}, envelope={msg_mixed.as_string()}") 
        smtp_obj.sendmail(from_addr, (to_addrs+cc_addrs+bcc_addrs), msg_mixed.as_string())
        smtp_obj.quit()
    except Exception as err:
        logger.error(f"Error sending mail", err)        
        raise

def validate_addrs(email):
    if email is None or not isinstance(email, str) or len(email) == 0:
        logger.warning(f"Invalid email address, removing {email=}")
        return None
    try:        
        email = validate_email(email).email
    except EmailNotValidError as err:        
        logger.error(f"Error parsing email address, {email=}", err)
        return None
    return email

def normalize_query(query: str) -> str:
    return re.sub("\s\s+", " ", query).strip()

def execute_query(query):
    query = normalize_query(query)
    logger.info(f"Executing query {query}")
    try:
        return db.execute(query)
    except Exception as err:
        logger.error(f"Error executing {query}", err)
        raise


def set_status(*args):
    proc = const.SP_UPDATE_FILE_STAGE_STATUS
    try:
        db.execute(proc, *args)
        logger.info(f"executed {proc=}, args {args=}")
    except Exception as err:
        logger.error(f"Error executing {proc=}, {args=}", err)
        raise


def parse_data(data_obj):
    try:
        data = json.loads(data_obj)
        data = data.get("response", data)
        if data and isinstance(data, dict):
            return data
        return None
    except Exception as err:
        logger.error(f"Error parsing data {data_obj=}", err)
        raise


async def request_data(url, **kwargs):
    data_obj = get_data(method="GET", url=url)
    data = parse_data(data_obj)
    if data:
        return kwargs | data
    return kwargs


async def process_query(query, dry_run):
    schema = [
        'file_query_id',
        'cli',
        'site_postcode',
        'exchange_name',
        'exchange_code',
        'exchange_postcode',
        'avg_data_usage',
        'implementation_date',
        'file_stage_fk',
        'exchange_product_fk'        
    ]
    query = { k:query[i] for i, k in enumerate(schema) }

    cli = query['cli']
    site_postcode = query['site_postcode']
    exchange_code = query['exchange_code']
    avg_data_usage = query['avg_data_usage']
    file_stage_fk = query['file_stage_fk']
    
    if not dry_run:
        args = (file_stage_fk, const.FILE_STATUS_PROCESS)
        set_status(*args)

    url = f"http://{docker_server_name}:{docker_server_port}/api/v1.0/pangea/recommendation/product/usage?limit={avg_data_usage}"
    #data = await request_data(url, **query)
    t1 = request_data(url, **query)
    
    criterion = cli if cli else site_postcode if site_postcode else exchange_code
    url = f"http://{docker_server_name}:{docker_server_port}/api/v1.0/pangea/sam/exchange/info?query={criterion}"
    #data = await request_data(url, **data)
    t2 = request_data(url, **query)

    # prop and await results
    results = await asyncio.gather(t1, t2)
    
    # combine dicts using reduce on merge lambda
    data = reduce(lambda x, y: x | y, results, {})
                
    exchange_code = data['exchange_code']
    if exchange_code:
        url = f"http://{docker_server_name}:{docker_server_port}/api/v1.0/pangea/decommission/exchange/search?query={exchange_code}"
        data = await request_data(url, **data)

        implementation_date = data['implementation_date']
        
        if implementation_date is None:
            url = f"http://{docker_server_name}:{docker_server_port}/api/v1.0/pangea/sam/exchange/info?exchange_code={exchange_code}"
            data = await request_data(url, **data)
    
    implementation_date = data.get('implementation_date')

    if implementation_date:
        try:
            data['stop_sell_date'] = parser.parse(implementation_date).date().strftime("""%Y-%m-%d""")
        except parser.ParserError as err:
            logger.error(f"Unable to parse, {implementation_date=}", err)            
            pass
    
    data = { k:v for k,v in data.items() if v is not None}

    args = (
        data.get('file_query_id'),
        data.get('cli', const.NOT_PROVIDED),
        data.get('site_postcode', const.NOT_PROVIDED),
        data.get('exchange_name', const.NO_DATA_RESULTS_FOUND),
        data.get('exchange_code', const.NO_DATA_RESULTS_FOUND),
        data.get('exchange_postcode', const.NO_DATA_RESULTS_FOUND),
        data.get('avg_data_usage'),
        data.get('stop_sell_date', const.NO_STOP_SELL_INFORMATION),
        data.get('product_id')
    )
    proc = const.SP_UPDATE_FILE_QUERY

    try:
        affected, _ = db.execute(proc, *args)
        logger.info(f"Executed {proc=}, {args=}, {affected=}")
    except Exception as err:
        logger.error(f"Error updating, {proc=}, {args=}", err)
        raise


async def process_upload(upload, dry_run):
    file_stage_id, *_ = upload

    if not dry_run:
        args = (file_stage_id, const.FILE_STATUS_UPLOAD)
        set_status(*args)

    proc = const.SP_GET_FILE_QUERY_BY_FILE_STAGE_ID
    if not dry_run:
        try:
            queries, _ = db.execute(proc, file_stage_id)
            logger.info(
                f"fetched builk queries, {proc=}, {file_stage_id=}, {dry_run=}"
            )
        except Exception as err:
            logger.error(f"Error uploading, {proc=}, raising err", err)
            if not queries and not dry_run:
                args = (file_stage_id, const.FILE_STATUS_EXCEPTION)
                set_status(*args)
            raise

    for query in queries:
        logger.info(f"processing {query=}")
        try:
            await process_query(query, dry_run)
        except Exception as err:
            logger.error(f"Error processing upload query, {query=}", err)

    if not dry_run:
        args = (file_stage_id, const.FILE_STATUS_NOTIFY)
        set_status(*args)
        return True


async def process_uploads(dry_run):
    try:
        if not dry_run:
            proc, args = const.SP_GET_UPLOADED_FILES, const.FILE_STATUS_NEW
            uploads, _ = db.execute(proc, args)
            for upload in uploads:
                await process_upload(upload, dry_run)
        logger.info(f"fetched uploads, {dry_run=}")
    except Exception as err:
        logger.error(f"Error processing uploads, raising err", err)
        raise


def process_notification(notification, dry_run):
    file_stage_id, email_to_address, *_ = notification
    try:
        proc, args = const.SP_GET_RECOMMENDATIONS, file_stage_id
        recommedations, _ = db.execute(proc, args)
        logger.info(f"executed {proc=}, {args=}, {recommedations=}, {dry_run=}")
    except Exception as err:
        logger.info(f"Error executing  {proc=}, {args=}, {dry_run=}")
        raise
    try:
        df = pandas.DataFrame()        
        from_addr = email_from_address
        to_addrs = email_to_address.split(',')
        cc = email_cc_address.split(',')
        bcc = email_bcc_address.split(',')
        try:
            df_cols = email_template_schema.values()
            df = pandas.DataFrame(recommedations, columns=df_cols)
        except Exception as err2:
            logger.error(f"Cannot form attachment, ignoring, {args=}", err2)
            pass            
        logger.info(f"sending mail {from_addr=}, {to_addrs=}, {cc=}, {bcc=}")
        args = (file_stage_id, const.FILE_STATUS_COMPLETE)
        if not dry_run:
            send_mail(from_addr, to_addrs, cc, bcc, df=df)
            set_status(*args)
        logger.info(f"sent mail {args=}, {df=}")
        if not dry_run:
            args = (file_stage_id, const.FILE_STATUS_SENT)
            set_status(*args)
        logger.info(f"updated status, {args=}")
        return True
    except Exception as err1:
        if not dry_run:
            args = (file_stage_id, const.FILE_STATUS_EXCEPTION)
            set_status(*args)
        logger.error(f"Error sending mail, {notification=}, {email_to_address=}", err1)
        raise


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
        raise


async def _main(**kwargs):
    dry_run = kwargs.get("dry_run", None)
    try:
        await process_uploads(dry_run)
        process_notifications(dry_run)
    except Exception as ex:
        logger.error(f"Error processing uploads and notifications, {kwargs=}", ex)
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
    docker_db_name = app.config["DOCKER_DB_NAME"]
    docker_server_name = app.config["DOCKER_SERVER_NAME"]
    docker_server_port = app.config["DOCKER_SERVER_PORT"]    
    docker_proxy_name = app.config["DOCKER_PROXY_NAME"]
    # setup smtp and email
    email_from_address = app.config["EMAIL_FROM_ADDRESS"]
    email_cc_address = app.config["EMAIL_CC_ADDRESSES"]
    email_bcc_address = app.config["EMAIL_BCC_ADDRESSES"]
    email_attachment = app.config["EMAIL_ATTACHMENT"]
    email_subject = app.config["EMAIL_SUBJECT"]
    smtp_user = app.config["SMTP_USER"]
    smtp_password = app.config["SMTP_PASSWORD"]
    smtp_host = app.config["SMTP_HOST"]
    smtp_port = app.config["SMTP_PORT"]
    # setup email template content
    email_template_text = app.config["EMAIL_TEMPLATE_TEXT"]
    email_template_html = app.config["EMAIL_TEMPLATE_HTML"]
    email_template_schema = app.config["EMAIL_TEMPLATE_SCHEMA"]
    # parse args, invoke main
    p = argparse.ArgumentParser(description="Process command line parameters")
    p.add_argument(
        "--dry-run",
        action=argparse.BooleanOptionalAction,
        help="dry run flag, if set to True no writes",
    )
    args = p.parse_args()
    status = asyncio.run(_main(**vars(args)))
    # capture wall time and status
    end = time.time()
    elapsed = end - start
    logger.info(f"Completed, {elapsed=}, {status=}")
