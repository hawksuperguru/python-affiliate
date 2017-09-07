from selenium_browser import UBrowse
# from flaskapp import Eight88
from sqlalchemy import create_engine

import psycopg2
import datetime
import json
import requests

class Affil(object):
    """docstring for Affil"""
    def __init__(self):
        self.client = UBrowse()
        
        self.headers = {
            'Host': 'program.uffiliates.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://program.uffiliates.com/en/reports/trafficstats',
            }


    def _create_params(self, from_date, to_date, media=False):

        if media:
            self.params = (
                ('operatorID', '1'),
                ('brandID', '-1'),
                ('mediaTypeId', '-1'),
                ('langId', '-1'),
                ('sizeId', '-1'),
                ('toDate', '%sT00:00:00Z'%to_date),
                ('fromDate', '%sT00:00:00Z'%from_date),
                ('_search', 'false'),
                ('rows', '50'),
                ('page', '1'),
                ('sidx', ''),
                ('sord', 'desc'),
                )
        else:
            self.params = (
                ('operatorID', '1'),
                ('brandID', '-1'),
                ('trackingCode', '-1'),
                ('toDate', '%sT00:00:00Z'%to_date),
                ('fromDate', '%sT00:00:00Z'%from_date),
                ('isGrouping', 'false'),
                ('isFilterFirstTime', 'true'),
                ('isWithAnid', 'false'),
                ('isShowCountry', 'false'),
                ('isShowDevice', 'false'),
                ('_search', 'false'),
                ('rows', '50'),
                ('page', '1'),
                ('sidx', ''),
                ('sord', 'asc'),
                )

    def _get_cookies(self):
        self.cookies = dict()
        cookies = self.client.driver.get_cookies()
        for i in cookies:
            self.cookies[i['name']] = i['value']

    def get_data(self, week=None, this_month=None, pre_month=None, year=None, media=False):
        date_now = datetime.datetime.now()
        from_date = date_now.strftime('%Y-%m-%d')
        to_date = date_now.strftime('%Y-%m-%d')

        if week:
            time_delta = datetime.timedelta(days = 7)
            from_date = (date_now - time_delta).strftime('%Y-%m-%d')
        if this_month:
            from_date = date_now.strftime('%Y-%m-01')
        if pre_month:
            time_delta = datetime.timedelta(days=date_now.day)
            last_date_pre_month = date_now - time_delta
            from_date = last_date_pre_month.strftime('%Y-%m-01')
            to_date = last_date_pre_month.strftime('%Y-%m-%d')
        if year:
            from_date = datetime.datetime(date_now.year, 1, 1).strftime('%Y-%m-%d')

        
        if media:
            self._create_params(from_date, to_date, media=True)
            url = 'https://program.uffiliates.com/en/Reports/GetMediaStatsReport'
        else:
            self._create_params(from_date, to_date)
            url = 'https://program.uffiliates.com/en/Reports/GetTrafficStatsReport'

        response = requests.get(url, headers=self.headers, params=self.params, cookies=self.cookies)
        return response

    def get_media_data(self, week=None, this_month=None, pre_month=None, year=None):
        date_now = datetime.datetime.now()
        from_date = date_now.strftime('%Y-%m-%d')
        to_date = date_now.strftime('%Y-%m-%d')

        if week:
            time_delta = datetime.timedelta(days = 7)
            from_date = (date_now - time_delta).strftime('%Y-%m-%d')
        if this_month:
            from_date = date_now.strftime('%Y-%m-01')
        if pre_month:
            time_delta = datetime.timedelta(days=date_now.day)
            last_date_pre_month = date_now - time_delta
            from_date = last_date_pre_month.strftime('%Y-%m-01')
            to_date = last_date_pre_month.strftime('%Y-%m-%d')
        if year:
            from_date = datetime.datetime(date_now.year, 1, 1).strftime('%Y-%m-%d')

        self._create_params(from_date, to_date)
        url = 'https://program.uffiliates.com/en/Reports/GetMediaStatsReport'
        response = requests.get(url, headers=self.headers, params=self.params, cookies=self.cookies)
        return response

    def run(self):
        self.client.open_url('https://program.uffiliates.com/en/Auth/Login')
        self.client.set_loginform('//*[@id="userName"]')
        self.client.set_passform('//*[@id="password"]')
        self.client.set_loginbutton('//*[@id="btnLogin"]')

        if self.client.login('betfyuk', 'LALB37hUhs') is True:
            self._get_cookies()

        return True

if __name__ == '__main__':

    affil = Affil()
    affil.run()
    data_to = json.loads(affil.get_data().content)
    data_week = json.loads(affil.get_data(week=True).content)
    data_this_month = json.loads(affil.get_data(this_month=True).content)
    data_pre_month = json.loads(affil.get_data(pre_month=True).content)
    data_year = json.loads(affil.get_data(year=True).content)

    mediadata_to = json.loads(affil.get_data(media=True).content)
    mediadata_week = json.loads(affil.get_data(week=True, media=True).content)
    mediadata_this_month = json.loads(affil.get_data(this_month=True, media=True).content)
    mediadata_pre_month = json.loads(affil.get_data(pre_month=True, media=True).content)
    mediadata_year = json.loads(affil.get_data(year=True, media=True).content)

    # affil.client.driver.close()
    affil.client.close()

    userdata_to = data_to['userdata']
    userdata_week = data_week['userdata']
    userdata_this_month = data_this_month['userdata']
    userdata_pre_month = data_pre_month['userdata']
    userdata_year = data_year['userdata']


    impression = sum([i['Impressions'] for i in mediadata_this_month['result']])
    click = sum([i['Clicks'] for i in mediadata_this_month['result']])
    registration = userdata_this_month['Registrations']
    lead = userdata_this_month['Leads']
    money_player = userdata_this_month['MoneyPlayers']

    balance = userdata_this_month['CommissionPerformance']
    
    imprwk = sum([i['Impressions'] for i in mediadata_week['result']])
    cliwk = sum([i['Clicks'] for i in mediadata_week['result']])
    regwk = userdata_week['Registrations']
    leadwk = userdata_week['Leads']
    mpwk = userdata_week['MoneyPlayers']
    
    imprpre = sum([i['Impressions'] for i in mediadata_pre_month['result']])
    clipre = sum([i['Clicks'] for i in mediadata_pre_month['result']])
    regpre = userdata_pre_month['Registrations']
    leadpre = userdata_pre_month['Leads']
    mppre = userdata_pre_month['MoneyPlayers']
    
    imprto = sum([i['Impressions'] for i in mediadata_pre_month['result']])
    clito = sum([i['Clicks'] for i in mediadata_pre_month['result']])
    regto = userdata_pre_month['Registrations']
    leadto = userdata_pre_month['Leads']
    mpto = userdata_pre_month['MoneyPlayers']

    prebal = userdata_pre_month['CommissionPerformance']


    engine = create_engine('postgresql://postgres:root@localhost/kyan')
    # engine = create_engine('mysql+pymysql://root:@localhost/kyan')
    print ("INSERT INTO eight88s (impression, click, registration, lead, money_player, balance, imprwk, cliwk, regwk, leadwk, mpwk, imprpre, clipre, regpre, leadpre, mppre, imprto, clito, regto, leadto, mpto, prebalance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", impression, click, registration, lead, money_player, balance, imprwk, cliwk, regwk, leadwk, mpwk, imprpre, clipre, regpre, leadpre, mppre, imprto, clito, regto, leadto, mpto, prebal)
    # result = engine.execute("INSERT INTO eight88s (impression, click, registration, lead, money_player, balance, imprwk, cliwk, regwk, leadwk, mpwk, imprpre, clipre, regpre, leadpre, mppre, imprto, clito, regto, leadto, mpto, prebalance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", impression, click, registration, lead, money_player, balance, imprwk, cliwk, regwk, leadwk, mpwk, imprpre, clipre, regpre, leadpre, mppre, imprto, clito, regto, leadto, mpto, prebal)
