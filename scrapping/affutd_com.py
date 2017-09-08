from selenium_browser import UBrowse
from sqlalchemy import create_engine
from settings.config import *

import psycopg2
import datetime
import json
import requests

class Affutd(object):
    """docstring for Affutd"""
    def __init__(self):
        self.client = UBrowse()
        
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

    def _create_params(self):
        one_day = datetime.timedelta(days = 1)
        day_now = datetime.datetime.now()
        yesterday = day_now - one_day
        date = yesterday.strftime('%d-%m-%Y')

        self.params = (
            ('dateFilterFrom', [date, date]),
            ('dateFilterTo', [date, date]),
        )

    def _get_cookies(self):
        self.cookies = dict()
        cookies = self.client.driver.get_cookies()
        for i in cookies:
            self.cookies[i['name']] = i['value']

    def get_data(self):
        url = 'https://account.affiliates.williamhill.com/affiliates/Reports/dailyFiguresReport'
        response = requests.get(url, headers=self.headers, params=self.params, cookies=self.cookies)
        return response

    def run(self):
        self.client.open_url('https://account.affiliates.williamhill.com/affiliates/Account/Login')
        self.client.set_loginform('//*[@id="txtUsername"]')
        self.client.set_passform('//*[@id="txtPassword"]')
        self.client.set_loginbutton('//*[@id="btnLogin"]')

        if self.client.login('betfy.co.uk', 'dontfuckwithme') is True:
            self._get_cookies()
            self._create_params()

        return True


if __name__ == '__main__':
    affud = Affutd()
    affud.run()

    response = json.loads(affud.get_data().content)
    data = response['data'][0]

    affud.client.driver.close()

    for i in data:
        if i.['Key'] = 'Views':
            views = i.['Value']

        if i.['Key'] = 'UniqueViews':
            unique_views = i.['Value']
            
        if i.['Key'] = 'Clicks':
            clicks = i.['Value']
            
        if i.['Key'] = 'UniqueClicks':
            unique_clicks = i.['Value']
            
        if i.['Key'] = 'Signups':
            signups = i.['Value']
            
        if i.['Key'] = 'DepositingCustomers':
            depositing_customers = i.['Value']
            
        if i.['Key'] = 'ActiveCustomers':
            active_customers = i.['Value']
            
        if i.['Key'] = 'Adj(Chargebacks)':
            chargebacks = i.['Value']
            
        if i.['Key'] = 'NetRevenue':
            net_revenue = i.['Value']


    engine = create_engine(get_database_connection_string())
    result = engine.execute("INSERT INTO williams (views, unique_views, clicks, unique_clicks, signups, depositing_customers, active_customers, chargebacks, net_revenue) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);", views, unique_views, clicks, unique_clicks, signups, depositing_customers, active_customers, chargebacks, net_revenue)
