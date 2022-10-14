
BOT_NAME = 'electronics'

SPIDER_MODULES = ['electronics.spiders']
NEWSPIDER_MODULE = 'electronics.spiders'


ROBOTSTXT_OBEY = False
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}

HTTPERROR_ALLOWED_CODES = [301]
