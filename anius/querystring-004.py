'''
Created on Nov 21, 2013

@author: rriehle

Generate a query string from time frame, symbol and date.  Sample query_string as follows:
query_string = 'select * from 5min2 where symbol="@NQ" and date="2013-10-22";'
'''

import datetime as dt
import logging

def _generate_date_string():
    begin = dt.datetime(2012, 10, 01)
    end   = dt.datetime(2013, 11, 30)
    for i in range((end - begin).days + 1):
        mydate = (begin+dt.timedelta(days = i)).date()        
        logging.debug("QueryString._generate_date_string(): mydate %s ", str(mydate))
        yield str(mydate)

def GenerateQueryString():
    a = 'select * from 5min2 where symbol="@NQ" and date="'
    c = '";'
    for myds in _generate_date_string():
        yield a + myds + c
        
if __name__ == '__main__':

    def pylogger():
        from logging.handlers import SysLogHandler
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        syslog = SysLogHandler(address="/dev/log")
        formatter = logging.Formatter('%(module)s[%(process)d]: %(levelname)s %(message)s')
        syslog.setFormatter(formatter)
        logger.addHandler(syslog)

    print("QueryString has started")
    logger = pylogger()
    logging.info("QueryString has started")


    for myds in _generate_date_string():
        print myds

    for myqs in GenerateQueryString():
        print myqs

    logging.info("QueryString has finished")
    print("QueryString has finished")
