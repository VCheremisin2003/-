from lxml import html
from pymongo import MongoClient
import time
from  pprint import pprint
import requests
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
response1 = requests.get('https://lenta.ru/')
dom1 = html.fromstring(response1.text)
news = []

blok1 = dom1.xpath("//div[@class='span4']/div[@class='item']")
for i in blok1:
    a={}
    a['источник'] = 'lenta.ru'
    a['date'] = i.xpath(".//time/@title")
    a['new'] = i.xpath(".//text()")[1]
    a['link'] = i.xpath(".//@href")[0]
    news.append(a)

response2 = requests.get('https://yandex.ru/')
dom2 = html.fromstring(response2.text)

blok2 = dom2.xpath("//ol//li")
day = dom2.xpath("//span[@class='datetime__day']/text()")[0]
month = dom2.xpath("//span[@class='datetime__month']/text()")[0]
for i in blok2:
    a={}
    a['источник'] = 'yandex.ru'
    a['date'] = day + month
    a['new'] = i.xpath(".//text()")[0]
    a['link']= i.xpath(".//@href")[0]
    news.append(a)

response3 = requests.get('https://news.mail.ru/')
dom3 = html.fromstring(response3.text)

blok3 = dom3.xpath("//li[contains(@class, 'list__item')]")
for i in blok3:
    a={}
    a['источник'] = 'mail.ru'
    a['date'] = day + month
    a['new'] = i.xpath(".//text()")
    a['link']= i.xpath(".//@href")
    news.append(a)



client = MongoClient('localhost', 27017)
db = client['news_db']
newcol = db.news
#запишем в нашу бд полученный словарь
for i in news:
    newcol.insert_one(i)
for i in newcol.find({}):
    pprint(i)