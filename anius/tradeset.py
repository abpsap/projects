'''
Created on Nov 25, 2013

@author: rriehle
'''

import logging
import pandas as pd

class TradeSet(object):
    '''
    classdocs
    '''
        
    def __new__(self):
        return(set())

    def __init__(self):
        '''
        Constructor
        '''
        pass

    def add(self,traderun):
        '''Add the TradeRun to the TradeSet'''
        logging.debug("len(traderun)", len(traderun))
        self.add(traderun)

    def consolidate(self):
        '''Return a consolidated, sorted, single Pandas DataFrame from all of the Pandas DataFrames in the TradeSet'''
        for e in self:
            df = pd.concat(e)
        dfsorted = df.sort_index(by='time')
        return(dfsorted)

#     The following code worked in a unit test elsewhere:
#     df10 = pd.concat([df2,df3,df4,df5])
#     df20 = df10.sort_index(by='time')
        
if __name__ == '__main__':

    from tradeseries import TradeSeries
    
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
    logger.info("TradeSet has started")
    
    mytradeseries = TradeSeries()
    print("Length of mytradeseries.df is ", len(mytradeseries.df))

    mytradeset = TradeSet()
    print("Type of mytradeset is ", mytradeset.__class__)

    mytraderun01 = mytradeseries.capture_traderun(100, 200)
    mytraderun02 = mytradeseries.capture_traderun(800, 900)

    print("Length of mytraderun01 is ", len(mytraderun01))
    print("Length of mytraderun02 is ", len(mytraderun02))

    mytradeset.add(mytraderun01)
    mytradeset.add(mytraderun02)

    df = mytradeset.consolidate()

    print("Length of df is ", len(df))
    
    logger.info("TradeSet is finished")
    
    