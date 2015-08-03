'''
Created on Nov 21, 2013

@author: rriehle
'''

import pandas.io.sql as psql
import MySQLdb as db
import logging

query_string = 'select * from 5min2 where symbol="@NQ" and date="2013-10-22";'

class TradeSeries(object):
    '''
    classdocs
    """A TradeSeries is a special case of a timeseries which includes last trade, bid, ask, etc."""
    '''

    df = None

    def __init__(self):
        '''
        Constructor
        '''
        logger.debug("Connecting to trade data server")
        mydb = db.connect(host="hoyne.rsquaredtrading.com", user="rriehle", passwd="daZxD95zf7=cVhrD", db="Data")

        logger.debug("Fetching data from trade data server")
        self.df = psql.frame_query(query_string, con=mydb)

        logger.debug("Closing connection to trade data server")
        mydb.close()


if __name__ == '__main__':    

    def r2pylogger():
        from logging.handlers import SysLogHandler
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        syslog = SysLogHandler(address="/dev/log")
        formatter = logging.Formatter('%(module)s[%(process)d]: %(levelname)s %(message)s')
        syslog.setFormatter(formatter)
        logger.addHandler(syslog)
        return(logger)
        
    logger = r2pylogger()
    logger.info("TradeSeries has started")
    
    ts = TradeSeries()
    print("Length of DataFrame df is ", len(ts.df))
    
    logger.info("TradeSeries is finished")
