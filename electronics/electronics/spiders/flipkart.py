import scrapy
from urllib.parse import urlencode
from urllib.parse import urljoin
from ..items import ScrapedItems
from scrapy.crawler import CrawlerProcess
from ..middlewares import *
from ..settings import HTTPERROR_ALLOWED_CODES

class FlipkartSpider(scrapy.Spider):
    name = 'flipkartSpy'
    
    custom_settings = {
        'USER_AGENT':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.50',
        'DOWNLOADER_MIDDLEWARES' : {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
        },
        'ROBOTSTXT_OBEY': False,
        'BOT_NAME' : 'electronics',
        'SPIDER_MODULES' : 'electronics.spiders',
        'NEWSPIDER_MODULE' : 'electronics.spiders',
        }

    def __init__(self, productName='', productCategory='',outputData = '', **kwargs):
        self.query=productName
        self.category=productCategory
        self.outputData = outputData
        super().__init__( **kwargs)

    def start_requests(self):
        url = 'https://flipkart.com/search?' + urlencode({'q': self.query})
        yield scrapy.Request(
            url=url, 
            callback=self.parse_keyword_response,
            meta = {
                'handle_httpstatus_list': [302]
            }
        )

    def parse_keyword_response(self, response):
        products = response.xpath('//*[@data-id]')
        productsList=[]
        for product in products:           
            fsn = product.xpath('@data-id').extract_first()
            productUrl= f"https://flipkart.com/product/p/itme?pid={fsn}"         
            productsList.append(productUrl)

        for i in range(0,len(productsList[0:5])):
            product_url=productsList[i]
            yield scrapy.Request(
                url=product_url, 
                callback=self.parse_product_page
            )

    def parse_product_page(self, response):
        
        item=ScrapedItems()

        website=f'Flipkart'
        category=self.category
        title=response.css(".B_NuCI").css("::text").extract_first()
        product_price=response.css("._16Jk6d").css("::text").extract_first().replace('₹','').replace(',','')
        deals=response.css(".u8dYXW+ span").css("::text").extract()
        imageUrl=response.xpath('//*[@id="container"]/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[2]/img/@src').extract_first()
        
        price=float(product_price)

        _class= "com.bestdeals.requestprocessor.models.Product"
        
        item['productName'] = title
        item['price'] = price
        
        item['category'] = category
        item['websiteName'] = website
        
        item['deals'] = deals
        item['imageUrl'] = imageUrl
        item['_class'] = _class

        self.outputData.append(dict(item))
        
        yield item