from flask import Blueprint

from .. import db
from ..models import Affiliate, History, Log
from reporter import SpiderReporter
from bet10 import Bet10
# from bet365 import Bet365Spider
# from betfred import BetFred

import datetime

class Spider(object):
    """
    Spider class, which will be aggregated daily in order to get data periodically.
    """
    def __init__(self):
        self.report = SpiderReporter()

    def get_delta_date(self, delta = 2, format_string = "%Y/%m/%d"):
        today = datetime.datetime.today()
        diff = datetime.timedelta(days = delta)
        return (today - diff).strftime(format_string)
        
    def log(self, provider, message, type = 'info'):
        self.report.write_log(provider, message, self.get_delta_date(), type)

    def save(self, affiliate, param):
        try:
            if affiliate is None:
                raise ValueError('Affiliate Can\'t be none.')
            
            if param is None:
                raise ValueError('Param Can\'t be none.')

        except:
            aff = Affiliate.query.filter_by(id = affiliate).first()
            self.log(aff.name, "Something went wrong in writting DB", 'error')


    def run(self):
        bet10 = Bet10()
        # bet365 = Bet365Spider()
        # betFred = BetFred()

        spiders = [bet10]

        for spider in spiders:
            try:
                spider.run()
            except:
                self.log(spider.affiliate, "Something went wrong during scraping.", 'error')


if __name__ == "__main__":
    spider = Spider()
    spider.run()