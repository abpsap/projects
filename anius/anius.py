'''
Created on Nov 12, 2013

@author: rriehle
'''

import datetime as dt
import logging
import pandas as pd
from querystring import GenerateQueryString
from tradeseries import TradeSeries

TREND0 = 0
TREND1 = 1
TREND2 = 2
VCLOSE = 3


def consolidate_tradeset(myts):
    '''Return a consolidated, sorted, single Pandas DataFrame from all of the Pandas DataFrames in the TradeSet'''

    dfaggregate = pd.concat(myts)
    dfsorted = dfaggregate.sort_index(by='time')
    
    return(dfsorted)

def get_selection_criterion():
#  Note that including the screen for the vclose at this level of the program, before iterative processing, is incorrect,
#  because it will lead to an artificially high rate of flicker of initial entry conditions and therefore skew results.

    # Alternate, not very good method. Uses lambda for an example.
#     dfuuu = mytradeseries.df[ (mytradeseries.df['trend']==2) & (mytradeseries.df['shorttrend']==2) & (mytradeseries.df['longtrend']==2) ]
#     criterion = dfuuu['vclose'].map(lambda x: x <= 4.04764039964)
#     mydf = dfuuu[criterion]
    
    vclose = [-4.04764039964, \
              -4.76417749748, \
              -4.13861925445, \
              -4.91537064605, \
              -5.44565420654, \
              -4.95587748430, \
              -4.80429611982, \
              -4.48430662326, \
              -5.08143646781, \
              -6.54130796415, \
              -6.98370504851, \
              -7.12133634292, \
              -7.04157317948, \
              -7.60161035793, \
              -8.16827818869, \
              -6.48816341905, \
              -6.82932266486, \
              -8.07630172755, \
              -6.72414808193, \
              -8.22475973216, \
              -9.44844736198, \
              -8.90679755796, \
              -9.55531697976, \
              -9.28591422926, \
              -10.2452175762, \
              -9.46847620508, \
              -11.0170724181 ]

    i = 0
    for j in [2, 0, -2]:
        for k in [2, 0, -2]:
            for l in [2, 0, -2]:
                yield [j, k, l, vclose[i]]
                i += 1


if __name__ == '__main__':    

    def pylogger():
        from logging.handlers import SysLogHandler
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        syslog = SysLogHandler(address="/dev/log")
        formatter = logging.Formatter('%(module)s[%(process)d]: %(levelname)s %(message)s')
        syslog.setFormatter(formatter)
        logger.addHandler(syslog)
        return(logger)
        
    logger = pylogger()
    logger.info("Anius has started")

    mytradeset = set()

    for selection_criterion in get_selection_criterion():
        print "trend0", selection_criterion[TREND0], "trend1", selection_criterion[TREND1], "trend2", selection_criterion[TREND2], "vclose", selection_criterion[VCLOSE]
    
        for myquerystring in GenerateQueryString():
            logger.info("anius: querystring is %s", myquerystring)
        
            mytradeseries = TradeSeries(myquerystring)
    
            if len(mytradeseries.df) == 0:
                logger.info("Length of DataFrame mytradeseries.df is %i; skipping this tradeseries", len(mytradeseries.df))
                continue
        
            mytradeseries.df_select = mytradeseries.df[ \
                                                       (mytradeseries.df['trend']      == selection_criterion[TREND0]) & \
                                                       (mytradeseries.df['shorttrend'] == selection_criterion[TREND1]) & \
                                                       (mytradeseries.df['longtrend']  == selection_criterion[TREND2]) & \
                                                       (mytradeseries.df['vclose']     <= selection_criterion[VCLOSE]) \
                                                        ]
            
            for mytraderun in mytradeseries.capture_traderun():
                try:
                    logging.info("anius: len(mytraderun) is %d", len(mytraderun))
                    try:
                        mytradeset.add(mytraderun)
                        logging.info("anius: len(mytradeset) is %d", len(mytradeset))
                    except:
                        logging.debug("anius: unable to add tradeset!?")
                        break
                except:
                    logging.info("len(mytraderun) is undefined, so we're done!")
                    break
            
        print("anius: FINAL len(mytradeset) is %d", len(mytradeset))
        logging.info("anius: FINAL len(mytradeset) is %d", len(mytradeset))
    
        if len(mytradeset) == 0:
            logger.info("Anius is finished: no Traderuns found.")
            exit(1)
    
        finaltraderun = consolidate_tradeset(mytradeset)
        
        print("anius: finaltraderun['lasttrd'].describe", finaltraderun['lasttrd'].describe())

#         finaltraderun.lasttrd.plot(use_index=False)

    logger.info("Anius is finished")
