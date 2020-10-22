# -*- coding: utf-8 -*-
"""
Copied and modified from https://github.com/onemoretime/mySQLHandler/
"""
import MySQLdb
import logging
import time
import six
logger = logging.getLogger(__name__)
 
class mySQLHandler(logging.Handler):
    """
    Original Logging handler for MySQL modified for mariaDB syntax
    """

    log_table_sql = """SHOW TABLES LIKE '%s';"""

    initial_sql = """CREATE TABLE IF NOT EXISTS %s(
    Created text,
    Name text,
    LogLevel int,
    LogLevelName text,
    Message text,
    Args text,
    Module text,
    FuncName text,
    LineNo int,
    Exception text,
    Process int,
    Thread text,
    ThreadName text
    )"""

    insertion_sql = """INSERT INTO log(
    Created,
    Name,
    LogLevel,
    LogLevelName,
    Message,
    Args,
    Module,
    FuncName,
    LineNo,
    Exception,
    Process,
    Thread,
    ThreadName
    )
    VALUES (
    "%(dbtime)s",
    "%(name)s",
    %(levelno)d,
    "%(levelname)s",
    "%(msg)s",
    "%(args)s",
    "%(module)s",
    "%(funcName)s",
    %(lineno)d,
    "%(exc_text)s",
    %(process)d,
    "%(thread)s",
    "%(threadName)s"
    );
    """

    def __init__(self, **kwargs):
        """
        Customized logging handler that puts logs to the database.
        """
        logging.Handler.__init__(self)
        self.host = kwargs['host']
        self.port = kwargs['port']
        self.dbuser = kwargs['dbuser']
        self.dbpassword = kwargs['dbpassword']
        self.dbname = kwargs['dbname']
        self.sql_conn, self.sql_cursor =  self.connect_to_db(kwargs['log_table'])

    def connect_to_db(self, log_table):
        """
        Connect to MySQL database to perform logging.
        """
        try:
            conn=MySQLdb.connect(host=self.host,port=self.port,user=self.dbuser,passwd=self.dbpassword,db=self.dbname)
            cur = conn.cursor()
            cur.execute(mySQLHandler.log_table_sql % log_table)
            conn.commit()
            result = cur.fetchone()
            if not result:
                cur.execute(mySQLHandler.initial_sql % log_table)
                conn.commit()
            return conn, cur
        except Exception:
            return None, None

    def flush(self):
        """
        Override to implement custom flushing behaviour.
        """
        if self.sql_conn:
            self.sql_cursor.close()
            self.sql_conn.close()

    def formatDBTime(self, record):
        """
        Time formatter
        """
        record.dbtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created))

    def emit(self, record):
        """
        Emit a record.
        Format the record and send it to the specified database.
        """
        if self.sql_conn:
            try:
                self.format(record)
                self.formatDBTime(record)
                if record.exc_info:
                    record.exc_text = logging._defaultFormatter.formatException(record.exc_info).replace('"', "'").replace('\n','').replace('\r','')
                else:
                    record.exc_text = ""
                if isinstance(record.msg, str):
                    record.msg = record.msg.replace("'", "''")
                if isinstance(record.msg, six.string_types):# check is a string
                    record.msg=self.sql_conn.escape_string(record.msg)
                sql = mySQLHandler.insertion_sql % record.__dict__
                self.sql_cursor.execute(sql)
                self.sql_conn.commit()
            except Exception:
                self.sql_conn.rollback()
                self.handleError(record)
