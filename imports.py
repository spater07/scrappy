from flask import Flask, request
import json
from flask_pymongo import PyMongo
import pymongo
import time
from waiting import wait
import asyncio

from scrapy.signalmanager import dispatcher
from scrapy.crawler import CrawlerRunner
from scrapy import signals

from electronics.electronics.spiders.reliance import RelianceDigitalSpider
from electronics.electronics.spiders.flipkart import FlipkartSpider
from electronics.electronics.spiders.amazon import AmazonSpider
from mongoconfig import db

from scrapyStatus import ScrapyResponse
from scrapyResponse import Scrapy
import crochet
import threading
from multiprocessing import Process
