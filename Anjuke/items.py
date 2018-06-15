# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AnjukeItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field() ##小区
    address = scrapy.Field() ##位置
    totalPrice = scrapy.Field() ##总价
    unitPrice = scrapy.Field() ##单价
    size = scrapy.Field() ##大小
    floor = scrapy.Field() ##楼层
    roomNum = scrapy.Field() ##房间数
    buildTime = scrapy.Field() ##建造时间
    publisher = scrapy.Field() ##发布人

