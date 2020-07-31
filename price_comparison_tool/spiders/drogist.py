# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from price_comparison_tool.items import PriceComparisonToolItem
import csv
import re


class DrogistSpider(Spider):
    name = 'drogist'
    allowed_domains = ['drogist.nl']

    def start_requests(self):
        # get the product urls from the csv file 
        # this spider only gets product urls from store 'drogist'
        # iterate through all the product urls and parse them, get the product data
        
        with open('products.csv', newline='') as file:
            rows = csv.reader(file, delimiter=',')
            for row in rows:
                if row[2] == self.name:
                    yield Request(row[1], 
                                  callback=self.parse,
                                  # passing product_url to parse function
                                  cb_kwargs=dict(product_url=row[1]))

    def parse(self, response, product_url):
        # Initializing the items.
        item = PriceComparisonToolItem()

        # Defining the items.
        item['product_name'] = response.xpath('//h1/text()').get()
        product_price_euro = response.xpath('//*[@class="euro"]//text()').get()
        product_price_cent = response.xpath('//*[@class="cent"]//text()').get()
        item['product_price'] = f'{product_price_euro}{product_price_cent}'

        try:
            if response.xpath('//*[@class="check ab-013-productcurrent"]//text()').get():
                item['product_stock_status'] = True
                product_quantity_note = response.xpath('//*[@class="check ab-013-productcurrent"]//text()').get()
                product_quantity_amount = re.findall(r"(\d+)", product_quantity_note)[0]
                item['product_quantity_note'] = product_quantity_note.strip()
                item['product_stock_amount'] = product_quantity_amount
        except:
            item['product_stock_status'] = False
            item['product_quantity_note'] = ''
            item['product_stock_amount'] = '0'
        
        item['product_brand'] = response.xpath('//*[@itemprop="brand"]/text()').get()
        item['product_EAN'] = response.xpath('//*[@itemprop="productID"]/@content').get().replace("ean:","")
        item['product_store'] = self.name
        item['product_url'] = product_url

        # Yielding the items.
        yield item