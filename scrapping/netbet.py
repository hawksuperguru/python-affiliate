from sqlalchemy import create_engine
from settings.config import *
from selenium_browser import UBrowse
from reporter import *

import psycopg2
import datetime
import json
import requests

class LiveParters(object):
    """docstring for LivePartners"""
    def __init__(self):
        self.report = SpiderReporter()
        self.username = 'betfyuk'
        self.password = 'dontfuckwithme'
        self.data = {}
        self.daily_ajax_url = "https://admin.livepartners.com/stats/quick-stats?start=0&limit=25&format=json&group_by%5B%5D=affiliate_website_id&search_period=yesterday&apikey=5pokw8jnonkexde8beihufmf7cshjsrplpwgasow"
        self.monthly_ajax_url = "https://admin.livepartners.com/stats/quick-stats?start=0&limit=25&format=json&group_by%5B%5D=affiliate_website_id&search_period=last_30_days&apikey=5pokw8jnonkexde8beihufmf7cshjsrplpwgasow"
        self.yearly_ajax_url = "https://admin.livepartners.com/stats/quick-stats?start=0&limit=25&format=json&group_by%5B%5D=affiliate_website_id&search_period=current_year&apikey=5pokw8jnonkexde8beihufmf7cshjsrplpwgasow"

    def get_delta_date(self, delta = 1, format_string = "%Y/%m/%d"):
        today = datetime.datetime.today()
        diff = datetime.timedelta(days = delta)
        return (today - diff).strftime(format_string)

    def get_json(self, url):
        response = requests.post(url)
        r = json.loads(response.content)
        return r['dataset'][0]

    def get_daily_data(self):
        try:
            data = self.get_json(self.daily_ajax_url)
            self.data['click'] = data['clicks_count']
            self.data['signup'] = data['registrations']
            self.data['commission'] = data['commission']
            self.data['paid_signup'] = data['deposits_count']
            self.data['created_at'] = self.get_delta_date()
            return True

        except:
            self.data['click'] = 0
            self.data['signup'] = 0
            self.data['commission'] = 0.0
            self.data['paid_signup'] = 0
            self.data['created_at'] = self.get_delta_date()
            self.report.write_log("Filed to get daily data.", "error")
            return False

    def get_monthly_data(self):
        try:
            data = self.get_json(self.monthly_ajax_url)
            self.data['monthly_click'] = data['clicks_count']
            self.data['monthly_signup'] = data['registrations']
            self.data['monthly_commission'] = data['commission']
            return True
        except:
            self.data['monthly_click'] = 0
            self.data['monthly_signup'] = 0
            self.data['monthly_commission'] = 0.0
            self.report.write_log("Filed to get monthly data.", "error")
            return False

    def get_yearly_data(self):
        try:
            data = self.get_json(self.yearly_ajax_url)
            self.data['yearly_click'] = data['clicks_count']
            self.data['yearly_signup'] = data['registrations']
            self.data['yearly_commission'] = data['commission']
            return True

        except:
            self.data['yearly_click'] = 0
            self.data['yearly_signup'] = 0
            self.data['yearly_commission'] = 0.0
            self.report.write_log("Filed to get yearly data.", "error")
            return False

    def get_data(self):
        return self.get_daily_data() and self.get_monthly_data() and self.get_yearly_data()

    def save(self):
        try:
            engine = create_engine(get_database_connection_string())
            result = engine.execute("INSERT INTO netbets (click, signup, commission, monthly_click, monthly_signup, monthly_commission, yearly_click, yearly_signup, yearly_commission, paid_signup, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", self.data['click'], self.data['signup'], self.data['commission'], self.data['monthly_click'], self.data['monthly_signup'], self.data['monthly_commission'], self.data['yearly_click'], self.data['yearly_signup'], self.data['yearly_commission'], self.data['paid_signup'], self.data['created_at'])
            return True
        except:
            self.report.write_error_log("Failed to write data in Netbet(livepartners_com.py)")
            return False


    def run(self):
        if (self.get_data()):
            return self.save()
        else:
            return False

if __name__ == "__main__":
    netbet = LiveParters()
    netbet.run()

# withdraw_amount = data['withdraw_amount']
# withdraw_count = data['withdraw_count']
# impressions_count = data['impressions_count']
# bonus_bets_amount = data['bonus_bets_amount']
# first_deposits_count = data['first_deposits_count']
# rakes_amount = data['rakes_amount']
# bonus_count = data['bonus_count']
# net_revenue = data['net_revenue']
# downloads_count = data['downloads_count']
# bonus_amount = data['bonus_amount']
# commission = data['commission']
# first_deposits_amount = data['first_deposits_amount']
# bonus_wins_amount = data['bonus_wins_amount']
# deposits_count = data['deposits_count']
# invalid_cpa = data['invalid_cpa']
# gross_revenue = data['gross_revenue']
# valid_cpa = data['valid_cpa']
# affiliate_website_id = data['affiliate_website_id']
# pending_cpa = data['pending_cpa']
# cash_wins_amount = data['cash_wins_amount']
# fees_amount = data['fees_amount']
# clicks_count = data['clicks_count']
# url = data['url']
# deposits_amount = data['deposits_amount']
# registrations = data['registrations']
# cash_bets_amount = data['cash_bets_amount']