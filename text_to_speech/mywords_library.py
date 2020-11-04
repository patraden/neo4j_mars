import sys, os
APP_ROOT = '/app/text_to_speech/'
os.chdir(APP_ROOT)
from CONSTANTS import *

# module logging initiation
from LogSQLHandler import mySQLHandler
import logging
import logging.config
import MySQLdb
logging.config.fileConfig(LOG_CONFIG)
logger = logging.getLogger(LOGGER_NAME)

#logging.raiseExceptions = False

def logging_module(oLog):
    # Print all log levels
    oLog.debug('debug')
    oLog.info('info')
    oLog.warning('warning')
    oLog.error('error')
    oLog.critical('critical')
    oLog.exception('exception')
    a=8
    b=0
    try:
        r=a/b
    except Exception as e:
        oLog.exception(e)

class MydbConnection(MySQLdb.connections.Connection):
    """
    Subclass of MySQLdb.connections.Connection.
    With integrated connectivity parameters for my application.
    And exception handling through model level logger.
    Custom attribute 'Open' will return if connection was successful.
    """
    def __init__(self):
        try:
            from six.moves import configparser
            import json
            config = configparser.ConfigParser()
            config.read(APP_CONFIG)
            kwargs = json.loads(config['db']['connection'])
            super().__init__(**kwargs)
            self._open = True
        except Exception as e:
            self._open = False
            logger.exception(e)

def google_data_prepare(file_path = GOOGLE_CSV_FILE , data_schema=GOOGLE_DATA_SCHEMA):
    """
    Prepares google translate words extract file for load to application db.
    Returns None in case of failures.
    Logs exceptions to logger
    """
    try:
        import csv
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            data = list()
            for row in reader: data.append(row)
            data_schema.update({'data': data})
            return data_schema
            f.close()
    except Exception as e:
        logger.exception(e)
        return

def insert_data(data=None):
    """
    Validates data structure versus table_schema.
    Insert prepared data into db table using table_schema.
    Returns None in case of failures
    Logs exceptions to logger
    """

    check_sql = """SHOW TABLES LIKE '{table}';"""
    create_sql = """CREATE TABLE IF NOT EXISTS {table}({columns_types});"""
    insert_sql = """INSERT INTO {table} ({columns}) VALUES ({values});"""

    try:
        table = data['table']
        columns = data['columns']
        values = data['data']
    except TypeError as e:
        logger.exception(e)
        return -1 #input error
    else:
        columns_types = ','.join([' '.join(item) for item in columns.items()])
        check_sql = check_sql.format(table=table)
        create_sql = create_sql.format(table=table, columns_types=columns_types)
        db = MydbConnection()
        if db._open:
            cursor = db.cursor()
            cursor.execute(check_sql)
            db.commit()
            table_exist = cursor.fetchone()
            if not table_exist:
                cursor.execute(create_sql)
                db.commit()
            for row in values:
                columns_values = {'columns': ','.join(columns.keys()), 'values': ','.join("'{0}'".format(elem) for elem in row)}
                _insert_sql = insert_sql.format(table=table, **columns_values)
                cursor.execute(_insert_sql)
                db.commit()
            cursor.close()
            db.close()

if __name__ == '__main__':
    for handler in logger.handlers:
        if isinstance(handler, mySQLHandler):
            if not handler.sql_conn:
                logger.removeHandler(handler)
    google_data = google_data_prepare()
    if google_data:
        #insert_data(google_data)
        insert_data()
    else:
        logger.warning('csv data upload failed. please check syslog table for more details')
