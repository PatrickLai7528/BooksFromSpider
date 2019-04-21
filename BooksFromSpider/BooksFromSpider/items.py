# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksfromspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    repositoryName = scrapy.Field()
    repositoryURL = scrapy.Field()
    # repositoryDescription = scrapy.Field()
    # repositoryStars = scrapy.Field()
    bookList = scrapy.Field()
    pass
