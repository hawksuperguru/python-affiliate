from selenium_browser import UBrowse
from reporter import *
from app import scheduler
from ..models import Affiliate, History, db

import psycopg2
import datetime
import dateutil.relativedelta
import json
import requests
import time

class LadBrokes(object):
    """docstring for LadBrokes"""
    def __init__(self):
        self.report = SpiderReporter()
        self.report_url = 'https://portal.ladbrokespartners.com/portal/#/statistics'
        self.ajax_url = 'https://portal.ladbrokespartners.com/portal/rest/reports/run/atOnce'
        self.data = {}
        self.affiliate = "LadBrokes"
        
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Length': '9167',
            'Content-Type': 'application/json;charset=utf-8',
            'Host': 'portal.ladbrokespartners.com',
            'Referer': 'https://portal.ladbrokespartners.com/portal/',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
            }

    def get_delta_date(self, delta = 2, format_string = "%Y/%m/%d"):
        today = datetime.datetime.today()
        diff = datetime.timedelta(days = delta)
        return (today - diff).strftime(format_string)

    def _create_params(self, mode = 'daily'):
        delta = datetime.timedelta(days = 1)
        today = datetime.datetime.now()
        yesterday = today - delta
        end_date = yesterday.strftime('%Y-%m-%d')
        start_date = yesterday.strftime('%Y-%m-%d')

        if mode == 'monthly':
            delta = dateutil.relativedelta.relativedelta(months = 1)
            start_date = (yesterday - delta).strftime('%Y-%m-%d')
        elif mode == 'yearly':
            delta = dateutil.relativedelta.relativedelta(years = 1)
            start_date = (yesterday - delta).strftime('%Y-%m-%d')

        self.ajax_param = '{"report":{"campaignId":"245450","input":[{"name":"startDate","label":"Stat Date","type":"dateRange","required":true,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":"yyyy-MM-dd","jsDateTimeFormat":"yy-MM-dd","precision":3,"value":"custom","values":[],"sublist":[{"name":"startDate_list","label":null,"type":"list","required":true,"collapsed":false,"filter":true,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":null,"value":"today","values":[{"id":"custom","name":null},{"id":"today","name":null},{"id":"yesterday","name":null},{"id":"currweek","name":null},{"id":"prevweek","name":null},{"id":"currmonth","name":null},{"id":"prevmonth","name":null},{"id":"threemonths","name":null},{"id":"sixmonths","name":null},{"id":"curryear","name":null},{"id":"prevyear","name":null}],"sublist":[]},{"name":"startDate_from","label":null,"type":"date","required":true,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":"yyyy-MM-dd","jsDateTimeFormat":"yy-MM-dd","precision":null,"value":"%s","values":[],"sublist":[]},{"name":"startDate_to","label":null,"type":"date","required":true,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":"yyyy-MM-dd","jsDateTimeFormat":"yy-MM-dd","precision":null,"value":"%s","values":[],"sublist":[]}]},{"name":"profile","label":"Profile","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"reportBy1","label":"Report By","type":"list","required":true,"collapsed":false,"filter":true,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":"stat_date","values":[{"id":"stat_date","name":"Date"},{"id":"stat_month","name":"Month"},{"id":"profile","name":"Profile"},{"id":"product","name":"Product"},{"id":"banner","name":"Banner"},{"id":"platform","name":"Platform"},{"id":"country","name":"Country"},{"id":"var1","name":"Var 1"},{"id":"var2","name":"Var 2"},{"id":"var9","name":"Var 9"},{"id":"var10","name":"Var 10"}],"sublist":[]},{"name":"reportBy2","label":"Report By","type":"list","required":false,"collapsed":false,"filter":true,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[{"id":"stat_date","name":"Date"},{"id":"stat_month","name":"Month"},{"id":"profile","name":"Profile"},{"id":"product","name":"Product"},{"id":"banner","name":"Banner"},{"id":"platform","name":"Platform"},{"id":"country","name":"Country"},{"id":"var1","name":"Var 1"},{"id":"var2","name":"Var 2"},{"id":"var9","name":"Var 9"},{"id":"var10","name":"Var 10"}],"sublist":[]},{"name":"reportBy3","label":"Report By","type":"list","required":false,"collapsed":false,"filter":true,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[{"id":"stat_date","name":"Date"},{"id":"stat_month","name":"Month"},{"id":"profile","name":"Profile"},{"id":"product","name":"Product"},{"id":"banner","name":"Banner"},{"id":"platform","name":"Platform"},{"id":"country","name":"Country"},{"id":"var1","name":"Var 1"},{"id":"var2","name":"Var 2"},{"id":"var9","name":"Var 9"},{"id":"var10","name":"Var 10"}],"sublist":[]},{"name":"reportBy4","label":"Report By","type":"list","required":false,"collapsed":false,"filter":true,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[{"id":"stat_date","name":"Date"},{"id":"stat_month","name":"Month"},{"id":"profile","name":"Profile"},{"id":"product","name":"Product"},{"id":"banner","name":"Banner"},{"id":"platform","name":"Platform"},{"id":"country","name":"Country"},{"id":"var1","name":"Var 1"},{"id":"var2","name":"Var 2"},{"id":"var9","name":"Var 9"},{"id":"var10","name":"Var 10"}],"sublist":[]}],"output":[{"name":"stat_date","label":"Date","type":"date","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":"yyyy-MM-dd","jsDateTimeFormat":"yy-MM-dd","precision":3,"value":null,"values":[],"sublist":[]},{"name":"stat_month","label":"Month","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"platform","label":"Platform","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"profile","label":"Profile","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"product","label":"Product","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"banner","label":"Banner","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"country","label":"Country","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"var1","label":"Var 1","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"var2","label":"Var 2","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"var9","label":"Var 9","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"var10","label":"Var 10","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"REAL_IMPS","label":"Unique Impressions","type":"long","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"RAW_IMPS","label":"Non-Unique Impressions","type":"long","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"REAL_CLICKS","label":"Unique Clicks","type":"long","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"RAW_CLICKS","label":"Non-Unique Clicks","type":"long","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"sports_signups","label":"sports Signups Cnt","type":"long","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"sports_acquired_count","label":"sports Acquired cnt","type":"long","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"acquired_count","label":"Acquired cnt","type":"long","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"WITHDRAWS_CNT","label":"Withdrawal cnt","type":"long","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"sports_net_gaming_revenue","label":"Sports Net Gaming Revenue","type":"number","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"cpa_commission","label":"CPA Commission","type":"number","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"ng_commission","label":"Net Gaming Commission","type":"number","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"tlr_amount","label":"Top Level Revenue","type":"number","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]}],"language":"EN","name":"trafficStatsNew","id":"1712"},"sc":{"offset":0,"limit":1000,"order":[{"ascending":true,"column":"1"}],"namedQuery":""}}'%(start_date, end_date)


    def _get_auth_token(self):
        try:
            self.headers['X-Auth-Token'] = self.client.driver.execute_script("return localStorage.authToken")
        except:
            return False
        return True

    def _get_cookies(self):
        self.cookies = dict()
        cookies = self.client.driver.get_cookies()
        for i in cookies:
            self.cookies[i['name']] = i['value']
    
    def log(self, message, type = 'info'):
        self.report.write_log("LadBroke", message, self.get_delta_date(), type)

    def get_yearly_data(self):
        self._create_params('yearly')
        response = requests.post(self.ajax_url, headers=self.headers, cookies=self.cookies, data=self.ajax_param)
        content = response.content
        response = json.loads(content)

        if (response['data']['total']['data']):
            values = response['data']['total']['data']
            self.data['yearly_click'] = int(values[3])
            self.data['yearly_signup'] = int(values[5])
            self.data['yearly_commission'] = float(values[10])
            return True

        else:
            self.log("Something went wrong in Ajax for Yearly data", 'error')
            return False
        
    def get_monthly_data(self):
        self._create_params('monthly')
        response = requests.post(self.ajax_url, headers=self.headers, cookies=self.cookies, data=self.ajax_param)
        content = response.content
        response = json.loads(content)

        if (response['data']['total']['data']):
            values = response['data']['total']['data']
            self.data['monthly_click'] = int(values[3])
            self.data['monthly_signup'] = int(values[5])
            self.data['monthly_commission'] = float(values[10])
            return True

        else:
            self.log("Something went wrong in Ajax for Monthly data", 'error')
            return False

    def get_daily_data(self):
        self.client.open_url(self.report_url)
        time.sleep(2)
        response = requests.post(self.ajax_url, headers=self.headers, cookies=self.cookies, data=self.ajax_param)
        content = response.content
        response = json.loads(content)

        if (response['data']['total']['data']):
            values = response['data']['total']['data']
            self.data['created_at'] = self.get_delta_date()
            self.data['daily_click'] = int(values[3])
            self.data['daily_signup'] = int(values[5])
            self.data['daily_commission'] = float(values[10])
            self.data['paid_signup'] = 0
            return True

        else:
            self.log("Something went wrong in Ajax for Daily data", 'error')
            return False

    def get_data(self):
        time.sleep(5)
        self._get_auth_token()
        self.log("Getting daily data...")
        self.get_daily_data()
        self.log("Getting monthly data...")
        self.get_monthly_data()
        self.log("Getting yearly data...")
        self.get_yearly_data()
        return self.save()

    def save(self):
        try:
            app = scheduler.app
            with app.app_context():
                affiliate = Affiliate.query.filter_by(name = self.affiliate).first()

                if affiliate is None:
                    affiliate = Affiliate(name = self.affiliate)
                    db.session.add(affiliate)
                    db.session.commit()

                print(affiliate)
                created_at = self.get_delta_date()

                history = History.query.filter_by(affiliate_id = affiliate.id, created_at = created_at).first()

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
                        created_at = created_at
                    )
                    db.session.add(history)
                    db.session.commit()
            return True
        except Exception as e:
            self.log(str(e), "error")
            return False

    def isExisting(self, date = None):
        if date == None:
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
        if self.isExisting() is False:
            self.client = UBrowse()
            self.client.open_url('https://portal.ladbrokespartners.com/portal/#/login')
            self.client.set_loginform('//*[@id="userName"]')
            self.client.set_passform('//*[@id="password"]')
            self.client.set_loginbutton('/html/body/div[3]/section/div/form/div[5]/div/input')

            if self.client.login('betfyuk', 'WjewEEUV') is True:
                self._get_cookies()
                self._create_params()

                if self.get_data():
                    self.log("Data stored successfully")
                else:
                    self.log("Failed to write to DB")
            else:
                self.log("Login Failed", 'error')
            self.client.close()

        else:
            self.log("Already scrapped for `{0}`. Skipping...".format(self.affiliate))


if __name__ == '__main__':
    lb = LadBrokes()
    lb.run()