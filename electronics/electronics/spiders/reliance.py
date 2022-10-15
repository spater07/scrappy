import scrapy
import re
from urllib.parse import urlencode
from urllib.parse import urljoin
from ..items import ScrapedItems
from ..middlewares import *
import pymongo


class RelianceDigitalSpider(scrapy.Spider):
    name = 'reliance'

    custom_settings = {
	    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.50',
        'DOWNLOADER_MIDDLEWARES' : {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
        },
        'ROBOTSTXT_OBEY': False,
        'BOT_NAME': 'electronics',
        'SPIDER_MODULES': 'electronics.spiders',
        'NEWSPIDER_MODULE': 'electronics.spiders'
    }

    def __init__(self, productName='', productCategory='', outputData = '', **kwargs):
        self.query = productName
        self.category = productCategory
        self.outputData = outputData
        print("<+++++++++++++Reliance+++++++++++++++++>")
        print(self.query)

        super().__init__(**kwargs)


    def start_requests(self):
        url = 'https://www.reliancedigital.in/search?' + urlencode({'q': self.query})
        yield scrapy.Request(
            url=url, 
            callback=self.parse_keyword_response,
            meta = {
                'handle_httpstatus_list': [302]
            }
        )


    def parse_keyword_response(self, response):
        products = response.css('div.sp a::attr(href)').extract()
        productsList=[]

        for href in products:
            productUrl = f"https://www.reliancedigital.in{href}"
            productsList.append(productUrl)

        for i in range(0,len(productsList[0:5])):
            product_url=productsList[i]
            yield scrapy.Request(
                url=product_url, 
                callback=self.parse_product_page
            )


    def parse_product_page(self, response):
        item = ScrapedItems()
        print("<+++++++++++++Reliance+++++++++++++++++>")


        website = 'Reliance-Digital'
        category = self.category
        title = response.css(".mb__20").css("::text").extract_first()
        product_price = response.css(".pdp__offerPrice span+ span").css("::text").extract_first().replace('₹','').replace(',','')

        deals = response.css('.pdp__emiTextStyle , .pdp__featuresBlk div div .p__5 .pdp__listStyle').css("::text").extract()
        
        for offers in deals[:]:
            if offers=="T&C" or offers==". ":
                deals.remove(offers)

                   
        if not product_price:
            product_price = response.css(".a-price-whole::text").extract_first()

        price=float(product_price)

        _class= "com.bestdeals.requestprocessor.models.Product"

        item['productName'] = title
        item['price'] = price
        
        item['category'] = category
        item['websiteName'] = website
        
        item['deals'] = deals

        self.outputData.append(dict(item))

        yield item