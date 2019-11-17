from lxml import etree
from random import randint
import requests
import pymongo
import csv
import time


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
cookie = 'acw_tc=7abe401c15738180375014074ed882b3c717a0558c7681e6cca3eb186d; sid=bf1e2210-02e0-4375-988f-0217af0e6724; cookieId=9ff6709a-03e6-45b6-9521-234baad4fc55; qchatid=35331ec5-aa7f-4f38-9489-589d2157c77d; language=SIMPLIFIED; CITY_NAME=SHENZHEN; WINDOW_DEVICE_PIXEL_RATIO=1; _ga=GA1.3.209829688.1573818042; JSESSIONID=aaaBxHU5qLxyAbhLOlQ5w; Hm_lvt_4d7fad96f5f1077431b1e8d8d8b0f1ab=1573818042,1573975164; _gid=GA1.3.414381323.1573975165; Hm_lvt_de678bd934b065f76f05705d4e7b662c=1573818042,1573975165; sec_tc=AQAAAK0h+gzwTAQAt11ztErmoagLVzDA; acw_sc__v2=5dd1145698473db1727413acac5bd4489efcc362; _dc_gtm_UA-47416713-1=1; Hm_lpvt_4d7fad96f5f1077431b1e8d8d8b0f1ab=1573983333; Hm_lpvt_de678bd934b065f76f05705d4e7b662c=1573983334'
pre_url = 'https://shenzhen.qfang.com/sale/f'
# host = '127.0.0.1'
# port = 27017
dbname = 'qfang'
docname = 'info'

client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
db = client[dbname]
col = db[docname]


def cookie_dict(cookie: str) -> dict:
    cookies = {}
    for k_v in cookie.split(';'):
        k, v = k_v.split('=', 1)
        cookies[k.strip()] = v
    return cookies


def download(url):
    html = requests.get(url, headers=headers, cookies=cookie_dict(cookie))
    time.sleep(randint(3, 7))
    return etree.HTML(html.content.decode())


def data_save_csv(item):
    with open('qfang.csv', mode='a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(item)


def insert_dict(item: list) -> dict:
    item_dict = {'apartment': item[0],
                 'houselayout': item[1],
                 'area': item[2],
                 'region': item[3],
                 'totalprice': item[4]}
    return item_dict


def spider(url):
    selector = download(url)
    house_list = selector.xpath("/html/body/div[5]/div/div[1]/div[4]/ul/li")
    for house in house_list:
        apartment = house.xpath("div[2]/div[1]/a/text()")[0]
        houselayout = house.xpath("div[2]/div[2]/p[1]/text()")[0]
        area = house.xpath("div[2]/div[2]/p[2]/text()")[0]
        region = house.xpath("div[2]/div[3]/div[1]/a[1]/text()")[0]
        totalprice = house.xpath("div[3]/p[1]/span[1]/text()")[0]
        item = [apartment, houselayout, area, region, totalprice]
        print(insert_dict(item))
        col.insert_one(insert_dict(item))
        data_save_csv(item)


if __name__ == '__main__':
    for i in range(1, 11):
        spider(pre_url + str(i))
