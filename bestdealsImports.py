import ScrapeDeals as srcapeDeals
from flask import Flask, request
from waiting import wait
from mongoconfig import db
from scrapyStatus import ScrapyResponse
from scrapyResponse import Scrapy
from multiprocessing import Process
import time
