import time,calendar,datetime

#format and show the system time
def get_current_localtime():
    localtime =time.localtime()
    print "Current localtime is:", localtime
    return localtime


def get_current_timestamp():
    # get the current timestamp
    currentTimeStamp = time.time()
    print "Current TimeStamp is:", currentTimeStamp
    return currentTimeStamp


def formatTime1():
    # format time like "Tue Nov 22 06:57:41 2016"
    localtime1 = time.asctime(time.localtime(time.time()))
    print "The format1 localtime is:", localtime1

    # format time like "Tue Nov 22 06:57:41 2016"
    print time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())

    return localtime1

def formatTime2():
    # format time like "2016-11-22 06:57:41"
    localtime2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print "The format2 localtime is:", localtime2
    return localtime2


def transform_Timestr_To_TimeStamp(timeStr):
    #the time string should be like this : "Sat Mar 28 22:24:24 2016"
    timestamp_a = time.mktime(time.strptime(timeStr, "%a %b %d %H:%M:%S %Y"))
    print "The timestamp is:", timestamp_a
    return timestamp_a


def getDateTime():
    now = datetime.datetime.now()
    print now
    #2016-12-22 11:28:43.603380
    return now



#here is some operation about calendar
def showCalendar():
    #get the calendar of January,2016
    cal = calendar.month(2016,1)
    print cal


