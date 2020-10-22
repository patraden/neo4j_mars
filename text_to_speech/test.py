from mySQLHandler import mySQLHandler
import logging
import logging.config
import sys
#sys.path.append('/app/text_to_speech/')

def main():
    def print_all_log(oLog):
        # Print all log levels
        oLog.debug('debug')
        oLog.info('info')
        oLog.warning('warning')
        oLog.error('error')
        oLog.critical('critical')
        oLog.exception('exception')
    # In main Thread
    logging.config.fileConfig('./text_to_speech/logging.conf')
    logger = logging.getLogger('mywords')
    print_all_log(logger)
    a=8
    b=0
    try:
        r=a/b
    except Exception as e:
        logger.exception(e)

if __name__ == '__main__':
    main()
