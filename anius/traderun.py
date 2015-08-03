'''
Created on Nov 21, 2013

@author: rriehle
'''

import logging
from tradeseries import TradeSeries

logger = None

trade_duration_seconds = 20  # Trade duration in terms of seconds
trade_duration_volume  = 200   # Trade duration in terms of volume

#class TradeRun(TradeSeries):
    '''
    classdocs
    '''


#     def __init__(self):
#         '''
#         Constructor
#         '''
#         pass

    
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
    logger.info("TradeRun has started")
    
    ts = TradeSeries()
    print("Length of DataFrame df is ", len(ts.df))

    ts2 = ts.capture_traderun(ts,100,200)
    ts3 = ts.capture_traderun(ts,800,900)
    ts4 = ts.capture_traderun(ts,10000,10200)
    ts5 = ts.capture_traderun(ts,10800,10900)
     
    df10 = ts.df.concat([ts2.df,ts3.df,ts4.df,ts5.df])
    df20 = df10.df.sort_index(by='time')
     
    df20.lasttrd.plot(use_index=False)
    
    logger.info("TradeRun is finished")
