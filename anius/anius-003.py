'''
Created on Nov 12, 2013

@author: rriehle
'''

#import numpy as np
#import pandas as pd
import datetime as dt
import logging
import pandas as pd
from querystring import GenerateQueryString
from tradeseries import TradeSeries
# from tradeset import TradeSet


def consolidate_tradeset(myts):
    '''Return a consolidated, sorted, single Pandas DataFrame from all of the Pandas DataFrames in the TradeSet'''
    
#     df = pd.DataFrame()
#     for e in myts:
#         logging.debug("Class of e is %s", e.__class__)
#         df = pd.concat(e)

    dfaggregate = pd.concat(mytradeset)
    dfsorted = dfaggregate.sort_index(by='time')
    
    return(dfsorted)

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
    logger.info("anius has started")

    for myquerystring in GenerateQueryString():
        print myquerystring
    
        mytradeseries = TradeSeries(myquerystring)

        logging.debug("Class of mytradeseries is %s", mytradeseries.__class__)
        logger.info("Length of DataFrame mytradeseries.df is %i", len(mytradeseries.df))
    
    #    mytr = mytradeseries.capture_traderun(100,200)   
    #    logging.debug("Type of mytr is %s", mytr.__class__)
    
        mytradeset = set()
    
        for mytraderun in mytradeseries.capture_traderun():
            try:
                print("len(mytraderun) is ", len(mytraderun))
                mytradeset.add(mytraderun)
            except:
                print("len(mytraderun) is undefined, so we're done!")
                break
    
    #     mytraderun01 = mytradeseries.capture_traderun(100, 200)
    #     mytraderun02 = mytradeseries.capture_traderun(800, 900)
    
    #     mytradeset = set()
    #     mytradeset.add(mytraderun01)
    #     mytradeset.add(mytraderun02)

    finaltraderun = consolidate_tradeset(mytradeset)
    
    print(finaltraderun['lasttrd'].describe())

#    finaltraderun.lasttrd.plot(use_index=False)

    dfuuu = mytradeseries.df[ (mytradeseries.df['trend']==2)  & (mytradeseries.df['shorttrend']==2)  & (mytradeseries.df['longtrend']==2)  ]

    criterion = dfuuu['vclose'].map(lambda x: x <= 4.04764039964)
    dfuuu[criterion]
    
    
#     dfuuu = df[ (df['trend']==2)  & (df['shorttrend']==2)  & (df['longtrend']==2)  ]
#     dfuu0 = df[ (df['trend']==2)  & (df['shorttrend']==2)  & (df['longtrend']==0)  ]
#     dfuud = df[ (df['trend']==2)  & (df['shorttrend']==2)  & (df['longtrend']==-2) ]
#     dfu0u = df[ (df['trend']==2)  & (df['shorttrend']==0)  & (df['longtrend']==2)  ]
#     dfu00 = df[ (df['trend']==2)  & (df['shorttrend']==0)  & (df['longtrend']==0)  ]
#     dfu0d = df[ (df['trend']==2)  & (df['shorttrend']==0)  & (df['longtrend']==-2) ]
#     dfudu = df[ (df['trend']==2)  & (df['shorttrend']==-2) & (df['longtrend']==2)  ]
#     dfud0 = df[ (df['trend']==2)  & (df['shorttrend']==-2) & (df['longtrend']==0)  ]
#     dfudd = df[ (df['trend']==2)  & (df['shorttrend']==-2) & (df['longtrend']==-2) ]
#     df0uu = df[ (df['trend']==0)  & (df['shorttrend']==2)  & (df['longtrend']==2)  ]
#     df0u0 = df[ (df['trend']==0)  & (df['shorttrend']==2)  & (df['longtrend']==0)  ]
#     df0ud = df[ (df['trend']==0)  & (df['shorttrend']==2)  & (df['longtrend']==-2) ]
#     df00u = df[ (df['trend']==0)  & (df['shorttrend']==0)  & (df['longtrend']==2)  ]
#     df000 = df[ (df['trend']==0)  & (df['shorttrend']==0)  & (df['longtrend']==0)  ]
#     df00d = df[ (df['trend']==0)  & (df['shorttrend']==0)  & (df['longtrend']==-2) ]
#     df0du = df[ (df['trend']==0)  & (df['shorttrend']==-2) & (df['longtrend']==2)  ]
#     df0d0 = df[ (df['trend']==0)  & (df['shorttrend']==-2) & (df['longtrend']==0)  ]
#     df0dd = df[ (df['trend']==0)  & (df['shorttrend']==-2) & (df['longtrend']==-2) ]
#     dfduu = df[ (df['trend']==-2) & (df['shorttrend']==2)  & (df['longtrend']==2)  ]
#     dfdu0 = df[ (df['trend']==-2) & (df['shorttrend']==2)  & (df['longtrend']==0)  ]
#     dfdud = df[ (df['trend']==-2) & (df['shorttrend']==2)  & (df['longtrend']==-2) ]
#     dfd0u = df[ (df['trend']==-2) & (df['shorttrend']==0)  & (df['longtrend']==2)  ]
#     dfd00 = df[ (df['trend']==-2) & (df['shorttrend']==0)  & (df['longtrend']==0)  ]
#     dfd0d = df[ (df['trend']==-2) & (df['shorttrend']==0)  & (df['longtrend']==-2) ]
#     dfddu = df[ (df['trend']==-2) & (df['shorttrend']==-2) & (df['longtrend']==2)  ]
#     dfdd0 = df[ (df['trend']==-2) & (df['shorttrend']==-2) & (df['longtrend']==0)  ]
#     dfddd = df[ (df['trend']==-2) & (df['shorttrend']==-2) & (df['longtrend']==-2) ]
    
    #  Note that including the screen for the vclose at this level of the program, before iterative processing, is incorrect,
    #  because it will lead to an artificially high rate of flicker of initial entry conditions and therefore skew results.
    
#     dfuuu = df[ (df['trend']==2)  & (df['shorttrend']==2)  & (df['longtrend']==2)  & (df['vclose']<=-4.04764039964) ]
#     dfuu0 = df[ (df['trend']==2)  & (df['shorttrend']==2)  & (df['longtrend']==0)  & (df['vclose']<=-4.76417749748) ]
#     dfuud = df[ (df['trend']==2)  & (df['shorttrend']==2)  & (df['longtrend']==-2) & (df['vclose']<=-4.13861925445) ]
#     dfu0u = df[ (df['trend']==2)  & (df['shorttrend']==0)  & (df['longtrend']==2)  & (df['vclose']<=-4.91537064605) ]
#     dfu00 = df[ (df['trend']==2)  & (df['shorttrend']==0)  & (df['longtrend']==0)  & (df['vclose']<=-5.44565420654) ]
#     dfu0d = df[ (df['trend']==2)  & (df['shorttrend']==0)  & (df['longtrend']==-2) & (df['vclose']<=-4.95587748430) ]
#     dfudu = df[ (df['trend']==2)  & (df['shorttrend']==-2) & (df['longtrend']==2)  & (df['vclose']<=-4.80429611982) ]
#     dfud0 = df[ (df['trend']==2)  & (df['shorttrend']==-2) & (df['longtrend']==0)  & (df['vclose']<=-4.48430662326) ]
#     dfudd = df[ (df['trend']==2)  & (df['shorttrend']==-2) & (df['longtrend']==-2) & (df['vclose']<=-5.08143646781) ]
#     df0uu = df[ (df['trend']==0)  & (df['shorttrend']==2)  & (df['longtrend']==2)  & (df['vclose']<=-6.54130796415) ]
#     df0u0 = df[ (df['trend']==0)  & (df['shorttrend']==2)  & (df['longtrend']==0)  & (df['vclose']<=-6.98370504851) ]
#     df0ud = df[ (df['trend']==0)  & (df['shorttrend']==2)  & (df['longtrend']==-2) & (df['vclose']<=-7.12133634292) ]
#     df00u = df[ (df['trend']==0)  & (df['shorttrend']==0)  & (df['longtrend']==2)  & (df['vclose']<=-7.04157317948) ]
#     df000 = df[ (df['trend']==0)  & (df['shorttrend']==0)  & (df['longtrend']==0)  & (df['vclose']<=-7.60161035793) ]
#     df00d = df[ (df['trend']==0)  & (df['shorttrend']==0)  & (df['longtrend']==-2) & (df['vclose']<=-8.16827818869) ]
#     df0du = df[ (df['trend']==0)  & (df['shorttrend']==-2) & (df['longtrend']==2)  & (df['vclose']<=-6.48816341905) ]
#     df0d0 = df[ (df['trend']==0)  & (df['shorttrend']==-2) & (df['longtrend']==0)  & (df['vclose']<=-6.82932266486) ]
#     df0dd = df[ (df['trend']==0)  & (df['shorttrend']==-2) & (df['longtrend']==-2) & (df['vclose']<=-8.07630172755) ]
#     dfduu = df[ (df['trend']==-2) & (df['shorttrend']==2)  & (df['longtrend']==2)  & (df['vclose']<=-6.72414808193) ]
#     dfdu0 = df[ (df['trend']==-2) & (df['shorttrend']==2)  & (df['longtrend']==0)  & (df['vclose']<=-8.22475973216) ]
#     dfdud = df[ (df['trend']==-2) & (df['shorttrend']==2)  & (df['longtrend']==-2) & (df['vclose']<=-9.44844736198) ]
#     dfd0u = df[ (df['trend']==-2) & (df['shorttrend']==0)  & (df['longtrend']==2)  & (df['vclose']<=-8.90679755796) ]
#     dfd00 = df[ (df['trend']==-2) & (df['shorttrend']==0)  & (df['longtrend']==0)  & (df['vclose']<=-9.55531697976) ]
#     dfd0d = df[ (df['trend']==-2) & (df['shorttrend']==0)  & (df['longtrend']==-2) & (df['vclose']<=-9.28591422926) ]
#     dfddu = df[ (df['trend']==-2) & (df['shorttrend']==-2) & (df['longtrend']==2)  & (df['vclose']<=-10.2452175762) ]
#     dfdd0 = df[ (df['trend']==-2) & (df['shorttrend']==-2) & (df['longtrend']==0)  & (df['vclose']<=-9.46847620508) ]
#     dfddd = df[ (df['trend']==-2) & (df['shorttrend']==-2) & (df['longtrend']==-2) & (df['vclose']<=-11.0170724181) ]

#     if len(dfuuu) <> 0:
#         print("dfuuu", len(dfuuu))
#         dfuuu.lasttrd.plot()
#     if len(dfuu0) <> 0:
#         print("dfuu0", len(dfuu0))
#         dfuu0.lasttrd.plot()
#     if len(dfuud) <> 0:
#         print("dfuud", len(dfuud))
#         dfuud.lasttrd.plot()
#     if len(dfu0u) <> 0:
#         print("dfu0u", len(dfu0u))
#         dfu0u.lasttrd.plot()
#     if len(dfu00) <> 0:
#         print("dfu00", len(dfu00))
#         dfu00.lasttrd.plot()
#     if len(dfu0d) <> 0:
#         print("dfu00", len(dfu00))
#         dfu0d.lasttrd.plot()
#     if len(dfudu) <> 0:
#         print("dfudu", len(dfudu))
#         dfudu.lasttrd.plot()
#     if len(dfud0) <> 0:
#         print("dfud0", len(dfud0))
#         dfud0.lasttrd.plot()
#     if len(dfudd) <> 0:
#         print("dfudd", len(dfudd))
#         dfudd.lasttrd.plot()
#     if len(df0uu) <> 0:
#         print("df0uu", len(df0uu))
#         df0uu.lasttrd.plot()
#     if len(df0u0) <> 0:
#         print("df0u0", len(df0u0))
#         dfu0u.lasttrd.plot()
#     if len(df0ud) <> 0:
#         print("df0ud", len(df0ud))
#         df0ud.lasttrd.plot()
#     if len(df00u) <> 0:
#         print("df00u", len(df00u))
#         df00u.lasttrd.plot()
#     if len(df000) <> 0:
#         print("df000", len(df000))
#         df000.lasttrd.plot()
#     if len(df00d) <> 0:
#         print("df00d", len(df00d))
#         df00d.lasttrd.plot()
#     if len(df0du) <> 0:
#         print("df0du", len(df0du))
#         df0du.lasttrd.plot()
#     if len(df0d0) <> 0:
#         print("df0d0", len(df0d0))
#         df0d0.lasttrd.plot()
#     if len(df0dd) <> 0:
#         print("df0dd", len(df0dd))
#         df0dd.lasttrd.plot()
#     if len(dfduu) <> 0:
#         print("dfduu", len(dfduu))
#         dfduu.lasttrd.plot()
#     if len(dfdu0) <> 0:
#         print("dfdu0", len(dfdu0))
#         dfdu0.lasttrd.plot()
#     if len(dfdud) <> 0:
#         print("dfdud", len(dfdud))
#         dfdud.lasttrd.plot()
#     if len(dfd0u) <> 0:
#         print("dfd0u", len(dfd0u))
#         dfd0u.lasttrd.plot()
#     if len(dfd00) <> 0:
#         print("dfd00", len(dfd00))
#         dfd00.lasttrd.plot()
#     if len(dfd0d) <> 0:
#         print("dfd0d", len(dfd0d))
#         dfd0d.lasttrd.plot()
#     if len(dfddu) <> 0:
#         print("dfddu", len(dfddu))
#         dfddu.lasttrd.plot()
#     if len(dfdd0) <> 0:
#         print("dfdd0", len(dfdd0))
#         dfdd0.lasttrd.plot()
#     if len(dfddd) <> 0:
#         print("dfddd", len(dfddd))
#         dfddd.lasttrd.plot()

#     dfuuu.lasttrd.plot(use_index=False)
#     dfuu0.lasttrd.plot(use_index=False)
#     dfuud.lasttrd.plot(use_index=False)
#     dfu0u.lasttrd.plot(use_index=False)
#     dfu00.lasttrd.plot(use_index=False)
#     dfu0d.lasttrd.plot(use_index=False)
#     dfudu.lasttrd.plot(use_index=False)
#     dfud0.lasttrd.plot(use_index=False)
#     dfudd.lasttrd.plot(use_index=False)
#     df0uu.lasttrd.plot(use_index=False)
#     df0u0.lasttrd.plot(use_index=False)
#     df0ud.lasttrd.plot(use_index=False)
#     df00u.lasttrd.plot(use_index=False)
#     df000.lasttrd.plot(use_index=False)
#     df00d.lasttrd.plot(use_index=False)
#     df0du.lasttrd.plot(use_index=False)
#     df0d0.lasttrd.plot(use_index=False)
#     df0dd.lasttrd.plot(use_index=False)
#     dfduu.lasttrd.plot(use_index=False)
#     dfdu0.lasttrd.plot(use_index=False)
#     dfdud.lasttrd.plot(use_index=False)
#     dfd0u.lasttrd.plot(use_index=False)
#     dfd00.lasttrd.plot(use_index=False)
#     dfd0d.lasttrd.plot(use_index=False)
#     dfddu.lasttrd.plot(use_index=False)
#     dfdd0.lasttrd.plot(use_index=False)
#     dfddd.lasttrd.plot(use_index=False)
    
#     dfuuu.vclose.plot(use_index=False)
#     dfuu0.vclose.plot(use_index=False)
#     dfuud.vclose.plot(use_index=False)
#     dfu0u.vclose.plot(use_index=False)
#     dfu00.vclose.plot(use_index=False)
#     dfu0d.vclose.plot(use_index=False)
#     dfudu.vclose.plot(use_index=False)
#     dfud0.vclose.plot(use_index=False)
#     dfudd.vclose.plot(use_index=False)
#     df0uu.vclose.plot(use_index=False)
#     df0u0.vclose.plot(use_index=False)
#     df0ud.vclose.plot(use_index=False)
#     df00u.vclose.plot(use_index=False)
#     df000.vclose.plot(use_index=False)
#     df00d.vclose.plot(use_index=False)
#     df0du.vclose.plot(use_index=False)
#     df0d0.vclose.plot(use_index=False)
#     df0dd.vclose.plot(use_index=False)
#     dfduu.vclose.plot(use_index=False)
#     dfdu0.vclose.plot(use_index=False)
#     dfdud.vclose.plot(use_index=False)
#     dfd0u.vclose.plot(use_index=False)
#     dfd00.vclose.plot(use_index=False)
#     dfd0d.vclose.plot(use_index=False)
#     dfddu.vclose.plot(use_index=False)
#     dfdd0.vclose.plot(use_index=False)
#     dfddd.vclose.plot(use_index=False)

    logger.info("anius is finished")
