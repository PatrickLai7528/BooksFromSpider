# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BooksfromspiderPipeline(object):

    def process_item(self, item, spider):
        file = open("result.txt", "a+")
        file.write("倉庫名稱：" + item["repositoryName"] + "\n")
        file.write("倉庫連結：" + item["repositoryName"] + "\n")
        for book in item["bookList"]:
            file.write("　　書本名稱：" + book["name"] + "\n")
            file.write("　　書本連結：" + book["url"] + "\n")
        return item
