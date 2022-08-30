"""
Copyright: Copyright (C) 2022 2DEVIATE Inc. - All Rights Reserved
Product: Standard
Description: Redis Utility Script
Notifyees: craig@2deviate.com
Category: None

"""
import logging
import os
import urllib3
import time
import argparse
from app.db import db
from config import configs
from run import create_app


logger = logging.getLogger(__name__)
dir_path = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(
    filename="/".join([dir_path, "redis.log"]),
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s",
    force=True,
)

# script globals
docker_server_name = None
docker_server_port = None


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


def flushall(dry_run=True):    
    if not dry_run:
        url = f"http://{docker_server_name}:{docker_server_port}/api/v1.0/resource/cache/flushall"
        response = get_data(method='GET', url=url)
        logger.error(f"Logging cache flush all processing response", response)


def _main(**kwargs):
    dry_run = kwargs.get("dry_run", None)
    flush_cache = kwargs.get("flush_cache", False)
    try:
        if not dry_run and flush_cache:
            flushall(dry_run=dry_run)
    except Exception as err:
        logger.error(f"Fatal error processing", err)
        return True
    return False


if __name__ == "__main__":
    """Script args for managing redis cache"""
    start = time.time()
    logger.info(f"__main__ call")
    logger.info(f"Started clock {start=}")
    # setup environment, get flask config
    env = os.environ.get("FLASK_ENV", "default")
    config = configs[env]
    # setup app for config keys
    app = create_app(config=config)
    # setup docker server
    docker_server_name = app.config["DOCKER_SERVER_NAME"]
    docker_server_port = app.config["DOCKER_SERVER_PORT"]
    # parse args, invoke main
    p = argparse.ArgumentParser(description="Process command line parameters")
    p.add_argument(
        "--dry-run",
        action=argparse.BooleanOptionalAction,
        help="dry run flag, if set to True no writes",        
    )
    p.add_argument(
        "--flushall",
        action="store_true",
        help="flush cache, removes all cached data"
    )
    args = p.parse_args()
    status = _main(**vars(args))
    # capture wall time and status
    end = time.time()
    elapsed = end - start
    logger.info(f"Completed, {args=}, {status=}, {elapsed=}")
