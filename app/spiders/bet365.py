#!/bin/python
# -*- coding: utf-8 -*-

from selenium_browser import UBrowse
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from reporter import SpiderReporter
from app import scheduler
from ..models import Affiliate, History, db

import psycopg2
import datetime
import json
import time
import re

class Bet365(object):
    """docstring for bet365Spider"""
    def __init__(self):
        self.client = UBrowse()
        self.login_url = 'https://www.bet365affiliates.com/ui/pages/affiliates/Affiliates.aspx'
        self.stats_url = 'https://www.bet365affiliates.com/members/CMSitePages/Router.aspx?TargetPage=Members%2fStatistics&lng=1'
        self.report = SpiderReporter()
        self.affiliate = "Bet365"
        
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

    def get_delta_date(self, delta = 2):
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
                monthly_click = int(self.items[2])
                monthly_signup = int(self.items[3])
                monthly_commission = float(self.items[5])
                yearly_click = int(self.items[8])
                yearly_signup = int(self.items[9])
                yearly_commission = float((self.items[11]).replace(",", ""))
                daily_click = int(self.items[13])
                daily_signup = int(self.items[14])
                daily_commission = float(self.items[16])
                paid_signup = int(self.items[4])
                created_at = self.get_delta_date()

                affiliate = Affiliate.query.filter_by(name = self.affiliate).first()

                if affiliate is None:
                    affiliate = Affiliate(name = self.affiliate)
                    db.session.add(affiliate)
                    db.session.commit()
                    
                history = History.query.filter_by(affiliate_id = affiliate.id, created_at = created_at).first()

                if history is None:
                    history = History(
                        affiliate_id = affiliate.id,
                        daily_click = daily_click,
                        daily_signup = daily_signup,
                        daily_commission = daily_commission,
                        monthly_click = monthly_click,
                        monthly_signup = monthly_signup,
                        monthly_commission = monthly_commission,
                        yearly_click = yearly_click,
                        yearly_signup = yearly_signup,
                        yearly_commission = yearly_commission,
                        paid_signup = paid_signup,
                        created_at = created_at
                    )
                    db.session.add(history)
                    db.session.commit()
                return True
            except:
                self.log("Something went wrong in Saving.", "error")
                return False

    def parse_report_table(self, table_name):
        app = scheduler.app
        with app.app_context():
            try:
                tblWrapper = self.client.driver.find_element_by_class_name('dataTables_scrollBody')
                table = tblWrapper.find_element_by_tag_name('table')
                row = table.find_elements_by_tag_name('tr')[-1]

                pattern = re.compile(r'[\-\d.\d]+')

                monthly_click = int(pattern.search(row.find_elements_by_tag_name('td')[0].text).group(0))
                monthly_signup = int(pattern.search(row.find_elements_by_tag_name('td')[1].text).group(0))
                paid_signup = int(pattern.search(row.find_elements_by_tag_name('td')[9].text).group(0))
                monthly_commission = float(pattern.search(row.find_elements_by_tag_name('td')[-1].text).group(0).replace(',', '.'))
                created_at = self.get_delta_date()

                affiliate = Affiliate.query.filter_by(name = self.affiliate).first()

                if affiliate is None:
                    affiliate = Affiliate(name = self.affiliate)
                    db.session.add(affiliate)
                    db.session.commit()
                    
                history = History.query.filter_by(affiliate_id = affiliate.id, created_at = created_at).first()

                if history is None:
                    history = History(
                        affiliate_id = affiliate.id,
                        monthly_click = monthly_click,
                        monthly_signup = monthly_signup,
                        monthly_commission = monthly_commission,
                        paid_signup = paid_signup,
                        created_at = created_at
                    )
                    db.session.add(history)
                    db.session.commit()

                return True
            except:
                self.log("Exception occured in parse_report_table", "error")
                return False

    def parse_stats(self, wait_for = 10, table_name = "bet365s"):
        # time.sleep(10)
        val = []
        try:
            self.client.open_url(self.stats_url)
            time.sleep(10)
            param_date = self.client.get_delta_date(2, "%d/%m/%Y")

            report_option = Select(self.client.driver.find_element_by_xpath('//*[@id="m_mainPlaceholder_ReportCriteria"]'))
            report_option.select_by_value('dailyReport')
            time.sleep(3)

            self.client.driver.execute_script("document.getElementById('m_mainPlaceholder_FromDate').value = '{0}'".format(param_date))
            time.sleep(3)
            self.client.driver.execute_script("document.getElementById('m_mainPlaceholder_ToDate').value = '{0}'".format(param_date))
            time.sleep(3)
            self.client.driver.find_element_by_id('m_mainPlaceholder_Refresh').click()
            time.sleep(5)

            result = self.parse_report_table(table_name)
            return result
        except:
            self.report_error_log("Exception occured in getting stats...")
            return False

    def login(self, username = 'betfyuk', password = 'passiveincome'):
        self.client.open_url(self.login_url)
        time.sleep(10)
        
        self.client.driver.find_element_by_css_selector("input[name='ctl00$MasterHeaderPlaceHolder$ctl00$userNameTextbox']").send_keys(username)
        tmp_pass = self.client.driver.find_element_by_xpath("//*[@id='ctl00_MasterHeaderPlaceHolder_ctl00_tempPasswordTextbox']")
        tmp_pass.clear()
        self.client.driver.find_element_by_xpath("//*[@id='ctl00_MasterHeaderPlaceHolder_ctl00_passwordTextbox']").send_keys(password)
        self.client.driver.find_element_by_xpath("//*[@id='ctl00_MasterHeaderPlaceHolder_ctl00_passwordTextbox']").send_keys(Keys.RETURN)
        
        return True

    def run(self, provider = 'Bet365', username = 'betfyuk', password = 'passiveincome'):
        self.log("Getting data with (betfyuk:passiveincome)")
        self.affiliate = provider
        if self.login(username, password):
            self.parse_stats()
        else:
            self.log("Failed to Login with 1st account.", "error")
        
        self.client.close()

if __name__ == '__main__':
    bet365 = Bet365()
    bet365.run()