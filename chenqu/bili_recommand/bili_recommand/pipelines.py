# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class BiliRecommandPipeline(object):
    def process_item(self, item, spider):
        return item


class SqlitePipeline:
    def __init__(self):
        self.connection = sqlite3.connect("bilircm.sqlite")
        self.cursor = self.connection.cursor()
        self.cursor.execute("create table if not exists bili_rcm(title varchar, url varchar)")
        self.connection.commit()

    def process_item(self, item, spider):
        self.cursor.execute("insert into bili_rcm (title, url) values (?, ?)", (item['title'], item['url']))
        self.connection.commit()
        return item

    def __del__(self):
        self.connection.close()
