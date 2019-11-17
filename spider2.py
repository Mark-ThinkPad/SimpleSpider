from lxml import etree
from random import randint
import requests
import pymongo
import csv
import time


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
pre_url = 'https://bj.5i5j.com/ershoufang/n'
cookie = ''
# host = '127.0.0.1'
# port = 27017
dbname = 'spider2'
docname = 'info'
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
db = client[dbname]
col = db[docname]


# def cookie_dict(cookie: str) -> dict:
#     cookies = {}
#     for k_v in cookie.split(';'):
#         k, v = k_v.split('=', 1)
#         cookies[k.strip()] = v
#     return cookies


def download(url):
    html = requests.get(url, headers=headers)
    time.sleep(randint(3, 7))
    return etree.HTML(html.content.decode())


def data_save_csv(item):
    with open('spider2.csv', mode='a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(item)


def insert_dict(item: list) -> dict:
    item_dict = {'apartment': item[0],
                 'house_layout': item[1],
                 'area': item[2],
                 'direction': item[3],
                 'floor': item[4],
                 'decoration': item[5],
                 'build_time': item[6],
                 'region': item[7],
                 'community': item[8],
                 'traffic': item[9],
                 'unit_price': item[10],
                 'total_price': item[11]}
    return item_dict


def mess_spilt(mess: str) -> tuple:
    spilt_over = mess.split('·')
    house_layout = spilt_over[0]
    area = spilt_over[1]
    direction = spilt_over[2]
    floor = spilt_over[3]
    decoration = spilt_over[4]
    build_time = spilt_over[5]

    return house_layout, area, direction, floor, decoration, build_time


def spider(url):
    selector = download(url)
    house_list = selector.xpath('/html/body/div[5]/div[1]/div[2]/ul/li')
    for house in house_list:
        try:
            apartment = house.xpath('div[2]/h3/a/text()')[0]
            mess_info = house.xpath('div[2]/div[1]/p[1]/text()')[0]
            mess_info = mess_info.replace(' ', '')
            house_layout, area, direction, floor, decoration, build_time = mess_spilt(mess_info)
            region = house.xpath('div[2]/div[1]/p[2]/text()[1]')[0]
            region = region.replace(' ', '')
            community = house.xpath('div[2]/div[1]/p[2]/a[1]/text()')[0]
            traffic = house.xpath('div[2]/div[1]/p[2]/a[2]/text()')[0]
            unit_price = house.xpath('div[2]/div[1]/div/p[2]/text()')[0]
            total_price = house.xpath('div[2]/div[1]/div/p[1]/strong/text()')[0]
            item = [apartment, house_layout, area, direction, floor, decoration, build_time, region, community, traffic, unit_price, total_price]
            col.insert_one(insert_dict(item))
            data_save_csv(item)
        except IndexError:
            continue


if __name__ == '__main__':
    for i in range(1, 6):
        spider(pre_url + str(i))
