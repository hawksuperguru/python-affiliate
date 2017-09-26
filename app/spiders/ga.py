# from reporter import *
# from app import scheduler
# from ..models import Affiliate, History, db

# import datetime
# import json
import requests



class GASpider(object):
    """docstring for GASpider"""
    def __init__(self):
        self.affiliate = "Positions"
        self.data = {}
        self.report = SpiderReporter()
        self.url = 'http://staging.betfy.co.uk/wp-json/wp/v2/websites?per_page=14'
        self.affiliates_map = {
            'Real Deal Bet': 'Real',
            'TitanBet App': 'TitanBet',
            'Netbet Mobile App': 'NetBet',
            'Stan James Mobile App': 'StanJames',
            'Betfred Mobile App' : 'BetFred',
            'Paddy Power App': 'Paddy',
            '10Bet' : 'Bet10',
            'Sky Bet App': 'SkyBet',
            '888': 'Eight88',
            'Coral Mobile App': 'Coral',
            'Ladbrokes App': 'LadBrokes',
            'BetVictor Mobile App': 'Victor',
            'William Hill Mobile App': 'William',
            'Bet365': 'Bet365'
        }

    def get_delta_date(self, delta = 2, format_string = "%Y/%m/%d"):
        today = datetime.datetime.today()
        diff = datetime.timedelta(days = delta)
        return (today - diff).strftime(format_string)

    def save(self, affiliate, rate):
        created_at = self.get_delta_date()
        try:
            app = scheduler.app
            with app.app_context():
                affiliate = Affiliate.query.filter_by(affiliate).first()
                if affiliate is None:
                    self.report.write_error_log("Positions", "Affiliate '{0}' not found.".format(affiliate), created_at)
                    return False

                history = History.query.filter_by(affiliate_id = affiliate.id, created_at = created_at).first()
                if history is None:
                    self.report.write_error_log("Positions", "History for '{0}' not found.".format(affiliate), created_at)
                    return False

                history.rate = float(rate)
                db.session.commit()
                return True
        except:
            self.report.write_error_log("Positions", "Something went wrong. ({0}, {1})".format(affiliate, rate), created_at)
            return False


    def run(self):
        r = requests.get(self.url).json()
        for i in r:
            website = i['title']['rendered']
            rating = i['acf']['rating']
            self.save(self.affiliates_map[website], rating)

if __name__ == "__main__":
    me = GASpider()
    me.run()