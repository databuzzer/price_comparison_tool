# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PriceComparisonToolItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_name = scrapy.Field()
    product_price = scrapy.Field()
    product_stock_status = scrapy.Field()
    product_stock_amount = scrapy.Field()
    product_quantity_note = scrapy.Field()
    product_EAN = scrapy.Field()
    product_brand = scrapy.Field()
    product_store = scrapy.Field()
    product_url = scrapy.Field()
