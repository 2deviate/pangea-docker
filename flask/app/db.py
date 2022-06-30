"""
Copyright: Copyright (C) 2022 2DEVIATE Inc. - All Rights Reserved
Product: Standard
Description: Database connector.  Implementation of MySql data connector
Notifyees: craig@2deviate.com
Category: None
"""
import os
import re
import pymysql
import logging
from pymysql.constants import CLIENT

logger = logging.getLogger(__name__)


class MySql(object):
    def __init__(self) -> None:
        self.username = None
        self.password = None
        self.host = None
        self.port = None
        self.database = None
        self.uri = None
        self.regex = re.compile(r"\(([^\)]+)\)")

    def init_app(self, app):
        config = app.config
        logger.info(f"Init MySql connection, {config=}")
        try:
            # dont use config from app as this is share script
            # code which may not have the app context, instead
            # use environment variables
            self.username = os.getenv("MYSQL_USER", None)
            self.password = os.getenv("MYSQL_PASSWORD", None)
            self.host = os.getenv("MYSQL_HOST", None)
            port_str = os.getenv("MYSQL_PORT", None)
            if port_str is None:
                raise Exception(f"Invalid configuration, Port None")
            self.port = int(port_str)
            self.database = os.getenv("MYSQL_DATABASE", None)
            logger.info(
                f"Connection, un={self.username}, host={self.host}, port={self.port}, db={self.database}"
            )
        except ValueError as err:
            logger.error(err, exc_info=err)
            raise
        except Exception as err:
            logger.error(err, exc_info=err)
            raise

    def connect(self):
        connection = None
        try:
            connection = pymysql.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                port=self.port,
                database=self.database,
                client_flag=CLIENT.MULTI_STATEMENTS,  # required for identity fk's
            )
            logger.info(f"MySql Server, {connection.get_server_info=}")
        except pymysql.Error as err:
            logger.error(err, exc_info=err)
            raise
        except Exception as err:
            logger.error(err, exc_info=err)
            raise
        return connection

    def execute(self, proc, *args):
        logger.info(f"Executing sql command {proc=}, {args=}")
        with self.connect() as cnn:
            with cnn.cursor() as curs:
                try:
                    param_vals = None
                    status = curs.callproc(proc, args)
                    cnn.commit()
                    results = curs.fetchall()
                    last_executed = curs._last_executed
                    logger.info(
                        f"executed {proc=}, {last_executed=}, returned {status=}, fetchall {results=}"
                    )
                    proc_params = self.regex.findall(last_executed)
                    if proc_params:
                        stmt = f"SELECT {proc_params[0]}"
                        curs.execute(stmt)
                        param_vals = curs.fetchone()
                        logger.info(f"executed sql param {stmt=}, result {param_vals=}")
                    return results, param_vals
                except Exception as err:
                    logger.error(err, exc_info=err)
                    raise


db = MySql()
