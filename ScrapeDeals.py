from imports import *

crochet.setup()
crawl_runner = CrawlerRunner()

class ScrapeDeals():  

    def __init__(self, product_name, product_category, outputData):
        self.product_name = product_name
        self.product_category = product_category
        self.outputData = outputData

    def scrape_amazon(self,product_name,product_category,outputData):

        eventual = crawl_runner.crawl(
            AmazonSpider, 
            productName=product_name, 
            productCategory=product_category,
            outputData = outputData 
        )
        return eventual

    def scrape_flipkart(self,product_name,product_category,outputData):

        eventual = crawl_runner.crawl(
            FlipkartSpider, 
            productName=product_name, 
            productCategory=product_category,
            outputData = outputData 
        )
        return eventual

    def scrape_reliance(self,product_name,product_category,outputData):

        eventual = crawl_runner.crawl(
            RelianceDigitalSpider, 
            productName=product_name, 
            productCategory=product_category,
            outputData = outputData 
        )
        return eventual

    