"""
Copyright: Copyright (C) 2022 2DEVIATE Inc. - All Rights Reserved
Product: Standard
Description: ETL Loader Script to Create, Read and Load data into AWS database instance
Notifyees: craig@2deviate.com
Category: None
"""
import re
import csv
import logging
import urllib3
import os
import tempfile
import openpyxl
import time
import argparse
from app.db import db
from dateutil import parser
from app.scraper import WebScraper, scraper
from run import create_app
from config import configs
import app.constants as const

logger = logging.getLogger(__name__)
dir_path = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(
    filename="/".join([dir_path, "etl.log"]),
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s",
    force=True,
)

CHUNK_SIZE = 1024
FILENAME = "/".join([dir_path, "openreach.csv"])


class Row(object):    
    def __init__(self, *args) -> None:
        self.site_no = args[0] if args[0] else None
        self.exchange_name = args[1] if args[1] else None
        self.exchange_location = args[2] if args[2] else None
        self.exchange_code = args[3] if args[3] else None
        self.implementation_date = args[4] if args[4] else None
        self.last_amended_date = args[5] if args[5] else None
        self.tranche = args[6] if args[6] else None

    def values(self):
        site_no = str(self.site_no)
        exchange_name = str(self.exchange_name)
        exchange_location = str(self.exchange_location)
        exchange_code = str(self.exchange_code)
        implementation_date = str(self.implementation_date)
        last_amended_date = str(self.last_amended_date)
        tranche = str(self.tranche)

        try:
            last_amended_date = (
                parser.parse(last_amended_date).date().strftime("""%Y-%m-%d""")
            )
        except parser.ParserError as err:
            last_amended_date = None

        return (
            site_no,
            exchange_name,
            exchange_location,
            exchange_code,
            implementation_date,
            last_amended_date,
            tranche,
        )


def get_location_uri():
    method = "GET"
    url = "https://www.openreach.com/upgrading-the-UK-to-digital-phone-lines/industry"
    headers = {
        "authority": "www.openreach.com",
        "cache-control": "max-age=0",
        "sec-ch-ua": "' Not A;Brand';v='99', 'Chromium';v='99', 'Google Chrome';v='99'",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "sec-fetch-site": "none",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    }
    links = scraper.scrape(
        method=method,
        headers=headers,
        url=url,
        func=WebScraper.scrape_hrefs,
        **{"class": "cta-primary"},
    )
    uri = "https://www.openreach.com/content/dam/openreach/openreach-dam-files/documents/%s"
    search = [
        "Openreach_FTTP_Priority_Exchanges_StopSell",
        "Openreach_FTTP_PriorityExchangeStopSell",
    ]
    regex = re.compile("|".join(search))
    for link in links:
        href = link["href"]
        download = regex.search(href)
        if href and download:
            uri = uri % href.split("/")[-1]
            return uri


def download_file(url, dry_run):
    http = urllib3.PoolManager()
    r = http.request("GET", url, preload_content=False)
    tmp = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
    logger.error(f"created tmpfile {tmp.name=}")
    while True and not dry_run:
        data = r.read(CHUNK_SIZE)
        if not data:
            break
        tmp.write(data)
    r.release_conn()
    if tmp:
        tmp.close()
    return tmp.name


def export_csv(tempfile, sheetname, dry_run):
    filename = FILENAME
    logger.info(f"writing {tempfile=}, {sheetname=} to {filename}")
    if not dry_run:
        workbook = openpyxl.load_workbook(filename=tempfile)
        sheet = workbook[sheetname]
        if not sheet:
            return
        try:            
            with open(filename, "w", encoding="utf-8") as f:
                c = csv.writer(f, quoting=csv.QUOTE_ALL)
                for r in sheet.rows:
                    c.writerow([cell.value for cell in r])            
        except Exception as err:
            logger.error(f"error exporting, {filename=}", err)
            raise 
    if os.path.isfile(filename):
        return filename
    else:
        logger.error(f"{filename=} not a file or does not exist")
        raise


def import_csv(filename, dry_run):
    if not os.path.isfile(filename):
        logger.error(f"{filename=} does not exist")
        raise
    if not dry_run:
        with open(filename) as f:
            csv_reader = csv.reader(f, delimiter=",")
            for row in csv_reader:
                yield row


def import_data(filename, dry_run):
    logger.info(f"importing csv file data, {filename=}, {dry_run=}")

    proc = const.SP_TRUNCATE_EXCHANGE_DECOM
    try:
        if not dry_run:
            db.execute(proc)
        logger.info(f"truncated table succesfully, {dry_run=}")
    except Exception as err:
        logger.error(f"Error importing data, raising err", err)
        raise

    proc = const.SP_INSERT_EXCHANGE_DECOM
    with open(filename) as f:
        csv_reader = csv.reader(f, delimiter=",")
        line_count = 0
        for line in csv_reader:
            line_count += 1
            if line_count == 1:
                continue
            if line:
                row_obj = Row(*line)
                args = row_obj.values()                
                try:
                    logger.info(f"inserting row, proc={proc}, {args=}, {dry_run=}")
                    if not dry_run:
                        db.execute(proc, *args, None)
                except Exception as err:
                    logger.error(f"Error inserting data, raising err", err)
                    raise


def fetch_data(dry_run):
    logger.info(f"fetch data, {dry_run=}")
    
    filename = None
    tempfile = None
    try:
        uri = get_location_uri()
        logger.info(f"fetched url {uri=}")
        if uri:
            tempfile = download_file(uri, dry_run)
            logger.info(f"dowloaded content from {uri=}")
            if tempfile:
                filename = export_csv(tempfile, sheetname="Exchange List", dry_run=dry_run)
    except Exception as err:
        logger.error(f"Swallowed exception", err)
    finally:
        if tempfile and not dry_run:
            os.unlink(tempfile)
        logger.info(f"removed temp {tempfile=}")
    return filename


def _main(**kwargs):
    dry_run = kwargs.get("dry_run", None)
    try:
        filename = fetch_data(dry_run)
        if filename:        
            import_data(filename, dry_run)
    except Exception as err:
        logger.error(f"Fatal error processing", err)
        return 1
    return 0


if __name__ == "__main__":
    """Script args for loading files into the database"""
    start = time.time()
    logger.info(f"__main__ call")
    logger.info(f"Started clock {start=}")
    # setup environment
    env = os.environ.get("FLASK_ENV", "default")
    config = configs[env]
    app = create_app(config=config)
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
    logger.info(f"Completed, {args=}, {status=}, {elapsed=}")
