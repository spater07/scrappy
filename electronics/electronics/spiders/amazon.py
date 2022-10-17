import scrapy
from urllib.parse import urlencode
from urllib.parse import urljoin
from ..items import ScrapedItems
from ..middlewares import *

class AmazonSpider(scrapy.Spider):
    name = 'amazon'

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


    def __init__(self, productName='', productCategory='', outputData ='', **kwargs):
        self.query = productName
        self.category = productCategory
        self.outputData = outputData
        # print(self.query)
        super().__init__(**kwargs)


    def start_requests(self):
        url = 'https://www.amazon.in/s?' + urlencode({'k': self.query})
        yield scrapy.Request(
            url=url, 
            callback=self.parse_keyword_response
        )


    def parse_keyword_response(self, response):
        products = response.xpath('//div[contains(@data-component-type,"s-search-result")]/@data-asin').extract()
        productsList=[]

        for i in range(0,len(products[0:4])):
            asin = products[i]
            if(asin!=''):
                productUrl = f"https://www.amazon.in/dp/{asin}"
                productsList.append(productUrl)

        for i in range(0,len(productsList[0:4])):
            product_url=productsList[i]
            yield scrapy.Request(
                url=product_url, 
                callback=self.parse_product_page
            )


    def parse_product_page(self, response):
        item = ScrapedItems()
        print("<+++++++++++++Amazon+++++++++++++++++>")

        website = f'Amazon'
        category = self.category
        title = response.css("#productTitle").css("::text").extract_first().strip()
        product_price = response.css(".apexPriceToPay").css("::text").extract_first()
        imageUrl= response.xpath('//*[@id="imgTagWrapperId"]/img/@src').extract_first()

        deals=response.xpath('//div[contains(@class,"offers-items-content")]/span/span/text()').extract()

        if not deals:
            deals = response.xpath('//*[@class="description"]/text()').extract()        
        
        if not product_price:
            product_price = response.css(".a-price-whole::text").extract_first()

        for letter in product_price:
            if letter == "₹" or ",":
                product_price = product_price.replace('₹','').replace(',','')
        
        price=float(product_price)

        _class= "com.bestdeals.requestprocessor.models.Product"


        item['productName'] = title
        item['price'] = price
        
        item['category'] = category
        item['websiteName'] = website
        
        item['deals'] = deals
        item['imageUrl'] = imageUrl
        item['_class']=_class
        
        self.outputData.append(dict(item))

        # print("<------------Amazon---------->")
        # print(item)
   
        yield item

