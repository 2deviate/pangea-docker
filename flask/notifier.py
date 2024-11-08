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
import shutil
import pandas
import urllib3
import time
import argparse
import tempfile
import asyncio
import datetime
import jinja2
from run import create_app
from app.db import db
from config import configs
import app.constants as const
from dateutil import parser
from functools import reduce
from json import JSONDecodeError
from flask import render_template

import smtplib
from email.mime.text import MIMEText
from email.mime.image import  MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email_validator import validate_email, EmailNotValidError

from xlsxwriter.utility import xl_cell_to_rowcol, xl_rowcol_to_cell

SOGEA_BASE = 30.05

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

excel_template_schema = None


class ExcelFormatter(object):
    """Simple Excel Formatter Class"""

    def __init__(self, workbook, worksheet, df) -> None:
        self.workbook = workbook
        self.worksheet = worksheet
        self.df = df

    @property
    def rows(self):
        return self.worksheet.dim_rowmax

    @property
    def columns(self):
        return self.worksheet.dim_colmax

    def set_border(self, xrange, border):
        formatter = self.workbook.add_format()
        formatter.set_border(border["style"])
        formatter.set_bottom(border["bottom"])
        formatter.set_top(border["top"])
        formatter.set_left(border["left"])
        formatter.set_right(border["right"])
        self.worksheet.conditional_format(
            xrange, {"type": "no_errors", "format": formatter}
        )

    def set_background_color(self, xrange, color):
        formatter = self.workbook.add_format()
        formatter.set_pattern(1)
        formatter.set_bg_color(color)
        self.worksheet.conditional_format(
            xrange,
            {
                "type": "text",
                "criteria": "containing",
                "value": "",
                "format": formatter,
            },
        )

    def set_width(self, xrange, width):
        self.worksheet.set_column(xrange, width)

    def set_zoom(self, zoom):
        self.worksheet.set_zoom(zoom)

    def set_format(self, xrange, format):
        formatter = self.workbook.add_format(format)
        self.worksheet.set_column(xrange, None, formatter)

    def set_condition(self, xrange, criteria, format):
        formatter = self.workbook.add_format(format)
        condition = criteria | {"format": formatter}
        self.worksheet.conditional_format(xrange, condition)

    def set_formula(self, xrange, formula):
        start_row, start_column = xl_cell_to_rowcol(xrange)
        for row in range(start_row, self.rows + 1):
            cell_obj = self.worksheet.table[row][start_column]
            cell_formula = formula.format(cell_value=cell_obj.number)
            cell_ref = xl_rowcol_to_cell(row, start_column)
            self.worksheet.write_array_formula(cell_ref, cell_formula, cell_obj.format)

    def set_merge(self, xrange, cell_value, format):
        formatter = self.workbook.add_format(format)
        self.worksheet.merge_range(xrange, cell_value, formatter)


    @staticmethod
    def format(formatter):
        dt0 = datetime.date.today()
        dt1 = dt0 + datetime.timedelta(days=60)
        dt2 = datetime.date.today() + datetime.timedelta(days=90)
        df = formatter.df
        formatter.set_formula(f"I5:I{5+formatter.rows}", '=IF({cell_value}>0.0,{cell_value},"Unlimited")')
        formatter.set_condition(f"G5:G{5+formatter.rows-4}",{"type": "date", "criteria": "between", "minimum": dt0, "maximum": dt1},{"bg_color": "#FFC7CE"},)
        formatter.set_condition(f"G5:G{5+formatter.rows-4}",{"type": "date", "criteria": "between", "minimum": dt1, "maximum": dt2},{"bg_color": "#FFEB9C"},)
        formatter.set_border("I1:I1", {"bottom": 0, "top": 0, "left": 0, "right": 1, "style": 1})
        formatter.set_border("I2:I2", {"bottom": 0, "top": 0, "left": 0, "right": 1, "style": 1})
        formatter.set_border("I3:I3", {"bottom": 0, "top": 0, "left": 0, "right": 1, "style": 1})
        formatter.set_border("A1:H4", {"bottom": 0, "top": 0, "left": 0, "right": 0, "style": 1})
        formatter.set_width("A:A", 0)
        formatter.set_width("B:B", 15)
        formatter.set_width("C:C", 15)
        formatter.set_width("D:D", 15)
        formatter.set_width("E:E", 15)
        formatter.set_width("F:F", 25)
        formatter.set_width("G:G", 22)
        formatter.set_width("H:H", 25)        
        formatter.set_width("J:AJ", 7)
        formatter.set_background_color("J1:J1", "#E2EFDA")
        formatter.set_background_color("S1:S1", "#C6E0B4")
        formatter.set_background_color("AB1:AB1", "#A9D08E")
        formatter.set_format(f"J5:AJ{5+formatter.rows-3}", {"num_format": "£#,##0.00"})
        formatter.set_merge("A1:A4", "Row", {"bold": 1, "border": 0, "align": "center", "valign": "vcenter"})
        formatter.set_merge("B1:B4", df.columns[0][0], {"bold": 1, "border": 0, "align": "center", "valign": "vcenter"})
        formatter.set_merge("C1:C4", df.columns[1][0], {"bold": 1, "border": 0, "align": "center", "valign": "vcenter"})
        formatter.set_merge("D1:D4", df.columns[2][0], {"bold": 1, "border": 0, "align": "center", "valign": "vcenter"})
        formatter.set_merge("E1:E4", df.columns[3][0], {"bold": 1, "border": 0, "align": "center", "valign": "vcenter"})
        formatter.set_merge("F1:F4", df.columns[4][0], {"bold": 1, "border": 0, "align": "center", "valign": "vcenter"})
        formatter.set_merge("G1:G4", df.columns[5][0], {"bold": 1, "border": 0, "align": "center", "valign": "vcenter"})
        formatter.set_merge("H1:H4", df.columns[6][0], {"bold": 1, "border": 0, "align": "center", "valign": "vcenter"})
        formatter.set_merge("I1:I4", df.columns[7][0], {"bold": 1, "border": 0, "align": "center", "valign": "vcenter"})
        formatter.set_format(f"I5:I{5+formatter.rows-4}", {"align": "center"})
        formatter.set_width("I:I", 25)
        formatter.set_zoom(75)


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


def valid_content(content):
    is_valid = (
        True
        if content is not None and isinstance(content, str) and len(content) > 1
        else False
    )
    return is_valid


def render_jinja_html(template_loc, file_name,**context):
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_loc+'/')).get_template(file_name).render(context)


def send_mail(from_addr, to_addrs, cc_addrs, bcc_addrs, attachment):
    "Sends mail with excel attachment"
    
    logger.info(f"sending mail, {from_addr=}, {to_addrs=}, {cc_addrs=}, {bcc_addrs=}, {attachment=}")

    msg_alternative = MIMEMultipart("alternative")
    if valid_content(email_template_text):
        text_content = email_template_text.strip()
        text_part = MIMEText(text_content, "plain")        
        msg_alternative.attach(text_part)

    if valid_content(email_template_html):
        html_template_path = os.path.join(dir_path, "app/templates")
        html_content = render_jinja_html(html_template_path, email_template_html, **attachment)
        html_part = MIMEText(html_content, "html")
        msg_alternative.attach(html_part)
    
    msg_mixed = MIMEMultipart("mixed")
    msg_mixed.attach(msg_alternative)

    # This example assumes the image is in the current directory
    imamge_content_path = os.path.join(dir_path, "app/static/img/", "pangea-163x50.png")
    with open(imamge_content_path, 'rb') as imgfil:
        image_content = imgfil.read()
        if image_content:
            msg_image = MIMEImage(image_content)        

        # Define the image's ID as referenced above
        msg_image.add_header('Content-ID', '<image1>')
        msg_mixed.attach(msg_image)
    
    df = attachment.get('df', None)
    if not df.empty:
        tmpdir = tempfile.mkdtemp()
        tmpfil = os.path.join(tmpdir, "temp.xlsx")
        logger.info(f"created tmp file {tmpfil=}")
        # open writer
        writer = pandas.ExcelWriter(
            tmpfil,
            engine="xlsxwriter",
            datetime_format="mm/dd/yyyy",
            date_format="mm/dd/yyyy",
        )
        # write df
        df.to_excel(writer, sheet_name="Sales Planner", merge_cells=True)
        # get excel workbook and sheet
        workbook = writer.book
        worksheet = writer.sheets["Sales Planner"]
        # format sheet
        formatter = ExcelFormatter(workbook, worksheet, df)
        ExcelFormatter.format(formatter)
        # save excel
        writer.save()
        # open binary attachment
        fp = open(tmpfil, "rb")
        attachment = MIMEApplication(fp.read(), _subtype="xls")
        fp.close()
        # clean up
        if os.path.exists(tmpfil):
            try:
                os.remove(tmpfil)  # remove tmp file
                shutil.rmtree(tmpdir)  # remove tmp folder
            except OSError as err:
                logger.error(
                    f"Unable to remove file {tmpfil=} or directory {tmpdir=}", err
                )
        # attach header
        attachment.add_header(
            "Content-Disposition", "attachment", filename=email_attachment
        )
        msg_mixed.attach(attachment)
    # setup mail address's
    to_addrs = [addrs for addrs in set(to_addrs) if validate_addrs(addrs) is not None]
    cc_addrs = [addrs for addrs in set(cc_addrs) if validate_addrs(addrs) is not None]
    bcc_addrs = [addrs for addrs in set(bcc_addrs) if validate_addrs(addrs) is not None]
    # setup mime message
    msg_mixed["From"] = from_addr
    msg_mixed["To"] = ",".join(to_addrs)
    msg_mixed["Cc"] = ",".join(cc_addrs)
    msg_mixed["Bcc"] = ",".join(bcc_addrs)
    msg_mixed["Subject"] = email_subject
    # send message
    try:
        logger.info(f"login to smpt sever {smtp_host=}, {smtp_port=}")
        smtp_obj = smtplib.SMTP_SSL(host=smtp_host, port=smtp_port)
        smtp_obj.ehlo()
        smtp_obj.login(smtp_user, smtp_password)
        logger.debug(
            f"send mail {from_addr=}, {to_addrs=}, envelope={msg_mixed.as_string()}"
        )
        smtp_obj.sendmail(
            from_addr, (to_addrs + cc_addrs + bcc_addrs), msg_mixed.as_string()
        )
        smtp_obj.quit()
    except Exception as err:
        logger.error(f"Error sending mail", err)
        raise


def validate_addrs(email):
    if email is None or not isinstance(email, str) or len(email) == 0:
        logger.warning(f"Invalid email address, removing {email=}")
        return None
    try:
        stripped = email.strip()
        return validate_email(stripped).email
    except EmailNotValidError as err:
        logger.error(f"Error parsing email address, {email=}", err)
        return None


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


def set_status(proc, *args):
    try:
        db.execute(proc, *args)
        logger.info(f"executed {proc=}, args {args=}")
    except Exception as err:
        logger.error(f"Error executing {proc=}, {args=}", err)
        raise


def parse_data(data_obj):
    if data_obj is None or len(data_obj) < 4:  # valid json obj "{}"
        return None
    try:
        data = json.loads(data_obj)
        if data and isinstance(data, list):
            return dict({"results": data})
        if data and isinstance(data, dict):
            data = data.get("response", data)
            return data
        return None
    except JSONDecodeError as err:
        logger.error(f"Error parsing data {data_obj=}", err)
        raise


async def request_data(url, kwargs={}):
    data_obj = get_data(method="GET", url=url)
    data = parse_data(data_obj)
    if data and kwargs:
        return kwargs | data
    elif kwargs:
        return kwargs
    return None


async def process_query(query, dry_run):
    schema = [
        "exchange_query_id",
        "cli",
        "site_postcode",
        "exchange_name",
        "exchange_code",
        "exchange_postcode",
        "avg_data_usage",
        "implementation_date",
        "file_upload_fk",
        "exchange_query_status_fk",
    ]
    query = {k: query[i] for i, k in enumerate(schema)}

    exchange_query_id = query["exchange_query_id"]
    cli = query["cli"]
    site_postcode = query["site_postcode"]
    avg_data_usage = query["avg_data_usage"]
    exchange_code = query["exchange_code"]

    if not dry_run:
        args = (exchange_query_id, const.EXCHANGE_QUERY_STATUS_BUSY)
        set_status(const.SP_UPDATE_EXCHANGE_QUERY_STATUS, *args)
    # http://localhost/api/v1.0/pangea/product/pricing/result/13?limit=3.0
    url = f"http://{docker_server_name}:{docker_server_port}/api/v1.0/pangea/product/pricing/result/store/{exchange_query_id}?limit={avg_data_usage}"
    t1 = request_data(url, query)

    criterion = cli if cli else site_postcode if site_postcode else exchange_code
    url = f"http://{docker_server_name}:{docker_server_port}/api/v1.0/pangea/sam/exchange/info?query={criterion}"
    t2 = request_data(url, query)

    # prop and await results
    results = await asyncio.gather(t1, t2)

    # combine dicts using reduce on merge lambda
    data = reduce(lambda x, y: x | y, results, {})

    exchange_code = data["exchange_code"]
    if exchange_code:
        url = f"http://{docker_server_name}:{docker_server_port}/api/v1.0/pangea/decommission/exchange/search?query={exchange_code}"
        t1 = request_data(url, data)
        results = await asyncio.gather(t1)
        data = reduce(lambda x, y: x | y, results, {})

        implementation_date = data["implementation_date"]

        if implementation_date is None:
            url = f"http://{docker_server_name}:{docker_server_port}/api/v1.0/pangea/sam/exchange/info?exchange_code={exchange_code}"
            t1 = request_data(url, data)
            results = await asyncio.gather(t1)
            data = reduce(lambda x, y: x | y, results, {})

    implementation_date = data.get("implementation_date")

    if implementation_date:
        try:
            data["stop_sell_date"] = (
                parser.parse(implementation_date).date().strftime("""%Y-%m-%d""")
            )
        except parser.ParserError as err:
            logger.error(f"Unable to parse, {implementation_date=}", err)
            pass

    data = {k: v for k, v in data.items() if v is not None}

    args = (
        data.get("exchange_query_id"),
        data.get("cli", const.NOT_PROVIDED),
        data.get("site_postcode", const.NOT_PROVIDED),
        data.get("exchange_name", const.NO_DATA_RESULTS_FOUND),
        data.get("exchange_code", const.NO_DATA_RESULTS_FOUND),
        data.get("exchange_postcode", const.NO_DATA_RESULTS_FOUND),
        data.get("avg_data_usage"),
        data.get("stop_sell_date", const.NO_STOP_SELL_INFORMATION),
        data.get("file_upload_fk"),
        const.EXCHANGE_QUERY_STATUS_DONE,
    )

    proc = const.SP_UPDATE_EXCHANGE_QUERY

    try:
        affected, _ = db.execute(proc, *args)
        logger.info(f"Executed {proc=}, {args=}, {affected=}")
    except Exception as err:
        logger.error(f"Error updating, {proc=}, {args=}", err)
        if not dry_run:
            args = (exchange_query_id, const.EXCHANGE_QUERY_STATUS_EXCEPTION)
            set_status(const.SP_UPDATE_EXCHANGE_QUERY_STATUS, *args)
        raise


async def process_upload(upload, dry_run):
    file_upload_id, *_ = upload

    if not dry_run:
        args = (file_upload_id, const.FILE_STATUS_UPLOAD)
        set_status(const.SP_UPDATE_FILE_UPLOAD_STATUS, *args)

    proc = const.SP_GET_EXCHANGE_QUERY_BY_FILE_UPLOAD_ID
    if not dry_run:
        try:
            queries, _ = db.execute(proc, file_upload_id)
            logger.info(
                f"fetched builk queries, {proc=}, {file_upload_id=}, {dry_run=}"
            )
        except Exception as err:
            logger.error(f"Error uploading, {proc=}, raising err", err)
            if not queries and not dry_run:
                args = (file_upload_id, const.FILE_STATUS_EXCEPTION)
                set_status(const.SP_UPDATE_FILE_UPLOAD_STATUS, *args)
            raise

    if not dry_run:
        args = (file_upload_id, const.FILE_STATUS_PROCESS)
        set_status(const.SP_UPDATE_FILE_UPLOAD_STATUS, *args)

    for query in queries:
        logger.info(f"processing {query=}")
        try:
            await process_query(query, dry_run)
        except Exception as err:
            logger.error(f"Error processing upload query, {query=}", err)

    if not dry_run:
        args = (file_upload_id, const.FILE_STATUS_NOTIFY)
        set_status(const.SP_UPDATE_FILE_UPLOAD_STATUS, *args)


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


async def process_notification(notification, dry_run):
    file_upload_id, email_to_address, *_ = notification
    try:
        # http://localhost/api/v1.0/pangea/product/pricing/recommendations/file/upload/3
        url = f"http://{docker_server_name}:{docker_server_port}/api/v1.0/pangea/product/pricing/recommendations/file/upload/{file_upload_id}"
        data_obj = get_data(method="GET", url=url)
        result = parse_data(data_obj)
    except Exception as err:
        logger.error(f"Error executing  {url=}, {result=}, {dry_run=}", err)
        raise Exception("process_notification failed")
    try:
        products = []
        multi_level_index = [
            email_template_schema["product_class"],
            email_template_schema["product_category"],
            email_template_schema["product_term"],
        ]
        single_level_index = [        
            email_template_schema["cli"],
            email_template_schema["site_postcode"],
            email_template_schema["exchange_name"],
            email_template_schema["exchange_code"],
            email_template_schema["avg_data_usage"],
            email_template_schema["stop_sell_date"],
            email_template_schema["switch_off_date"],
            email_template_schema["product_limit"],
        ]
        drop_columns = [
            "exchange_query_status_id",
            "exchange_query_id",
            "redis_cache_result_key",
            "file_email_address",
            "file_upload_id",
        ]
        # error if result not well formed
        if (
            result is None
            or not isinstance(result, dict)
            or len(result) == 0
            or "results" not in result.keys()
        ):
            logger.error(f"Parsed data error, {result=}, {notification=}")
            raise Exception("process_notification failed")
        # process result
        for record in result["results"]:
            product_df = pandas.DataFrame.from_dict(record["product_pricing"])
            product_df = product_df.drop(["product_name", "product_unit"], axis=1)
            product_df.rename(columns=email_template_schema, inplace=True)
            prices_df = pandas.DataFrame.from_dict(record)
            prices_df = prices_df.drop(drop_columns + ["product_pricing"], axis=1)
            prices_df.rename(columns=email_template_schema, inplace=True)
            combined_df = pandas.concat([product_df, prices_df], axis=1)
            products.append(combined_df)
        # concat dataframes
        df = pandas.concat(products)
        df[email_template_schema["stop_sell_date"]] = pandas.to_datetime(
            df[email_template_schema["stop_sell_date"]]
        )
        df[email_template_schema["switch_off_date"]] = pandas.to_datetime(
            df[email_template_schema["switch_off_date"]]
        )
        df = pandas.pivot_table(
            df,
            index=single_level_index,
            columns=multi_level_index,
            values=email_template_schema["product_price"],
        )
        df.columns.names = (None, None, None)  # reset multi-level index names
        # aggregates
        count = len(df)
        pangea = df.sum().groupby(level=0).min().sum()
        sogea = count * SOGEA_BASE
        #PAN-43. Fix Excel merge cells (keys on pivot table)        
        df.reset_index(inplace=True)        
        #PAN-42. End
        # on sheet formatting
        df.columns.names = (None, None, None)  # reset multi-level index names
        #setup attachment
        attachment = {'pangea': "{:,.2f}".format(pangea), 'sogea': "{:,.2f}".format(sogea), 'count': count, 'df': df}
        # setup mail
        from_addr = email_from_address
        to_addrs = email_to_address.split(",")
        cc = email_cc_address.split(",")
        bcc = email_bcc_address.split(",")
        # send mail with attachments
        logger.info(f"sending mail {from_addr=}, {to_addrs=}, {cc=}, {bcc=}")
        args = (file_upload_id, const.FILE_STATUS_COMPLETE)
        if not dry_run:
            send_mail(from_addr, to_addrs, cc, bcc, attachment=attachment)
            set_status(const.SP_UPDATE_FILE_UPLOAD_STATUS, *args)
        logger.info(f"sent mail {args=}, {df=}")
        if not dry_run:
            args = (file_upload_id, const.FILE_STATUS_SENT)
            set_status(const.SP_UPDATE_FILE_UPLOAD_STATUS, *args)
        logger.info(f"updated status, {args=}")
        return True
    except Exception as err1:
        if not dry_run:
            args = (file_upload_id, const.FILE_STATUS_EXCEPTION)
            set_status(const.SP_UPDATE_FILE_UPLOAD_STATUS, *args)
        logger.error(f"Error sending mail, {notification=}, {email_to_address=}", err1)
        raise Exception("process_notification failed")


async def process_notifications(dry_run):
    try:
        if not dry_run:
            proc, args = const.SP_GET_UPLOADED_FILES, const.FILE_STATUS_NOTIFY
            notifications, _ = db.execute(proc, args)
            for notification in notifications:
                await process_notification(notification, dry_run)
        logger.info(f"fetched notifications, {dry_run=}")
    except Exception as err:
        logger.error(f"Error processing notification, raising err", err)
        raise


async def _main(**kwargs):
    dry_run = kwargs.get("dry_run", None)
    try:
        await process_uploads(dry_run)
        await process_notifications(dry_run)
    except Exception as ex:
        logger.error(f"Error processing uploads and notifications, {kwargs=}", ex)
        return False
    return True


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
    # setup excel template content
    excel_template_schema = app.config["EXCEL_TEMPLATE_SCHEMA"]
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
