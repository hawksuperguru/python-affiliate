from reporter import *
from app import scheduler
from ..models import Affiliate, db

import psycopg2
import datetime
import json
import requests

class PositionSpider(object):
    """docstring for LivePartners"""
    def __init__(self):
        self.report = SpiderReporter()
        self.affiliate = "Positions"
        self.data = {}
        self.url = 'http://staging.betfy.co.uk/wp-json/wp/v2/websites?per_page=14'

    def get_delta_date(self, delta = 2, format_string = "%Y/%m/%d"):
        today = datetime.datetime.today()
        diff = datetime.timedelta(days = delta)
        return (today - diff).strftime(format_string)

    def get_json(self, url):
        response = requests.post(url)
        r = json.loads(response.content)
        return r['dataset'][0]


    def run(self):
        if (self.get_data()):
            return self.save()
        else:
            return False

if __name__ == "__main__":
    netbet = PositionSpider()
    netbet.run()