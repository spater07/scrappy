import scrapy

class ScrapedItems(scrapy.Item):
    websiteName=scrapy.Field()
    productName = scrapy.Field()
    price=scrapy.Field()
    category=scrapy.Field()
    deals=scrapy.Field()
    imageUrl=scrapy.Field()
    _class=scrapy.Field()

