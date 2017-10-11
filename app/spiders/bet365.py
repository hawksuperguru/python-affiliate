#!/bin/python
# -*- coding: utf-8 -*-

from selenium_browser import UBrowse
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from reporter import SpiderReporter
from app import scheduler
from ..models import Affiliate, History, db
from env import *

import psycopg2
import datetime
import json
import time
import dateutil.relativedelta
import re

class Bet365(object):
    """docstring for bet365Spider"""
    def __init__(self):
        self.login_url = 'https://www.bet365affiliates.com/ui/pages/affiliates/Affiliates.aspx'
        self.stats_url = 'https://www.bet365affiliates.com/members/CMSitePages/Router.aspx?TargetPage=Members%2fStatistics&lng=1'
        self.report = SpiderReporter()
        self.affiliate = "Bet365"
        self.data = {}
        
        self.headers = {
            'Host': 'www.bet365affiliates.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.bet365affiliates.com/Members/Members/Statistics/',
            }


    def _create_params(self, from_date, to_date, media=False):

        if media:
            self.params = (
                ('key', 'value'),
                )
        else:
            self.params = (
                ('operatorID', '1'),
                )


    def _get_cookies(self):
        self.cookies = dict()
        cookies = self.client.driver.get_cookies()
        for i in cookies:
            self.cookies[i['name']] = i['value']

    def get_delta_date(self, delta = DELTA_DAYS):
        today = datetime.datetime.today()
        diff = datetime.timedelta(days = delta)
        return (today - diff).strftime("%Y/%m/%d")

    def log(self, message, type = 'info'):
        self.report.write_log("Bet365", message, self.get_delta_date(), type)

    def report_error_log(self, message):
        self.log(message, "error")

    def save(self):
        app = scheduler.app
        with app.app_context():
            try:
                created_at = self.get_delta_date()
                affiliate = Affiliate.query.filter_by(name = self.affiliate).first()

                if affiliate is None:
                    affiliate = Affiliate(name = self.affiliate)
                    db.session.add(affiliate)
                    
                history = History.query.filter_by(affiliate_id = affiliate.id, created_at = created_at).first()

                if history is None:
                    history = History(
                        affiliate_id = affiliate.id,
                        created_at = created_at
                    )
                    db.session.add(history)

                history.daily_click = self.data.get('daily_click')
                history.daily_signup = self.data.get('daily_signup')
                history.daily_deposit = self.data.get('daily_deposit')
                history.daily_commission = self.data.get('daily_commission')
                history.weekly_click = self.data.get('weekly_click')
                history.weekly_signup = self.data.get('weekly_signup')
                history.weekly_deposit = self.data.get('weekly_deposit')
                history.weekly_commission = self.data.get('weekly_commission')
                history.monthly_click = self.data.get('monthly_click')
                history.monthly_signup = self.data.get('monthly_signup')
                history.monthly_deposit = self.data.get('monthly_deposit')
                history.monthly_commission = self.data.get('monthly_commission')
                history.yearly_click = self.data.get('yearly_click')
                history.yearly_signup = self.data.get('yearly_signup')
                history.yearly_deposit = self.data.get('yearly_deposit')
                history.yearly_commission = self.data.get('yearly_commission')
                db.session.commit()
                return True
            except Exception as e:
                self.log(str(e), "error")
                return False

    def parse_report_table(self, table_name, mode = 'daily'):
        app = scheduler.app
        try:
            tblWrapper = self.client.driver.find_element_by_class_name('dataTables_scrollBody')
            table = tblWrapper.find_element_by_tag_name('table')
            row = table.find_elements_by_tag_name('tr')[-1]

            pattern = re.compile(r'[\-\d.\d]+')

            if mode == 'daily':
                self.data['daily_click'] = int(pattern.search(row.find_elements_by_tag_name('td')[0].text.replace(',', '')).group(0))
                self.data['daily_signup'] = int(pattern.search(row.find_elements_by_tag_name('td')[1].text.replace(',', '')).group(0))
                self.data['daily_deposit'] = int(pattern.search(row.find_elements_by_tag_name('td')[9].text.replace(',', '')).group(0))
                self.data['daily_commission'] = float(pattern.search(row.find_elements_by_tag_name('td')[-1].text.replace(',', '')).group(0))
            elif mode == 'weekly':
                self.data['weekly_click'] = int(pattern.search(row.find_elements_by_tag_name('td')[0].text.replace(',', '')).group(0))
                self.data['weekly_signup'] = int(pattern.search(row.find_elements_by_tag_name('td')[1].text.replace(',', '')).group(0))
                self.data['weekly_deposit'] = int(pattern.search(row.find_elements_by_tag_name('td')[9].text.replace(',', '')).group(0))
                self.data['weekly_commission'] = float(pattern.search(row.find_elements_by_tag_name('td')[-1].text.replace(',', '')).group(0))
            elif mode == 'monthly':
                self.data['monthly_click'] = int(pattern.search(row.find_elements_by_tag_name('td')[0].text.replace(',', '')).group(0))
                self.data['monthly_signup'] = int(pattern.search(row.find_elements_by_tag_name('td')[1].text.replace(',', '')).group(0))
                self.data['monthly_deposit'] = int(pattern.search(row.find_elements_by_tag_name('td')[9].text.replace(',', '')).group(0))
                self.data['monthly_commission'] = float(pattern.search(row.find_elements_by_tag_name('td')[-1].text.replace(',', '')).group(0))
            elif mode == 'yearly':
                self.data['yearly_click'] = int(pattern.search(row.find_elements_by_tag_name('td')[0].text.replace(',', '')).group(0))
                self.data['yearly_signup'] = int(pattern.search(row.find_elements_by_tag_name('td')[1].text.replace(',', '')).group(0))
                self.data['yearly_deposit'] = int(pattern.search(row.find_elements_by_tag_name('td')[9].text.replace(',', '')).group(0))
                self.data['yearly_commission'] = float(pattern.search(row.find_elements_by_tag_name('td')[-1].text.replace(',', '')).group(0))
            return True
        except Exception as e:
            self.log(str(e), "error")
            return False

    def select_date_range(self, start, end, wait_for = 3):
        report_option = Select(self.client.driver.find_element_by_xpath('//*[@id="m_mainPlaceholder_ReportCriteria"]'))
        report_option.select_by_value('-1')
        time.sleep(1)
        report_option = Select(self.client.driver.find_element_by_xpath('//*[@id="m_mainPlaceholder_ReportCriteria"]'))
        report_option.select_by_value('dailyReport')
        time.sleep(wait_for)
        self.client.driver.execute_script("document.getElementById('m_mainPlaceholder_FromDate').value = '{0}'".format(start))
        time.sleep(wait_for)
        self.client.driver.execute_script("document.getElementById('m_mainPlaceholder_ToDate').value = '{0}'".format(end))
        time.sleep(wait_for)
        self.client.driver.find_element_by_id('m_mainPlaceholder_Refresh').click()
        time.sleep(wait_for)
        pass

    def parse_stats(self, wait_for = 10, table_name = "bet365s"):
        # time.sleep(wait_for)
        val = []
        try:
            self.client.open_url(self.stats_url)
            time.sleep(3)

            today = datetime.datetime.today()
            diff = datetime.timedelta(days = DELTA_DAYS)
            end_date = (today - diff)

            param_date = end_date.strftime("%d/%m/%Y")
            self.select_date_range(param_date, param_date)
            self.parse_report_table(table_name, 'daily')

            delta = dateutil.relativedelta.relativedelta(weeks = 1)
            start_date = end_date - delta
            self.select_date_range(start_date.strftime("%d/%m/%Y"), end_date.strftime("%d/%m/%Y"))
            self.parse_report_table(table_name, 'weekly')

            delta = dateutil.relativedelta.relativedelta(months = 1)
            start_date = end_date - delta
            self.select_date_range(start_date.strftime("%d/%m/%Y"), end_date.strftime("%d/%m/%Y"))
            self.parse_report_table(table_name, 'monthly')

            delta = dateutil.relativedelta.relativedelta(years = 1)
            start_date = end_date - delta
            self.select_date_range(start_date.strftime("%d/%m/%Y"), end_date.strftime("%d/%m/%Y"))
            self.parse_report_table(table_name, 'yearly')

            return self.save()
        except Exception as e:
            self.report_error_log(str(e))
            return False

    def login(self, username = 'betfyuk', password = 'passiveincome'):
        try:
            self.client.open_url(self.login_url)
            time.sleep(1)
            
            self.client.driver.find_element_by_css_selector("input[name='ctl00$MasterHeaderPlaceHolder$ctl00$userNameTextbox']").send_keys(username)
            tmp_pass = self.client.driver.find_element_by_xpath("//*[@id='ctl00_MasterHeaderPlaceHolder_ctl00_tempPasswordTextbox']")
            tmp_pass.clear()
            self.client.driver.find_element_by_xpath("//*[@id='ctl00_MasterHeaderPlaceHolder_ctl00_passwordTextbox']").send_keys(password)
            self.client.driver.find_element_by_xpath("//*[@id='ctl00_MasterHeaderPlaceHolder_ctl00_passwordTextbox']").send_keys(Keys.RETURN)
        
            return True
        except Exception as e:
            self.report_error_log(str(e))
            return False

    def isExisting(self, date = None):
        if date is None:
            date = self.get_delta_date()
        
        app = scheduler.app
        created_at = self.get_delta_date()
        with app.app_context():
            affiliate = Affiliate.query.filter_by(name = self.affiliate).first()
            if affiliate is None:
                return False

            history = History.query.filter_by(affiliate_id = affiliate.id, created_at = created_at).first()
            if history is None:
                return False
        return True

    def run(self, provider = 'Bet365', username = 'betfyuk', password = 'passiveincome'):
        self.log("""
        ======================================================
        ======  Starting Bet 365 Spider  ======================
        """)
        self.log("Getting data with (" + username + ":" + password + ")")
        self.affiliate = provider
        # if self.isExisting():
        #     self.log("Already scraped for {0} at {1}".format(provider, self.get_delta_date()))
        # else:
        self.client = UBrowse()
        if self.login(username, password):
            self.parse_stats()
        else:
            self.log("Failed to Login with current account.", "error")
        
        self.client.close()
        

if __name__ == '__main__':
    bet365 = Bet365()
    bet365.run()