# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


class AnjukePipeline (object):
    def open_spider(self, spider):

        self.conn = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="anjuke",
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor )
        self.cursor = self.conn.cursor()
        self.cursor.execute("drop table if exists houseinfo")

        createsql = """create table houseinfo(name VARCHAR(32) NOT NULL,
                  address VARCHAR(32) NOT NULL,
                  totalPrice VARCHAR(32) NOT NULL,
                  unitPrice VARCHAR(32) NOT NULL,
                  size VARCHAR(32) NOT NULL,
                  floor VARCHAR(32) NOT NULL,
                  roomNum VARCHAR(32) NOT NULL,
                  buildTime VARCHAR(32) NOT NULL,
                  publisher VARCHAR(32) NOT NULL,
                  area varchar(8) not null)"""
        self.cursor.execute(createsql)

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        item['totalPrice'] = item['totalPrice'].split('万')[0]
        item['unitPrice'] = item['unitPrice'].split('元')[0]
        item['builtTime'] = item['builtTime'].split('年')[0]
        item['size'] = item['size'].split('m')[0]
        area = item['address'].split('-')[0]
        insertsql = 'insert into houseinfo(name, address,totalPrice, unitPrice, size, floor, roomNum, \
                        buildTime, publisher,area) \
                        VALUES ("%s", "%s","%s", "%s","%s", "%s","%s", "%s","%s","%s")' % \
                        (item['name'], item['address'], item['totalPrice'], item['unitPrice'], item['size'], item['floor'], item['roomNum'], item['builtTime'], item['publisher'],area)
        try:
            self.cursor.execute(insertsql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)


        return item
