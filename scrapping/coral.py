#!/bin/python
# -*- coding: utf-8 -*-

from selenium_browser import UBrowse
from sqlalchemy import create_engine
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from settings.config import *
from reporter import SpiderReporter

import psycopg2
import datetime
import json
import requests
import time
import re

class Coral(object):
    """docstring for Coral"""
    def __init__(self):
        self.client = UBrowse()
        self.report = SpiderReporter()
        self.login_url = 'https://affiliate.coral.co.uk/login.asp'
        self.report_url = 'https://affiliate.coral.co.uk/reporting/quick_summary_report.asp'
        self.username = 'betfyuk1'
        self.password = 'dontfuckwithme'
        self.items = []
        self.quick_stats_timer = 0
        self.YTD_stats_timer = 0
        self.report_timer = 0

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
        self.report.write_log("Coral", message, type)

    def report_error_log(self, message):
        self.log(message, "error")

    def get_delta_date(self, delta = 1, format_string = "%Y/%m/%d"):
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
            if self.YTD_stats_timer < 8:
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
            if self.quick_stats_timer < 8:
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
            if self.report_timer < 10:
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
        merchant = str(self.items[0])
        impression = int(self.items[1])
        click = int(self.items[2])
        registration = int(self.items[3])
        new_deposit = int(self.items[4])
        commissionStr = str(self.items[5]).replace(',', '')

        pattern = re.compile(r'[\-\d.\d]+')
        commission = float(pattern.search(commissionStr).group(0))
        impreytd = int(self.items[7])
        cliytd = int(self.items[8])
        regytd = int(self.items[9])
        ndytd = int(self.items[10])
        commiytdStr = str(self.items[11]).replace(',', '')
        commiytd = float(pattern.search(commiytdStr).group(0))
        impreto = int(self.items[12])
        clito = int(self.items[13])
        regto = int(self.items[14])
        ndto = int(self.items[15])
        commito = float(self.items[16])
        dateto = datetime.datetime.strptime(self.items[17], '%Y/%m/%d').date()

        engine = create_engine(get_database_connection_string())
        result = engine.execute("INSERT INTO corals (merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regytd, ndytd, commiytd, impreto, clito, regto, ndto, commito, dateto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regytd, ndytd, commiytd, impreto, clito, regto, ndto, commito, dateto)
        return True


if __name__ == "__main__":
    coral = Coral()
    coral.log("Coral Spider is being initialized....")

    if coral.login() is True:
        coral.log("Successfully logged in. Parsing quick stats.")
        coral.get_quick_stats()

        coral.log("pulling YTD stats data...")
        coral.select_YTD_option()
        coral.get_YTD_stats()

        coral.log("Pulling quick stats reporting...")
        coral.get_stats_report()

        if coral.save() == True:
            coral.log("Pulled data successfully saved!")
        else:
            coral.report_error_log("Something went wrong in DB Query.")
    else:
        coral.report_error_log("Failed to log in!!")

    coral.client.close()