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
        
        logging.debug("QueryString._generate_date_string(): class of mydate is %s ", mydate.__class__)
        logging.debug("QueryString._generate_date_string(): mydate %s ", str(mydate))
        yield str(mydate)

def GenerateQueryString():
    a = 'select * from 5min2 where symbol="@NQ" and date="'
#    b = str(_generate_date_string())
    b = (_generate_date_string())
    logging.debug("QueryString.GenerateQueryString(): class of b %s", b.__class__)
    logging.debug("QueryString.GenerateQueryString(): b %s", b)
    c = '";'
    abc = a + b + c
    yield abc
#    yield 'select * from 5min2 where symbol="@NQ" and date="' + str(_generate_date_string()) + '";'

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

    for myds in _generate_date_string():
        print myds

    for myqs in GenerateQueryString():
        print myqs

    logging.info("QueryString has finished")

