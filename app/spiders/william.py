from selenium_browser import UBrowse
from reporter import SpiderReporter
from app import scheduler
from ..models import Affiliate, History, db

import dateutil.relativedelta
import datetime
import json
import requests

class William(object):
    """docstring for William"""
    def __init__(self):
        self.client = UBrowse()
        self.ajax_url = 'https://account.affiliates.williamhill.com/affiliates/Reports/dailyFiguresReport'
        self.report = SpiderReporter()
        self.data = {}
        self.affiliate = "William"
        
        self.headers = {
            'Host': 'account.affiliates.williamhill.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json; charset=utf-8',
            'X-Requested-With': 'XMLHttpRequest',
            'x-ms-request-root-id': '7x9tg',
            'x-ms-request-id': '8rW9l',
            'Referer': 'https://account.affiliates.williamhill.com/affiliates/Reports/DailyFigures',
            }

    def _create_params(self, mode = 'daily', date_format = '%d-%m-%Y'):
        one_day = datetime.timedelta(days = 1)
        today = datetime.datetime.now()
        yesterday = today - one_day
        end_date = yesterday.strftime(date_format)

        if mode == 'daily':
            start_date = end_date
        elif mode == 'monthly':
            delta = dateutil.relativedelta.relativedelta(months = 1)
            start_date = (yesterday - delta).strftime(date_format)
        else:
            delta = dateutil.relativedelta.relativedelta(years = 1)
            start_date = (yesterday - delta).strftime(date_format)
        self.params = (
            ('dateFilterFrom', [start_date, start_date]),
            ('dateFilterTo', [end_date, end_date]),
        )

    def _get_cookies(self):
        self.cookies = dict()
        cookies = self.client.driver.get_cookies()
        for i in cookies:
            self.cookies[i['name']] = i['value']

    def get_delta_date(self, delta = 2):
        today = datetime.datetime.today()
        diff = datetime.timedelta(days = delta)
        return (today - diff).strftime("%Y/%m/%d")

    def save(self):
        try:
            app = scheduler.app
            with app.app_context():
                affiliate = Affiliate.query.filter_by(name = self.affiliate).first()
                if affiliate is None:
                    affiliate = Affiliate(name = self.affiliate)
                    db.session.add(affiliate)
                    db.commit()

                history = History.query.filter_by(affiliate_id = affiliate.id, created_at = self.data['created_at']).first()
                if history is None:
                    history = History(
                        affiliate_id = affiliate.id,
                        daily_click = self.data['daily_click'],
                        daily_signup = self.data['daily_signup'],
                        daily_commission = self.data['daily_commission'],
                        monthly_click = self.data['monthly_click'],
                        monthly_signup = self.data['monthly_signup'],
                        monthly_commission = self.data['monthly_commission'],
                        yearly_click = self.data['yearly_click'],
                        yearly_signup = self.data['yearly_signup'],
                        yearly_commission = self.data['yearly_commission'],
                        paid_signup = self.data['paid_signup'],
                        created_at = self.data['created_at']
                    )
                    db.session.add(history)
                    db.session.commit()
            return True
        except:
            self.log("Something went wrong in DB.", "error")
            return False

    def get_ajax_data(self, mode = 'daily'):
        self._create_params(mode)
        response = requests.get(self.ajax_url, headers=self.headers, params=self.params, cookies=self.cookies)
        return response

    def log(self, message, type = 'info'):
        self.report.write_log("William", message, self.get_delta_date(), type)

    def get_daily_data(self):
        response = self.get_ajax_data()
        try:
            response = json.loads(response.content)
            data = response['data'][0]
            self.data['daily_click'] = int(data[3]['Value'])
            self.data['daily_signup'] = int(data[5]['Value'])
            self.data['daily_commission'] = float(data[13]['Value'])
            self.data['paid_signup'] = int(data[10]['Value'])
            self.data['created_at'] = self.get_delta_date()
            return True
        except:
            self.log("Getting daily report failed in william spider.", "error")
            return False

    def get_monthly_data(self):
        response = self.get_ajax_data('monthly')
        try:
            response = json.loads(response.content)
            rows = response['data']
            click = 0
            signup = 0
            commission = 0.0

            for row in rows:
                click += int(row[3]['Value'])
                signup += int(row[5]['Value'])
                commission += float(row[13]['Value'])
            
            self.data['monthly_click'] = click
            self.data['monthly_signup'] = signup
            self.data['monthly_commission'] = commission
            return True

        except:
            self.log("Getting monthly report failed in william spider.", "error")
            return False

    def get_yearly_data(self):
        response = self.get_ajax_data('yearly')
        try:
            response = json.loads(response.content)
            rows = response['data']
            click = 0
            signup = 0
            commission = 0.0

            for row in rows:
                click += int(row[3]['Value'])
                signup += int(row[5]['Value'])
                commission += float(row[13]['Value'])
            
            self.data['yearly_click'] = click
            self.data['yearly_signup'] = signup
            self.data['yearly_commission'] = commission
            return True
        except:
            return False

    def get_data(self):
        return self.get_daily_data() and self.get_monthly_data() and self.get_yearly_data()

    def login(self):
        try:
            self.client.open_url('https://account.affiliates.williamhill.com/affiliates/Account/Login')
            self.client.set_loginform('//*[@id="txtUsername"]')
            self.client.set_passform('//*[@id="txtPassword"]')
            self.client.set_loginbutton('//*[@id="btnLogin"]')

            if self.client.login('betfy.co.uk', 'dontfuckwithme') is True:
                self._get_cookies()
                return True
            else:
                return False
        except:
            return False

    def isExisting(self, date = None):
        if date is None:
            date = self.get_delta_date()
        app = scheduler.app
        with app.app_context():
            affiliate = Affiliate.query.filter_by(name = self.affiliate).first()

            if affiliate is None:
                return False

            history = History.query.filter_by(affiliate_id = affiliate.id, created_at = date).first()

            if history is None:
                return False
            else:
                return True
        
        return True

    def run(self):
        if self.isExisting():
            self.log("Scrapped for `{0}` already done. Skipping...".format(self.affiliate))
        elif self.login():
            if self.get_data():
                if self.save():
                    self.log("Successfully stored to DB.")
                else:
                    self.log("Something went wrong in DB manipulation.", "error")
            else:
                self.log("Failed to get data", "error")
        else:
            self.log("Login Failed in william spider", "error")

        self.client.close()


if __name__ == '__main__':
    me = William()
    me.run()

# Original code:
    # try:
    #     engine = create_engine(get_database_connection_string())
    #     result = engine.execute("INSERT INTO williams (click, signup, commission, monthly_click, monthly_signup, monthly_commission, yearly_click, yearly_signup, yearly_commission, paid_signup, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", self.data['daily_click'], self.data['daily_signup'], self.data['daily_commission'], self.data['monthly_click'], self.data['monthly_signup'], self.data['monthly_commission'], self.data['yearly_click'], self.data['yearly_signup'], self.data['yearly_commission'], self.data['paid_signup'], self.data['created_at'])
    #     return True
    # except:
    #     return False