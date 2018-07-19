# -*- encoding:utf-8 -*-
from urllib import request,parse
import re
from bs4 import BeautifulSoup
import json
from datetime import datetime,date

#出发地
depList=['厦门','上海','广州','福州','深圳']

#目的地(东南亚)
arrList=['新加坡', '吉隆坡', '槟城', '怡保', '曼谷', '清迈', '普吉岛', '古晋', '雅加达', '巴里岛', '棉兰', '泗水', '仰光', '河内', '金边', '西贡', '永珍', '马尼拉', '宿雾', '阿皮亚', '达卡', '诗邬', '塞班', '新得里', '喀布尔', '吉大港', '喀拉蚩', '东加大埔', '孟买', '科伦坡', '加尔各答', '马德拉斯' ]

def getSoup(url, charset="utf-8"):
    req = request.Request(url)
    content = request.urlopen(req).read().decode(charset, 'ignore')
    soup = BeautifulSoup(content, "html.parser")
    return soup

#https://sijipiao.fliggy.com/search/common_cheapest_calendar.htm?_ksTS=1505207356915_2265&callback=jsonp2266&searchBy=1355&depCity=SHA&arrCity=TYO&searchDay=2017-10-08&agentId=&calType=SevendayCalendar&origDepDate=2017-10-10&origRetDate=
#https://sijipiao.fliggy.com/search/common_cheapest_calendar.htm?_ksTS=1505285342396_2251&callback=jsonp2252&searchBy=1251&depCity=SHA&arrCity=TYO&searchDay=2017-10-05&agentId=&calType=SevendayCalendar&origDepDate=2017-10-08&origRetDate=
# 飞猪网针对国际的（国内到国际，国际到国内，国际到国际)
def feizhuGetPrice(maxPrice,depCity,arrCity):
    depCity1 = ""
    arrCity1 = ""
    f = open("code.txt", 'r', encoding='utf-8')
    for line in f.readlines():
        alist = (str(line)).split(":")
        if alist[0] == depCity:
            depCity1=(alist[1]).strip()
        if alist[0] == arrCity:
            arrCity1=(alist[1]).strip()
    f.close()
    if arrCity1 == "":
        print("目的地"+arrCity+"找不到，你咋不上天呢")
        return 0
    if depCity1=="":
        print("出发地"+depCity+"找不到，你咋不上天呢")
        return 0
    # print("======================开始查找从 <"+depCity+"> 到 <"+arrCity+"> 的最便宜机票============================================")
    alist=[]
    blist=[]
    for j in 10, 11, 12:
        for t in '01', '05', 10, 13, 15, 20, 28:
            url = 'https://sijipiao.fliggy.com/search/common_cheapest_calendar.htm?_ksTS=1505207356915_2265&callback=jsonp2266&searchBy=1355&depCity='+depCity1+'&arrCity='+arrCity1+'&searchDay=2017-' + str(
                j) + '-' + str(t) + '&agentId=&calType=SevendayCalendar&origDepDate=2017-10-10&origRetDate='
            try:
                soup = getSoup(url)
                a = str(soup)
                a = re.sub(r'jsonp2266\(', "", a)
                a = re.sub(r'\)', "", a)
                decode_json = json.loads(a)
                data = decode_json['data']
            except:
                continue
            for i in range(7):
                allinfo = data[i]
                fdata = allinfo['fDate']
                furl="https://" + (allinfo['url'])[2:]
                price = int(allinfo['price']) + int(allinfo['tax'])
                if price == -2:
                    continue
                alist.append(price)
                tmp={
                    'fdata':fdata,
                    'furl':furl,
                    'fprice':price
                }
                blist.append(tmp)
    if len(alist)!=0:
        minPrice = min(alist)
        tmpstr="飞猪网查到从"+depCity+"到"+arrCity+"最便宜的价格是"+str(minPrice)+"。这些日期是:"
        tmpList=[]
        for i in blist:
            if i['fprice']==minPrice:
                if i['fdata'] not in tmpList:
                    tmpList.append(i['fdata'])
        for i in tmpList:
            tmpstr+=i+" "
        print(tmpstr)
        if minPrice<maxPrice:
            print("快，飞猪网找到c从"+depCity+"到"+arrCity+"你要的机票了，赶紧买啊++++++++++++++++++++++++")

# 去哪儿网
#qunaerUrl = 'https://lp.flight.qunar.com/api/lp_calendar?dep=%E5%8E%A6%E9%97%A8&arr=%E6%96%B0%E5%8A%A0%E5%9D%A1&dep_date=2017-11-06&adultCount=1&month_lp=0&tax_incl=1&direct=0&callback=jsonp_orqrdy253dbfulk'
def qunaerGetPrice(maxPrice,depCity,arrCity):
    depCity1=parse.quote(depCity)
    arrCity1=parse.quote(arrCity)
    alist=[]
    blist=[]
    for j in 10, 11, 12:
        for t in '01', '05', 10, 13, 15, 20, 28:
            qunaerUrl = 'https://lp.flight.qunar.com/api/lp_calendar?dep='+depCity1+'&arr='+arrCity1+'&dep_date=2017-' + str(
                j) + '-' + str(t) + '&adultCount=1&month_lp=0&tax_incl=1&direct=0&callback=jsonp_orqrdy253dbfulk'
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
            if i['fprice']==minPrice:
                if i['fdata'] not in tmpList:
                    tmpList.append(i['fdata'])
        for i in tmpList:
            tmpstr+=i+" "
        print(tmpstr)
        if minPrice<maxPrice:
            print("快，去哪儿网找到c从"+depCity+"到"+arrCity+"你要的机票了，赶紧买啊++++++++++++++++++++++++")

#定时，循环查找机票
def loopGetTicket(maxPrice):
    for i in depList:
        for j in arrList:
            feizhuGetPrice(maxPrice,i,j)
            qunaerGetPrice(maxPrice,i,j)

if __name__ == '__main__':
    print("-------------欢迎来到特价飞机票搜索程序：---------------")
    flag = 0
    while flag == 0:
        promot = "=====================\n" \
                 "请输入您要选择的功能:\n" \
                 "1：查询特价机票\n" \
                 "2：查找东南亚的几个地方\n" \
                 "3：退出\n" \
                 "=====================\n"
        choice = input(promot)
        if choice == "1":
            maxprice = int(input("请输入最大能接受的票价:"))
            depCity = input("请输入出发地:")
            arrCity = input("请输入目的地:")
            feizhuGetPrice(depCity,arrCity)
            qunaerGetPrice(depCity,arrCity)
        if choice == "2":
            loopGetTicket(300)
            exit(0)
        if choice == "3":
            flag += 1