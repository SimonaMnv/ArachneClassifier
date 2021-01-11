# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    body = scrapy.Field()
    tags = scrapy.Field()
    author = scrapy.Field()
    link = scrapy.Field()
    type = scrapy.Field()
    scope = scrapy.Field()
