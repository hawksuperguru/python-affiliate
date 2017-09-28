#!/bin/python
# -*- coding: utf-8 -*-

from selenium_browser import UBrowse
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from reporter import *
from app import scheduler
from ..models import Affiliate, History, db

import datetime
import json
import requests
import time
import re

class RealDealBet(object):
    """docstring for RealDealBet"""
    def __init__(self):
        self.report = SpiderReporter()
        self.client = UBrowse()
        self.login_url = 'https://partners.realdealbet.com/login.asp'
        self.report_url = 'https://partners.realdealbet.com/reporting/quick_summary_report.asp'
        self.username = 'id_betfyuk'
        self.password = 'dontfuckwithme'
        self.items = []
        self.quick_stats_timer = 0
        self.YTD_stats_timer = 0
        self.report_timer = 0
        self.affiliate = "Real"

        self.headers = {
            'Host': 'partners.realdealbet.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://partners.realdealbet.com/reporting/quick_summary_report.asp',
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

    def get_delta_date(self, delta = 2, format_string = "%Y/%m/%d"):
        today = datetime.datetime.today()
        diff = datetime.timedelta(days = delta)
        return (today - diff).strftime(format_string)

    def login(self):
        self.client.open_url(self.login_url)
        time.sleep(3)
        self.client.set_loginform('//*[@id="username"]')
        self.client.set_passform('//*[@id="password"]')
        self.client.set_loginbutton('//button[@type="submit"]')

        if self.client.login(self.username, self.password) is True:
            self._get_cookies()
            return True
        else:
            return False

    def log(self, message, type = 'info'):
        self.report.write_log("Real", message, self.get_delta_date(), type)

    def select_YTD_option(self):
        try:
            period_select = Select(self.client.driver.find_element_by_xpath('//*[@id="dashboard"]//select[@name="WRQSperiod"]'))
            period_select.select_by_value('YTD')
            return True
        except:
            return False

    def get_YTD_stats(self):
        time.sleep(5)
        try:
            table = self.client.driver.find_element_by_xpath('//*[@id="dashboard_quick_stats"]//tr[@class="row_light_color"]')
            for td in table.find_elements_by_tag_name('td'):
                if td.text == u'':
                    raise ValueError("Value can't be empty.")
                    break
                self.items.append(td.text)
            return True

        except:
            self.log("Element not found.")
            self.YTD_stats_timer += 1
            if self.YTD_stats_timer < 10:
                return self.get_YTD_stats()
            else:
                return False

    def get_quick_stats(self):
        time.sleep(5)
        try:
            table = self.client.driver.find_element_by_xpath('//*[@id="dashboard_quick_stats"]//tr[@class="row_light_color"]')
            for td in table.find_elements_by_tag_name('td'):
                if td.text == u'':
                    raise ValueError("Value can't be empty.")
                    break
                self.items.append(td.text)
            return True
            
        except:
            self.log("Element not found.")
            self.quick_stats_timer += 1
            if self.quick_stats_timer < 6:
                return self.get_quick_stats()
            else:
                return False

    def parse_stats_report(self):
        time.sleep(3)
        param_date = self.get_delta_date()
        try:
            # tableDiv = Betfred.find_element_by_id("internalreportdata")
            table = self.client.driver.find_element_by_xpath('//*[@id="internalreportdata"]/table')
            # table = tableDiv.find_element_by_tag_name("table")
            todayVal = table.find_elements_by_tag_name("tr")

            pattern = re.compile(r'[\-\d.\d]+')
            impreto = pattern.search(todayVal[1].text).group(0)
            self.items.append(impreto)
            clito = pattern.search(todayVal[2].text).group(0)
            self.items.append(clito)
            regto = pattern.search(todayVal[5].text).group(0)
            self.items.append(regto)
            ndto = pattern.search(todayVal[8].text).group(0)
            self.items.append(ndto)
            commito = pattern.search(todayVal[-1].text).group(0)
            self.items.append(commito)
            self.items.append(param_date)
            return True

        except:
            self.log("Element not found.")
            self.report_timer += 1
            if self.report_timer < 4:
                return self.parse_stats_report()
            else:
                return False

    def get_stats_report(self):
        self.client.open_url(self.report_url)
        time.sleep(10)
        merchant = Select(self.client.driver.find_element_by_xpath('//form[@id="FRMReportoptions"]//select[@name="merchantid"]'))
        merchant.select_by_value('0')
        param_date = self.get_delta_date()
        self.client.driver.execute_script("document.getElementById('startdate').value = '{0}'".format(param_date))
        self.client.driver.execute_script("document.getElementById('enddate').value = '{0}'".format(param_date))
        self.client.driver.find_element_by_class_name("button").click()
        self.parse_stats_report()

    def save(self):
        try:
            pattern = re.compile(r'[\-\d.\d]+')
            monthly_click = int(self.items[2])
            monthly_signup = int(self.items[3])
            paid_signup = int(self.items[4])
            commissionStr = str(self.items[5]).replace(',', '')
            monthly_commission = float(pattern.search(commissionStr).group(0))

            yearly_click = int(self.items[8])
            yearly_signup = int(self.items[9])
            commiytdStr = str(self.items[11]).replace(',', '')
            yearly_commission = float(pattern.search(commiytdStr).group(0))
            
            daily_click = int(self.items[13])
            daily_signup = int(self.items[14])
            daily_commission = float(self.items[16])
            
            created_at = self.get_delta_date()
            
            app = scheduler.app
            with app.app_context():
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
            self.log("Something went wrong in writing DB.", "error")
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
            self.log("Successfully logged in. Parsing quick stats.")
            self.get_quick_stats()
            self.select_YTD_option()
            self.get_YTD_stats()

            self.log("Pulling quick stats reporting...")
            self.get_stats_report()

            if self.save() == True:
                self.log("Pulled data successfully saved!")
            else:
                self.log("Something went wrong in DB Query.", "error")
        else:
            self.log("Failed to log in!!", "error")

        self.client.close()


if __name__ == "__main__":
    me = RealDealBet()
    me.run()