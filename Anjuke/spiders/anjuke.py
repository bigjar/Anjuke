# -*- coding: utf-8 -*-
import scrapy


class AnjukeSpider (scrapy.Spider):
    name = 'anjuke'
    allowed_domains = ['hangzhou.anjuke.com']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://hangzhou.anjuke.com/sale/'
        yield scrapy.Request (url=url, headers=self.headers)

    page = 1

    def parse(self, response):
        houseList = response.xpath ('//*[@id="houselist-mod-new"]/li')
        for div in houseList:
            item = {}
            houseDetails = div.xpath ('./div[@class="house-details"]')
            commAddress = houseDetails.xpath ('./div[3]/span/@title').extract_first ()

            item['name'] = commAddress.split ()[0]
            item['address'] = commAddress.split ()[1]

            item['roomNum'] = houseDetails.xpath('./div[2]/span[1]/text()').extract_first()
            item['size'] = houseDetails.xpath('./div[2]/span[2]/text()').extract_first()
            item['floor'] = houseDetails.xpath ('./div[2]/span[3]/text()').extract_first ()
            item['builtTime'] = houseDetails.xpath ('./div[2]/span[4]/text()').extract_first ()
            item['publisher'] = houseDetails.xpath ('./div[2]/span[5]/text()').extract_first ()

            proPrice = div.xpath('./div[@class="pro-price"]')
            item['totalPrice'] = proPrice.xpath('./span[@class="price-det"]/strong/text()').extract_first() +\
                                 proPrice.xpath('./span[@class="price-det"]/text()').extract_first()
            item['unitPrice'] = proPrice.xpath('./span[@class="unit-price"]/text()').extract_first()
            yield item

        if self.page <= 50:
            self.page += 1
            next_url = response.xpath('//div[@class="multi-page"]/a[last()]/@href').extract_first()

            yield scrapy.Request(url=next_url,callback=self.parse,dont_filter=True)


