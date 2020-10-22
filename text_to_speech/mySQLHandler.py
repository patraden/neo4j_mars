# -*- coding: utf-8 -*-
"""
Copied and modified from https://github.com/onemoretime/mySQLHandler/
"""
import MySQLdb
import logging
import time
 
class mySQLHandler(logging.Handler):
    """
    Logging handler for MySQL db.
    """

    check_sql = """SHOW TABLES LIKE '{log_table}';"""

    create_sql = """CREATE TABLE IF NOT EXISTS {log_table}(
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

    insert_sql = """INSERT INTO {log_table}(
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
    "{dbtime}",
    "{name}",
    {levelno},
    "{levelname}",
    "{msg}",
    "{args}",
    "{module}",
    "{funcName}",
    {lineno},
    "{exc_text}",
    {process},
    "{thread}",
    "{threadName}"
    );
    """

    def __init__(self, **kwargs):
        """
        Customized logging handler that puts logs to MySQL db.
        """
        logging.Handler.__init__(self)
        self.host = kwargs['host']
        self.port = kwargs['port']
        self.dbuser = kwargs['dbuser']
        self.dbpassword = kwargs['dbpassword']
        self.dbname = kwargs['dbname']
        self.log_table = kwargs['log_table']
        self.sql_conn, self.sql_cursor =  self.connect_to_db()

    def connect_to_db(self):
        """
        Connect to MySQL database to perform logging.
        Create log table if does not exist.
        """
        try:
            conn=MySQLdb.connect(host=self.host,port=self.port,user=self.dbuser,passwd=self.dbpassword,db=self.dbname)
            cur = conn.cursor()
            cur.execute(mySQLHandler.check_sql.format(log_table = self.log_table))
            conn.commit()
            table_exist = cur.fetchone()
            if not table_exist:
                cur.execute(mySQLHandler.create_sql.format(log_table = self.log_table))
                conn.commit()
            return conn, cur
        except Exception: # ignoring connection and table creation exceptions as this handler meant to be used with application db
            return None, None

    def flush(self):
        """
        Override to implement custom flushing behaviour for MySQLdb connection.
        """
        if self.sql_conn:
            self.sql_cursor.close()
            self.sql_conn.close()

    def formatDBTime(self, record):
        """
        Time formatter.
        """
        record.dbtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created))

    def emit(self, record):
        """
        Emit a record to MySQL db.
        Format the record and send it to the specified database.
        """
        if self.sql_conn:
            try:
                self.format(record)
                self.formatDBTime(record)
                record.exc_text = logging._defaultFormatter.formatException(record.exc_info).replace('"', "'").replace('\n','').replace('\r','') if record.exc_info else ""
                if isinstance(record.msg, str): record.msg = record.msg.replace("'", "''")
                sql_stmt = mySQLHandler.insert_sql.format(**record.__dict__, log_table = self.log_table)
                self.sql_cursor.execute(sql_stmt)
                self.sql_conn.commit()
            except Exception:
                self.sql_conn.rollback()
                self.handleError(record)
