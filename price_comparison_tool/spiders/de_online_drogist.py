# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from price_comparison_tool.items import PriceComparisonToolItem
import csv


class DeOnlineDrogistSpider(Spider):
    name = 'de_online_drogist'
    allowed_domains = ['deonlinedrogist.nl']

    def start_requests(self):
        # get the product urls from the csv file 
        # this spider only gets product urls from store 'de_online_drogist'
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

        product_price = response.xpath('//*[@class="c-singleProduct__price--new"]//text()').getall()
        product_price = ''.join(product_price)
        if ' * ' in product_price:
            product_price = product_price.replace(' * ', '')
            item['product_quantity_note'] = response.xpath('//*[contains(text(), "* Let op!")]/parent::*//text()').getall()
        item['product_price'] = product_price
        
        item['product_brand'] = response.xpath('//*[contains(text(), "Merk:")]/child::*//text()').get()
        
        # to prevent the script from crashing when there is no stock
        try:
            if response.xpath('//*[contains(text(), "Op voorraad:")]'):
                item['product_stock_status'] = True
                item['product_stock_amount'] = response.xpath('//*[contains(text(), "Op voorraad:")]/following-sibling::*/text()').get()
        except:
            item['product_stock_status'] = False
            item['product_stock_amount'] = '0'
        
        item['product_EAN'] = response.xpath('//*[contains(text(), "EAN:")]/text()').get().split(' ')[1]
        item['product_store'] = self.name
        item['product_url'] = product_url

        # Yielding the items.
        yield item

