# IPython log file

base = datetime.datetime.today()
dateList = [ base - datetime.timedelta(days=x) for x in range(0,numdays) ]
dateList = [ base - datetime.timedelta(days=x) for x in range(0,10) ]
dateList
import datetime
a = datetime.datetime.today()
numdays=10
dateList = []
for x in range (0, numdays):
    dataList.append(a - datetime.timedelta(days=x))
    
for x in range (0, numdays):
    dateList.append(a - datetime.timedelta(days=x))
    
print dateList
from dateutil import rrule
from datetime import datetime
list(rrule.rrule(rrule.DAILY,count=10,dtstart=datetime.now()))
def generate_dates(start_date, end_date):
    td = datetime.timedelta(hours=24)
    current_date = start_date
    while current_date <= end_date:
        print current_date
        current_date += td
        
start_date = datetime.date(2010, 1, 25)
start_date = datetime.date(2010, 1, 25)
for single_date in (start_date + timedelta(n) for n in range(10)):
    print strftime("%Y-%m-%d", single_date.timetuple())
    
def daterange(start_date, end_date):
    for n in range(int ((end-date - start_date).days)):
        yeild start_date + timedelta(n)
        
def daterange(start_date, end_date):
    for n in range(int ((end-date - start_date).days)):
        yeild (start_date + timedelta(n))
        
get_ipython().magic(u'reset ')
import datetime as dt
n = dt.datetime(2012, 12, 25)
s = dt.datetime(2012, 1, 1)
for i in range((n -s).days + 1):
    print (s+dt.dimedelta(days = i)).date()
    
for i in range((n -s).days + 1):
    print (s+dt.timedelta(days = i)).date()
    
get_ipython().magic(u'logstart ')
exit()
