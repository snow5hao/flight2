# -*- encoding:utf-8 -*-
from urllib import request,parse
import re
from bs4 import BeautifulSoup
import json
from datetime import *
from sendMail import *
import sys
#出发地
depList=['厦门']

#目的地(东南亚)
arrList=['新加坡', '吉隆坡', '槟城', '怡保', '曼谷', '清迈', '普吉岛', '古晋', '雅加达', '巴里岛', '棉兰', '泗水', '仰光', '河内', '金边', '西贡', '永珍', '马尼拉', '宿雾', '阿皮亚', '达卡', '诗邬', '塞班', '新得里', '喀布尔', '吉大港', '喀拉蚩', '东加大埔', '孟买', '科伦坡', '加尔各答', '马德拉斯' ]

domestic=['哈尔滨','西安','兰州','拉萨','郑州']
def getSoup(url, charset="utf-8"):
    req = request.Request(url)
    content = request.urlopen(req).read().decode(charset, 'ignore')
    soup = BeautifulSoup(content, "html.parser")
    return soup

def betweenDay(day1,day2):
    day1=day1.strip()
    day2=day2.strip()
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
    return (d2 - d1).days

def computeDay(day,n):
    day=datetime.strptime(day.strip(), "%Y-%m-%d")
    nextday=day+timedelta(days=n)
    return ("%s-%s-%s " % (nextday.year,nextday.month,nextday.day))

#吧2017-9-8 这种时间处理成2017-09-08
def relurDay(day):
    alist=[]
    for i in day:
        i=i.strip()
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
# 去哪儿网
#qunaerUrl = 'https://lp.flight.qunar.com/api/lp_calendar?dep=%E5%8E%A6%E9%97%A8&arr=%E6%96%B0%E5%8A%A0%E5%9D%A1&dep_date=2017-11-06&adultCount=1&month_lp=0&tax_incl=1&direct=0&callback=jsonp_orqrdy253dbfulk'
def qunaerGetPrice(maxPrice,depCity,arrCity,beginDay,endDay):
    endDay=computeDay(endDay,-3)
    beginDay=computeDay(beginDay,3)
    urlList=[]
    x=betweenDay(beginDay, endDay)
    if x<7 and x>0:
        #只需要两个url即可
        urlList.append(beginDay)
        urlList.append(endDay)
    elif x>7:
        urlList.append(beginDay)
        urlList.append(endDay)
        while betweenDay(beginDay,endDay)>7:
            urlList.append(computeDay(beginDay,3))
            beginDay=computeDay(beginDay,3)
    elif x<=0:
        #只需要两个之间的任意一个url即可,这种情况需要排查结果中不在这个日期的价格
        urlList.append(beginDay)
    newurllist=relurDay(urlList)
    depCity1=parse.quote(depCity)
    arrCity1=parse.quote(arrCity)
    alist=[]
    blist=[]
    for t in newurllist:
        qunaerUrl = 'https://lp.flight.qunar.com/api/lp_calendar?dep='+depCity1+'&arr='+arrCity1+'&dep_date='+str(t)+ '&adultCount=1&month_lp=0&tax_incl=1&direct=0&callback=jsonp_orqrdy253dbfulk'
        try:
            soup = getSoup(qunaerUrl)
            a = str(soup)
            a = re.sub(r'jsonp_orqrdy253dbfulk\(', "", a)
            a = re.sub(r'\)', "", a)
            decode_json = json.loads(a)
            data = decode_json['data']
            data = data['banner']
        except:
            continue
        for i in range(7):
            allinfo = data[i]
            fdata = allinfo['depDate']
            price = int(allinfo['price'])
            alist.append(price)
            tmp={
                'fdata':fdata,
                'fprice':price
            }
            blist.append(tmp)
    if len(alist)!=0:
        minPrice = min(alist)
        if minPrice>5000:
            return 0
        tmpstr="去哪儿网查到从"+depCity+"到"+arrCity+"最便宜的价格是"+str(minPrice)+"。这些日期是:"
        tmpList=[]
        for i in blist:
            # print(i)
            if i['fprice']==minPrice:
                if i['fdata'] not in tmpList:
                    tmpList.append(i['fdata'])
        for i in tmpList:
            tmpstr+=i+" "
        file=open("flight.log",'a',encoding='utf-8')
        thisTime=datetime.now()
        file.write(str(thisTime))
        file.write(tmpstr)
        file.write("\n")
        file.close()
        if minPrice<maxPrice:
            print(tmpstr)
            # sendmail('国内机票搜索', tmpstr)

today=datetime.now()
today=today.strftime('%Y-%m-%d')

#定时，循环查找机票
def loopGetTicket(maxPrice):
    for i in depList:
        for j in domestic:
            qunaerGetPrice(maxPrice, i, j, str(today), '2017-10-04')

# print(sys.argv[1])
loopGetTicket(500)
# qunaerGetPrice(400,'厦门','西安','2017-09-30','2017-10-04')
