# 简易基本爬虫之爬取二手房信息

## Content

<!-- TOC -->

- [简易基本爬虫之爬取二手房信息](#简易基本爬虫之爬取二手房信息)
    - [Content](#content)
    - [简介](#简介)
    - [文件内容](#文件内容)
    - [运行须知](#运行须知)

<!-- /TOC -->

## 简介

- Python专选课上机任务之二, 使用`lxml`, `requests`编写简易爬虫爬取二手房信息, 同时将爬取结果写入csv文件和MongoDB数据库
- 开发环境: `Python 3.8.0`
- 系统环境: `Arch Linux`

## 文件内容

- [qfang_spider.py](./qfang_spider.py): 目标网址: [https://shenzhen.qfang.com/sale](https://shenzhen.qfang.com/sale), 该网站有防爬虫机制, 需要配置`headers`和`cookies`, 而且应避免短时间内密集运行
- [qfang.csv](./qfang.csv): 为以上程序的爬取结果
- [spider2.py](./spider2.py): 目标网址: [https://bj.5i5j.com/ershoufang/](https://bj.5i5j.com/ershoufang/), 只需要设置`headers`即可正常运行
- [spider2.csv](./spider2.csv): 为以上程序的爬取结果

## 运行须知

- 运行时需要保持MongoDB的开启
