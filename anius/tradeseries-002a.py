'''
Created on Nov 21, 2013

@author: rriehle
'''

import pandas.io.sql as psql
import MySQLdb as db
import logging

query_string = 'select * from 5min2 where symbol="@NQ" and date="2013-10-22";'

trade_duration_seconds = 20  # Trade duration in terms of seconds
trade_duration_volume  = 200   # Trade duration in terms of volume

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
        logging.debug("Connecting to trade data server")
        mydb = db.connect(host="hoyne.rsquaredtrading.com", user="rriehle", passwd="daZxD95zf7=cVhrD", db="Data")

        logging.debug("Fetching data from trade data server")
        self.df = psql.frame_query(query_string, con=mydb)

        logging.debug("Closing connection to trade data server")
        mydb.close()

    def capture_traderun(self,index_start,index_end):
        """Set lasttrd values across a traderun to +/- zero relative to the first lasttrd price.
        
        Todo: reset the index of the resulting dataframe to zero before returning to the caller."""
        
        normalize_value = self.df.lasttrd[index_start]  # Record the price at the beginning of the traderun
        start_time = self.df.time[index_start]          # Record the time at the beginning of the traderun
        df2 = self.df[index_start:index_end]            # Create a new dataframe from the original timeseries
        
        #  Some proposed traderuns might be non-contiguous due to a change away from initial trade entry conditions.
        #  Abort these traderuns.  Use the following condition to identify non-contiguous traderuns....
        #  Subtract the value of the first index from the value of the last index and compare it to the total length of the timeseries;
        #  If the length of the traderun is shorter than the difference then there are missing points in the timeseries; abort these.
        if df2.index.item(len(df2)-1) - df2.index.item(0) <> len(df2)-1:
            logger.info("Skipping non-contiguous timeseries", df2.index.item(0), df2.index.item(len(df2)-1), len(df2))
            return(None)
        
        df3 = df2.copy(deep=True)                  # df2 is a reference variable of/into df, so copy it to a new dframe before making modifications
        df3.lasttrd -= normalize_value             # Subtract the initial price from every price in the traderun
        df3.time -= start_time                     # Subtract the initial time from every time in the traderun
        
        return(df3)                                # The new timeseries will be normalized to +/- zero 

    def startindex(self):
        """Perhaps this is the method that assesses indicators to identify the entry condition."""
        pass

    def endindex(self,index0):
        """Given the starting index of a traderun, return the ending index as defined by the number of elapsed seconds."""
        i = index0  # Use i to iterate through df.time until we reach trade_turation_seconds
        start_time = self.df.time[index0]  # Save the starting time for clarity
        tdelta = self.df.time[i] - start_time  # Initial time delta will be 0
        while tdelta.total_seconds() < trade_duration_seconds:  # While time delta is short of our target duration
            i += 1  # Move on to the next record
            tdelta = self.df.time[i] - start_time  # Compute the time delta between this record and the original start time        
        print("Index at end of traderun is ", index0+i)
        return(index0+i)  # Return the index once we've reached our target time

    def starttime(self,index0):
        """Return clock time at beginning of traderun."""
        print("Time at beginning of traderun is ", str(self.df.time[index0]))
        return(self.df.time[index0])
    
    def endtime(self,index0):
        """Return clock time at end of traderun."""
        i = self.endindex(index0)
        print("Time at end of traderun is ", str(self.df.time[i]))
        return(self.df.time[i])

if __name__ == '__main__':    

    def pylogger():
        from logging.handlers import SysLogHandler
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        syslog = SysLogHandler(address="/dev/log")
        formatter = logging.Formatter('%(module)s[%(process)d]: %(levelname)s %(message)s')
        syslog.setFormatter(formatter)
        logger.addHandler(syslog)
        return(logger)
        
    logger = pylogger()
    logger.info("TradeSeries has started")
    
    ts = TradeSeries()
    print("Length of DataFrame df is ", len(ts.df))
    
    logger.info("TradeSeries is finished")
