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

    def add(self):
        self.add()

    def consolidate(self):
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

    mytradeset.add(mytradeseries.capture_traderun(100, 200))
    mytradeset.add(mytradeseries.capture_traderun(800, 900))
    df = mytradeset.consolidate(mytradeset)

    print("Length of df is ", len(df))
    
    logger.info("TradeSet is finished")
    
    