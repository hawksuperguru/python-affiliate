from selenium_browser import UBrowse
from reporter import SpiderReporter
from app import scheduler
from ..models import Affiliate, History, db

import psycopg2
import datetime
import json
import requests

class Paddy(object):
    """docstring for Paddy"""
    def __init__(self):
        self.client = UBrowse()
        self.report = SpiderReporter()
        self.affiliate = "Paddy"
        self.headers = {
            'Host': 'affiliates.paddypartners.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json; charset=utf-8',
            'X-Requested-With': 'XMLHttpRequest',
            'x-ms-request-root-id': 'cZ8hr',
            'x-ms-request-id': 'ZK2p+',
            'Referer': 'https://affiliates.paddypartners.com/affiliates/Reports/DailyFigures',
            }

    def _create_params(self, date = None):
        if date is None:
            date = self.get_delta_date(2, '%d-%m-%Y')

        self.params = (
            ('dateFilterFrom', [date, date]),
            ('dateFilterTo', [date, date]),
        )

    def _get_cookies(self):
        self.cookies = dict()
        cookies = self.client.driver.get_cookies()
        for i in cookies:
            self.cookies[i['name']] = i['value']

    def get_delta_date(self, delta = 2, format_string = "%Y/%m/%d"):
        today = datetime.datetime.today()
        diff = datetime.timedelta(days = delta)
        return (today - diff).strftime(format_string)

    def log(self, message, type = "info"):
        self.report.write_log("Paddy", message, self.get_delta_date(), type)

    def get_data(self):
        url = 'https://affiliates.paddypartners.com/affiliates/Reports/dailyFiguresReport'
        response = requests.get(url, headers=self.headers, params=self.params, cookies=self.cookies)
        return response

    def login(self):
        self.client.open_url('https://affiliates.paddypartners.com/affiliates/Account/Login')

        self.client.set_loginform('//*[@id="txtUsername"]')
        self.client.set_passform('//*[@id="txtPassword"]')
        self.client.set_loginbutton('//*[@id="btnLogin"]')

        if self.client.login('betfyuk', 'dontfuckwithme') is True:
            self._get_cookies()
            self._create_params()
        else:
            return False
        return True

    def run(self):
        if self.login():
            response = json.loads(self.get_data().content)
            data = response['data'][0]

            one_day = datetime.timedelta(days = 1)
            yesterday = datetime.datetime.now() - one_day
            date = yesterday.strftime('%Y-%m-%d')
            
            views = data[1]['Value']
            uniqueviews = data[2]['Value']
            clicks = data[3]['Value']
            uniqueclicks = data[4]['Value']
            signups = data[5]['Value']
            depositingcustomers = data[6]['Value']
            activecustomers = data[7]['Value']
            newdepositingcustomers = data[8]['Value']
            newactivecustomers = data[9]['Value']
            firsttimedepositingcustomers = data[10]['Value']
            firsttimeactivecustomers = data[11]['Value']
            netrevenue = data[12]['Value']

            app = scheduler.app
            with app.app_context():
                affiliate = Affiliate.query.filter_by(name = self.affiliate).first()
                if affiliate is None:
                    affiliate = Affiliate(name = self.affiliate)
                    db.session.add(affiliate)
                    db.session.commit()
                
                created_at = self.get_delta_date()
                history = History.query.filter_by(affiliate_id = affiliate.id, created_at = created_at).first()
                if history is None:
                    history = History(
                        affiliate_id = affiliate.id,
                        daily_click = clicks,
                        daily_signup = signups,
                        daily_commission = netrevenue,
                        paid_signup = newdepositingcustomers,
                        created_at = created_at
                    )
                    db.session.add(history)
                    db.session.commit()

            self.client.driver.close()

            # engine = create_engine(get_database_connection_string())
            # result = engine.execute("INSERT INTO paddyies (dateto, views, uniqueviews, clicks, uniqueclicks, signups, depositingcustomers, activecustomers, newdepositingcustomers, newactivecustomers, firsttimedepositingcustomers, firsttimeactivecustomers, netrevenue) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", date, views, uniqueviews, clicks, uniqueclicks, signups, depositingcustomers, activecustomers, newdepositingcustomers, newactivecustomers, firsttimedepositingcustomers, firsttimeactivecustomers, netrevenue)
        pass

if __name__ == '__main__':
    pp = Paddy()
    pp.run()
# response = json.loads(pp.get_data().content)

# data = response['data'][0]

# one_day = datetime.timedelta(days = 1)
# yesterday = datetime.datetime.now() - one_day
# date = yesterday.strftime('%Y-%m-%d')

# views = data[1]['Value']
# uniqueviews = data[2]['Value']
# clicks = data[3]['Value']
# uniqueclicks = data[4]['Value']
# signups = data[5]['Value']
# depositingcustomers = data[6]['Value']
# activecustomers = data[7]['Value']
# newdepositingcustomers = data[8]['Value']
# newactivecustomers = data[9]['Value']
# firsttimedepositingcustomers = data[10]['Value']
# firsttimeactivecustomers = data[11]['Value']
# netrevenue = data[12]['Value']

# pp.client.driver.close()

# engine = create_engine(get_database_connection_string())
# result = engine.execute("INSERT INTO paddyies (dateto, views, uniqueviews, clicks, uniqueclicks, signups, depositingcustomers, activecustomers, newdepositingcustomers, newactivecustomers, firsttimedepositingcustomers, firsttimeactivecustomers, netrevenue) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", date, views, uniqueviews, clicks, uniqueclicks, signups, depositingcustomers, activecustomers, newdepositingcustomers, newactivecustomers, firsttimedepositingcustomers, firsttimeactivecustomers, netrevenue)

