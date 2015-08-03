'''
Created on Nov 21, 2013

@author: rriehle
'''

import datetime as dt
import logging
import MySQLdb as db
import pandas as pd
import pandas.io.sql as psql

query_string = 'select * from 5min2 where symbol="@NQ" and date="2013-10-22";'

trade_duration_seconds = 20  # Trade duration in terms of seconds
trade_duration_volume  = 200   # Trade duration in terms of volume

class TradeSeries(object):
    '''
    classdocs
    """A TradeSeries is a special case of a timeseries which includes last trade, bid, ask, etc."""
    '''

    def __init__(self):
        '''
        Constructor
        '''
        logging.debug("TradeSeries.__init__(): Connecting to trade data server")
        mydb = db.connect(host="hoyne.rsquaredtrading.com", user="rriehle", passwd="daZxD95zf7=cVhrD", db="Data")

        logging.debug("TradeSeries.__init__(): Fetching data from trade data server")
        self.df = psql.frame_query(query_string, con=mydb)

        logging.debug("TradeSeries.__init__(): Type of self is %s", self.__class__)
        logging.debug("TradeSeries.__init__(): Type of self.df is %s", self.df.__class__)

        logging.debug("TradeSeries.__init__(): Closing connection to trade data server")
        mydb.close()
    
    def startindex(self):
        """Perhaps this is the method that assesses indicators to identify the entry condition."""
        pass

    def endindex(self,index0):
        """Given the starting index of a traderun, return the ending index as defined by the number of elapsed seconds."""
        i = index0  # Use i to iterate through df.time until we reach trade_turation_seconds
        start_time = self.df.time[index0]  # Save the starting time for clarity
        tdelta = self.df.time[i] - start_time  # Initial time delta will be 0
        # logging.debug("TradeSeries.endindex(): tdelta %s", str(tdelta))
        while tdelta.total_seconds() < trade_duration_seconds:  # While time delta is short of our target duration
            i += 1  # Move on to the next record
            tdelta = self.df.time[i] - start_time  # Compute the time delta between this record and the original start time        
            # logging.debug("TradeSeries.__init__(): i is %d  tdelta is %s", i, str(tdelta))
        logging.debug("TradeSeries.endindex(): Index at end of traderun is %d  tdelta is %s", index0+i, str(tdelta))
        return(index0+i)  # Return the index once we've reached our target time
        
    def capture_traderun(self):
        '''Set lasttrd values across a traderun to +/- zero relative to the first lasttrd price; this is the definition of a "traderun"
        
        Todo: reset the index of the resulting dataframe to zero before returning to the caller.'''

        index_start = 0

        def _traderun_is_not_contiguous():
            #  Some proposed traderuns might be non-contiguous due to a change away from initial trade entry conditions.
            #  Abort these traderuns.  Use the following condition to identify non-contiguous traderuns....
            #  Subtract the value of the first index from the value of the last index and compare it to the total length of the timeseries;
            #  If the length of the traderun is shorter than the difference then there are missing points in the timeseries; abort these.
            if df2.index.item(len(df2)-1) - df2.index.item(0) <> len(df2)-1:
                logger.info("TradeSeries.capture_traderun(): Skipping non-contiguous traderun", df2.index.item(0), df2.index.item(len(df2)-1), len(df2))

        while(True):                                        # Need the while loop around the whole routine, because this is a generator/yield
            index_end   = self.endindex(index_start)

            normalize_value = self.df.lasttrd[index_start]  # Record the price at the beginning of the traderun
            start_time = self.df.time[index_start]          # Record the time at the beginning of the traderun
            
            try: 
                df2 = self.df[index_start:index_end]        # Create a new dataframe from the original timeseries
            except:
                logger.debug("TradeSeries.capture_traderun(): Unable to create DataFrame from self.df; probably at end of traderun")
                yield None
            
            if _traderun_is_not_contiguous():             
                index_start += index_end + 1
                continue
             
            df3 = df2.copy(deep=True)                  # df2 is a reference variable of/into df, so copy it to a new dframe before making modifications
            df3.lasttrd -= normalize_value             # Subtract the initial price from every price in the traderun
            df3.time -= start_time                     # Subtract the initial time from every time in the traderun
            
            logging.debug("TradeSeries.capture_traderun(): yielding df3")
            yield df3                                  # The new timeseries will be normalized to +/- zero vis-a-vis price and time

            if index_end < len(self.df):
                logging.debug("TradeSeries.capture_traderun(): Not yet at end of tradeseries, continuing...")
                index_start += index_end + 1
                continue
            else:
                logging.debug("TradeSeries.capture_traderun(): At end of tradeseries, yielding None")
                yield None

    def starttime(self,index0):
        """Return clock time at beginning of traderun."""
        #print("Time at beginning of traderun is ", str(self.df.time[index0]))
        logging.debug("TradeSeries.starttime(): Time at beginning of traderun is %s", str(self.df.time[index0]))
        return(self.df.time[index0])
    
    def endtime(self,index0):
        """Return clock time at end of traderun."""
        i = self.endindex(index0)
        logging.debug("TradeSeries.endtime(): Time at end of traderun is %s", str(self.df.time[i]))
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
    
    myts = TradeSeries()
    logging.debug("TradeSeries.__main__(): Type of myts is %s", myts.__class__)

    print("Length of DataFrame myts.df is ", len(myts.df))

    print("Time at myts.starttime(100) is ", str(myts.starttime(100)))
    print("Time at myts.endtime(100) is ", str(myts.endtime(100)))

    for mytr in myts.capture_traderun():
        try:
            print("len(mytr) is ", len(mytr))
        except:
            print("len(mytr) is undefined, so we're done!")
            break

    logger.info("TradeSeries is finished")
