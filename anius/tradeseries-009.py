'''
Created on Nov 21, 2013

@author: rriehle
'''

import datetime as dt
import logging
import MySQLdb as db
import pandas as pd
import pandas.io.sql as psql
from querystring import GenerateQueryString

#query_string = 'select * from 5min2 where symbol="@NQ" and date="2013-10-22";'

trade_duration_seconds = 20  # Trade duration in terms of seconds
trade_duration_volume  = 200   # Trade duration in terms of volume

class TradeSeries(object):
    '''
    classdocs
    """A TradeSeries is a special case of a timeseries which includes last trade, bid, ask, etc."""
    '''

    def __init__(self, query_string):
        '''
        Constructor
        '''
        logging.debug("TradeSeries.__init__(): Connecting to trade data server")
        mydb = db.connect(host="hoyne.rsquaredtrading.com", user="rriehle", passwd="daZxD95zf7=cVhrD", db="Data")

        logging.debug("TradeSeries.__init__(): Fetching data from trade data server")
        self.df = psql.frame_query(query_string, con=mydb)

#         logging.debug("TradeSeries.__init__(): Type of self is %s", self.__class__)
#         logging.debug("TradeSeries.__init__(): Type of self.df is %s", self.df.__class__)

        logging.debug("TradeSeries.__init__(): Closing connection to trade data server")
        mydb.close()
    
    def startindex(self):
        """Perhaps this is the method that assesses indicators to identify the entry condition."""
        pass

    def endindex(self,index0):
        """Given the starting index of a traderun, return the ending index as defined by the number of elapsed seconds."""
        i = index0  # Use i to iterate through df.time until we reach trade_turation_seconds

        try:
            start_time = self.df.time[index0]  # Save the starting time for clarity
        except KeyError:
            logging.debug("TradeSeries.endindex(): indexing operation raised KeyError, end of Tradeseries, returning None")
            return None

        tdelta = self.df.time[i] - start_time  # Initial time delta will be 0
#         logging.debug("TradeSeries.endindex(): tdelta %s, tdelta.total_seconds() %d", str(tdelta), tdelta.total_seconds())
        while tdelta.total_seconds() < trade_duration_seconds:  # While time delta is short of our target duration
            i += 1  # Move on to the next record
            try:
                tdelta = self.df.time[i] - start_time  # Compute the time delta between this record and the original start time
            except KeyError:
                logging.debug("TradeSeries.endindex(): indexing operation raised KeyError, end of Tradeseries, returning None")
                return None
#         logging.debug("TradeSeries.endindex(): index0 is %d, i is %d, tdelta is %s", index0, i, str(tdelta))
        return i  # Return the index once we've reached our target time
        
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
                logging.info("TradeSeries.capture_traderun(): Skipping non-contiguous traderun: df.index.intem(0) %d, df.index.item(len(df2)-1) is %d, len(df2) is %d", df2.index.item(0), df2.index.item(len(df2)-1), len(df2))
                return True
            else:
                return False

        while(True):                                        # Need the while loop around the whole routine, because this is a generator/yield
            index_end = self.endindex(index_start)
            if index_end == None:
                logging.debug("TradeSeries.capture.traderun(), endindex() returned None indicating end of TradeSeries, yielding None.")
                yield None

            normalize_value = self.df.lasttrd[index_start]  # Record the price at the beginning of the traderun
            start_time = self.df.time[index_start]          # Record the time at the beginning of the traderun

            logging.debug("TradeSeries.capture_traderun(): index_start is %d, index_end is %d", index_start, index_end)
            
            try: 
                df2 = self.df[index_start:index_end]        # Create a new dataframe from the original timeseries
                logging.debug("TradeSeries.capture_traderun(): len(df2) is %d", len(df2))
            except:
                logging.debug("TradeSeries.capture_traderun(): Unable to create DataFrame from self.df; probably at end of traderun")
                yield None
            
            if _traderun_is_not_contiguous():             
                index_start += index_end + 1
                continue
             
            df3 = df2.copy(deep=True)                  # df2 is a reference variable of/into df, so copy it to a new dframe before making modifications
#             print("TradeSeries.capture_traderun(): df3.lasttrd", df3.lasttrd)
#             print("TradeSeries.capture_traderun(): df3.time", df3.time)
#             logging.debug("TradeSeries.capture_traderun(): len(df3) is %d,           df3.lasttrd[0] %d,           df3.time[0] %s", len(df3), df3.lasttrd[0], df3.time[0])
#             logging.debug("TradeSeries.capture_traderun(): len(df3) is %d, df3.lasttrd[index_end-1] %d, df3.time[index_end-1] %s", len(df3), df3.lasttrd[index_end-1], df3.time[index_end-1])
            df3.lasttrd -= normalize_value             # Subtract the initial price from every price in the traderun
            df3.time -= start_time                     # Subtract the initial time from every time in the traderun
#             print("TradeSeries.capture_traderun(): d3 after normalization....")
#             print("TradeSeries.capture_traderun(): df3.lasttrd", df3.lasttrd)
#             print("TradeSeries.capture_traderun(): df3.time", df3.time)
#             logging.debug("TradeSeries.capture_traderun(): len(df3) is %d,           df3.lasttrd[0] %d,           df3.time[0] %s", len(df3), df3.lasttrd[0], df3.time[0])
#             logging.debug("TradeSeries.capture_traderun(): len(df3) is %d, df3.lasttrd[index_end-1] %d, df3.time[index_end-1] %s", len(df3), df3.lasttrd[index_end-1], df3.time[index_end-1])
            
            logging.debug("TradeSeries.capture_traderun(): yielding a Traderun")
            yield df3                                  # The new timeseries will be normalized to +/- zero vis-a-vis price and time

            if index_end < len(self.df):
                logging.debug("TradeSeries.capture_traderun(): index_end is %d, len(self.df) is %d, thus not yet at end of tradeseries, continuing...", index_end, len(self.df))
                index_start = index_end + 1
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

    num_trade_runs = 0

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

    for myquerystring in GenerateQueryString():
        print myquerystring
    
        myts = TradeSeries(myquerystring)
#        logging.debug("TradeSeries.__main__(): Type of myts is %s", myts.__class__)

        print("Length of DataFrame myts.df is ", len(myts.df))
        if len(myts.df) == 0:
            continue

        for mytr in myts.capture_traderun():
            try:
                print("len(mytr) is ", len(mytr))
                num_trade_runs += 1
                logging.debug("TradeSeries.__main__(): len(mtr) is %d", len(mytr))
#                 print("Time at myts.starttime(100) is ", str(myts.starttime(100)))
#                 print("Time at myts.endtime(100) is ", str(myts.endtime(100)))
            except:
                print("len(mytr) is undefined, so we're done with this Tradeseries, found %d Traderuns so far....", num_trade_runs)
                break

    print("TradeSeries is finished, found %d Traderuns", num_trade_runs)
    logger.info("TradeSeries is finished, found %d Traderuns", num_trade_runs)
