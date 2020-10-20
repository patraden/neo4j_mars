# -*- coding: utf-8 -*-
"""
Copied and modified from https://github.com/onemoretime/mySQLHandler/
"""
import MySQLdb
import logging
import time
import six
 
class mySQLHandler(logging.Handler):
    """
    Original Logging handler for MySQL modified for mariaDB syntax
    """

    initial_sql = """CREATE TABLE IF NOT EXISTS log(
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

    def __init__(self, db):
        """
        Constructor
        @param db: ['host','port','dbuser', 'dbpassword', 'dbname'] 
        @return: mySQLHandler
        """
        logging.Handler.__init__(self)
        self.db = db
        # Try to connect to DB
        # Check if 'log' table in db already exists
        result = self.checkTablePresence()
        # If not exists, then create the table
        if not result:
            try:
                conn=MySQLdb.connect(host=self.db['host'],port=self.db['port'],user=self.db['dbuser'],passwd=self.db['dbpassword'],db=self.db['dbname'])
            except MySQLdb.Error as e:
                raise Exception(e)
                exit(-1)
            else:
                cur = conn.cursor()
                try:
                    cur.execute(mySQLHandler.initial_sql)
                except MySQLdb.Error as e:
                    conn.rollback()
                    cur.close()
                    conn.close()
                    raise Exception(e)
                    exit(-1)
                else:
                    conn.commit()
                finally:
                    cur.close()
                    conn.close()

    def checkTablePresence(self):
        try:
            conn=MySQLdb.connect(host=self.db['host'],port=self.db['port'],user=self.db['dbuser'],passwd=self.db['dbpassword'],db=self.db['dbname'])
        except MySQLdb.Error as e:
            raise Exception(e)
            exit(-1)
        else:
            # Check if 'log' table in db already exists
            cur = conn.cursor()
            stmt = """SHOW TABLES LIKE "log";"""
            cur.execute(stmt)
            result = cur.fetchone()
            cur.close()
            conn.close()
        if not result:
            return 0
        else:
            return 1

    def formatDBTime(self, record):
        """
        Time formatter
        @param record:
        @return: nothing
        """
        record.dbtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created))

    def emit(self, record):
        """
        Connect to DB, execute SQL Request, disconnect from DB
        @param record:
        @return:
        """
        # Use default formatting:
        self.format(record)
        # Set the database time up:
        self.formatDBTime(record)
        if record.exc_info:
            record.exc_text = logging._defaultFormatter.formatException(record.exc_info)
        else:
            record.exc_text = ""
        # Replace single quotes in messages
        if isinstance(record.__dict__['message'], str):
            record.__dict__['message'] = record.__dict__['message'].replace("'", "''")
        if isinstance(record.__dict__['msg'], str):
            record.__dict__['msg'] = record.__dict__['msg'].replace("'", "''")
        # Insert log record:
        try:
            conn=MySQLdb.connect(host=self.db['host'],port=self.db['port'],user=self.db['dbuser'],passwd=self.db['dbpassword'],db=self.db['dbname'])
        except MySQLdb.Error as e:
        #    from pprint import pprint
        #    print("The Exception during db.connect")
        #    pprint(e)
            raise Exception(e)
            exit(-1)
        # escape the message to allow for SQL special chars
        if isinstance(record.msg, six.string_types):# check is a string
          record.msg=conn.escape_string(record.msg)
        sql = mySQLHandler.insertion_sql % record.__dict__
        cur = conn.cursor()
        try:
            cur.execute(sql)
        except MySQLdb.ProgrammingError as e:
            errno, errstr = e.args
            if not errno == 1146:
                raise
            cur.close() # close current cursor
            cur = conn.cursor() # recreate it (is it mandatory?)
            try:            # try to recreate table
                cur.execute(mySQLHandler.initial_sql)
            except MySQLdb.Error as e:
                # definitly can't work...
                conn.rollback()
                cur.close()
                conn.close()
                raise Exception(e)
                exit(-1)
            else:   # if recreate log table is ok
                conn.commit()
                cur.close()
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                # then Exception vanished
        except MySQLdb.Error as e:
            conn.rollback()
            cur.close()
            conn.close()
            raise Exception(e)
            exit(-1)
        else:
            conn.commit()
        finally:
            cur.close()
            conn.close()
