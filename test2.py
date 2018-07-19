#运行环境python3.6
from datetime import *

#今天
today=datetime.now()
print(type(today))
print(today)
print(today.year)
print(today.month)
print(today.day)
#明天
tomorrow = today + timedelta(days=1)
print(tomorrow)
#将格式字符串转换为datetime对象
newDate=datetime.strptime("2017-10-04", "%Y-%m-%d")
print(type(newDate))
print(newDate)


#计算两个日期之间相差的天数
def betweenDay(day1,day2):
    dt = datetime.strptime(day1, "%Y-%m-%d")
    dt2 = datetime.strptime(day2, "%Y-%m-%d")
    d1y=dt.year
    d1m=dt.month
    d1d=dt.day
    d1 = date(d1y, d1m, d1d)
    d2y=dt2.year
    d2m=dt2.month
    d2d=dt2.day
    d2 = date(d2y, d2m, d2d)
    x=(d1 - d2).days
    print(type(x))
    return x
print(betweenDay('2017-6-29','2017-5-19'))

#计算加上或减去n天后的日期
def computeDay(day,n):
    day=datetime.strptime(day, "%Y-%m-%d")
    nextday=day+timedelta(days=n)
    return ("%s-%s-%s " % (nextday.year,nextday.month,nextday.day))

    # a=str(nextday.year)+"-"+str(nextday.month)+"-"+

computeDay("2017-09-30",-5)
computeDay("2017-09-30",15)

print("=================")
#把2017
def relurDay(day):
    alist=[]
    for i in day:
        dt = datetime.strptime(i, "%Y-%m-%d")
        d1m = dt.month
        d1d = dt.day
        if int(d1m)<10:
            d1m='0'+str(d1m)
        if int(d1d)<10:
            d1d='0'+str(d1d)
        x=("%s-%s-%s" % (dt.year,d1m,d1d))
        alist.append(x)
    return alist
blist=['2018-1-2','2017-1-5']
relurDay(blist)