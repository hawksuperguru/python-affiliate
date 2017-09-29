#!/bin/python
# -*- coding: utf-8 -*-

from selenium_browser import UBrowse
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import ( Select, WebDriverWait )
from selenium.webdriver.common.keys import Keys
from reporter import SpiderReporter
from app import scheduler
from ..models import Affiliate, History, db
from env import *

import psycopg2
import datetime
import json
import time
import re

class Eight88(object):
    """docstring for Eight88"""
    def __init__(self):
        self.report = SpiderReporter()
        self.login_url = 'http://affiliates.888.com/'
        self.username = 'betfyuk'
        self.password = 'LALB37hUhs'
        self.items = []
        self.timer = 0
        self.affiliate = "Eight88"

        self.headers = {
            'Host': 'secure.activewins.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://secure.activewins.com/reporting/quick_summary_report.asp',
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

    def log(self, message, type = 'info'):
        self.report.write_log("Eight88s", message, self.get_delta_date(), type)

    def report_error_log(self, message):
        self.log(message, "error")

    def get_delta_date(self, delta = DELTA_DAYS, format_string = "%Y/%m/%d"):
        today = datetime.datetime.today()
        diff = datetime.timedelta(days = delta)
        return (today - diff).strftime(format_string)

    def close(self):
        self.client.close()

    def login(self, username = 'betfyuk', password = 'LALB37hUhs'):
        try:
            self.client.driver.find_element_by_class_name("hide-under-480").click()
            WebDriverWait(self.client.driver, 10).until(expected_conditions.frame_to_be_available_and_switch_to_it(self.client.driver.find_element_by_xpath('//iframe[contains(@src, "Auth/Login")]')))
            self.client.driver.find_element_by_id("userName").send_keys("betfyuk")
            self.client.driver.find_element_by_id("password").send_keys("LALB37hUhs")
            self.client.driver.find_element_by_id("btnLogin").click()
            time.sleep(1)
            self._get_cookies()
            return True
        except Exception as e:
            self.report_error_log(str(e))
            return False

    def parse_page(self):
        try:
            self.client.driver.find_element_by_id("rbQuickStatID_This Month (1st - Today)").click()
            bal = self.client.driver.find_element_by_id("this-month").text
            balCents = self.client.driver.find_element_by_id("this-month-cents").text
            netBal = bal + balCents
            prebal = self.client.driver.find_element_by_id("last-month").text
            for summarise in self.client.driver.find_elements_by_xpath('.//span[@class = "summariseTab"]'):
                self.items.append(summarise.text)
            self.items.append(netBal)

            self.client.driver.find_element_by_id("rbQuickStatID_Last 7 Days").click()
            time.sleep(2)
            for summarise in self.client.driver.find_elements_by_xpath('.//span[@class = "summariseTab"]'):
                self.items.append(summarise.text)

            self.client.driver.find_element_by_id("rbQuickStatID_Previous Month").click()
            time.sleep(2)
            for summarise in self.client.driver.find_elements_by_xpath('.//span[@class = "summariseTab"]'):
                self.items.append(summarise.text)

            self.client.driver.find_element_by_id("rbQuickStatID_Today").click()
            time.sleep(2)
            for summarise in self.client.driver.find_elements_by_xpath('.//span[@class = "summariseTab"]'):
                self.items.append(summarise.text)
            self.items.append(prebal)
            return True
        except Exception as e:
            self.report_error_log(str(e))
            return False

    def save(self):
        app = scheduler.app

        try:
            with app.app_context():
                monthly_click = int(self.items[1])
                monthly_signup = int(self.items[2])
                monthly_commission = float(self.items[5])
                
                weekly_click = int(self.items[7])
                weekly_signup = int(self.items[8])
                
                daily_click = int(self.items[17])
                daily_signup = int(self.items[18])

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
                        weekly_click = weekly_click,
                        weekly_signup = weekly_signup,
                        monthly_click = monthly_click,
                        monthly_signup = monthly_signup,
                        monthly_commission = monthly_commission,
                        created_at = created_at
                    )
                    db.session.add(history)
                    db.session.commit()
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
            try:
                affiliate = Affiliate.query.filter_by(name = self.affiliate).first()
                if affiliate is None:
                    return False

                history = History.query.filter_by(affiliate_id = affiliate.id, created_at = created_at).first()
                if history is None:
                    return False
            except Exception as e:
                self.report_error_log(str(e))
                return False
        return True

    def run(self):
        self.log("""
        ======================================================
        ======  Starting 888 Spider  ======================
        """)
        if self.isExisting():
            self.log("Scrapped for `{0}` already done.".format(self.affiliate))
        else:
            self.client = UBrowse()
            self.log("Logging in....")
            self.client.open_url(self.login_url)
            time.sleep(1)
            if self.login() is True:
                self.log("Successfully logged in.")
                if self.parse_page() is True:
                    self.save()
                else:
                    self.log("Parsing Error...")

            else:
                self.report_error_log("Failed to log in.")
            self.close()


if __name__ == "__main__":
    eight88 = Eight88()
    eight88.run()