from flask import Flask, request

from scrapy.signalmanager import dispatcher
from scrapy.crawler import CrawlerRunner
from scrapy import signals

from electronics.electronics.spiders.reliance import RelianceDigitalSpider
from electronics.electronics.spiders.flipkart import FlipkartSpider
from electronics.electronics.spiders.amazon import AmazonSpider

import crochet
import threading
