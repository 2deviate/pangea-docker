"""
Copyright: Copyright (C) 2022 2DEVIATE Inc. - All Rights Reserved
Product: Standard
Description: Database connector.  Implementation of MySql data connector
Notifyees: craig@2deviate.com
Category: None
"""
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
        self.regex = re.compile(r'\(([^\)]+)\)')

    def init_app(self, app):
        config = app.config
        logger.info(f"Init MySql connection, {app=}, {config=}")     
        try:            
            self.username = config.get("MYSQL_USER", None)
            self.password = config.get("MYSQL_PASSWORD", None)
            self.host = config.get("MYSQL_HOST", None)
            port_str = config.get("MYSQL_PORT", None)
            self.port = int(port_str)
            self.database = config.get("MYSQL_DATABASE", None)
            logger.info(f"Connection, un={self.username}, host={self.host}, port={self.port}, db={self.database}")
        except ValueError as err:
            logger.error(err, exc_info=err)
        except Exception as err:
            logger.error(err, exc_info=err)

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
        except Exception as err:
            logger.error(err, exc_info=err)
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
                    logger.info(f"executed {proc=}, {last_executed=}, returned {status=}, fetchall {results=}")
                    proc_params = self.regex.findall(last_executed)                    
                    if proc_params:
                        stmt = f'SELECT {proc_params[0]}'                    
                        curs.execute(stmt)
                        param_vals = curs.fetchone()
                        logger.info(f"executed sql param {stmt=}, result {param_vals=}")                    
                    return results, param_vals
                except Exception as err:
                    logger.error(err, exc_info=err)
                    raise err
db = MySql()
