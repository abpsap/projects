'''
Created on Nov 21, 2013

@author: rriehle
'''

import datetime as dt
import logging

def generate_query_string():
    '''
    Generate a query string from time frame, symbol and date.  Sample query_string as follows:
    query_string = 'select * from 5min2 where symbol="@NQ" and date="2013-10-22";'
    '''
    begin = dt.datetime(2012, 10, 01)
    end   = dt.datetime(2013, 11, 30)
    for i in range((end - begin).days + 1):
        yield (begin+dt.timedelta(days = i)).date()

if __name__ == '__main__':

    def pylogger():
        from logging.handlers import SysLogHandler
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        syslog = SysLogHandler(address="/dev/log")
        formatter = logging.Formatter('%(module)s[%(process)d]: %(levelname)s %(message)s')
        syslog.setFormatter(formatter)
        logger.addHandler(syslog)

    logger = pylogger()
    logging.info("QueryString has started")

#    for mytr in myts.capture_traderun():
#        try:
#            print("len(mytr) is ", len(mytr))
#        except:
#            print("len(mytr) is undefined, so we're done!")
#            break

    for myqs in generate_query_string():
	print myqs

    logging.info("QueryString has finished")

