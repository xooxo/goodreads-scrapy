# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class GoodreadsBookItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    score = scrapy.Field()
    pages = scrapy.Field()
    year = scrapy.Field()
    genre = scrapy.Field()
    desc = scrapy.Field()
    reviews = scrapy.Field()
    url = scrapy.Field()

