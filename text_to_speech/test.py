from mySQLHandler import mySQLHandler
import logging

def main():
    def print_all_log(oLog):
        # Print all log levels
        oLog.debug('debug')
        oLog.info('info')
        oLog.warning('warning')
        oLog.error('error')
        oLog.critical('critical')
        oLog.exception('exception')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    db = {'host':'mariadb', 'port': 3306, 'dbuser':'pi', 'dbpassword':'JuveLivorno01', 'dbname':'mywords'}
    sqlh = mySQLHandler(db)
    logger.addHandler(sqlh)
    # In main Thread
    print_all_log(logger)

if __name__ == '__main__':
    main()
