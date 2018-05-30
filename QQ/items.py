# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QqItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class QQ_MessageBoardItem(scrapy.Item):
    floor = scrapy.Field()
    id = scrapy.Field()
    secret = scrapy.Field()
    pasterid = scrapy.Field()
    bmp = scrapy.Field()
    pubtime = scrapy.Field()
    modifytime = scrapy.Field()
    effect = scrapy.Field()
    type = scrapy.Field()
    uin = scrapy.Field()
    nickname = scrapy.Field()
    capacity = scrapy.Field()
    htmlContent = scrapy.Field()
    ubbContent = scrapy.Field()
    signature = scrapy.Field()
    # replyList = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    nick = scrapy.Field()
