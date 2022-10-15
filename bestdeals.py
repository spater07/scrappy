from bestdealsImports import *

app = Flask(__name__)

@app.route("/scrape-data", methods=['GET'])
def scrape():
    args=request.args
    product_name=args.get('productName')
    product_category=args.get('productCategory')

    outputData = []
    scrape = srcapeDeals.ScrapeDeals(product_name=product_name , product_category=product_category,outputData = outputData)

    scrape.scrape_amazon(product_name=product_name , product_category=product_category,outputData = outputData)
    scrape.scrape_flipkart(product_name=product_name , product_category=product_category,outputData = outputData)
    scrape.scrape_reliance(product_name=product_name , product_category=product_category,outputData = outputData)

    
    # # # # scrape_amazon(product_name=product_name , product_category=product_category) 
    # t1=Process(target=scrape.scrape_amazon, args=(product_name, product_category, outputData))
    # t1.start()
    # t2=Process(target=scrape.scrape_flipkart, args=(product_name, product_category, outputData))
    # t2.start()
    # t3=Process(target=scrape.scrape_reliance, args=(product_name, product_category, outputData))
    # # time.sleep(20)
    
    # t3.start()
    # # time.sleep(20)
    # t1.join()
    # t2.join()
    # t3.join()
    time.sleep(20)

    time.sleep(5)
    if len(outputData)==0:
        returned_product = Scrapy(product_name, ScrapyResponse.SCRAPPING_FAILURE.name) 
    else:
        i=0
        while(i<len(outputData)):
            filter_dict = {"productName":outputData[i]['productName']}
            if db.electronics.count_documents(filter_dict):
                i += 1
            else:
                db.Product.insert_one(outputData[i])
                i += 1

        returned_product = Scrapy(product_name, ScrapyResponse.SCRAPPING_COMPLETE.name)
    
    return (returned_product.__dict__)


if __name__ == "__main__":
    app.run(debug=True)
