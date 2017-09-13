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

class Bet10(object):
    """docstring for Bet10"""
    def __init__(self):
        self.client = UBrowse()
        self.login_url = 'https://partners.10bet.com/login.asp'
        self.report_url = 'https://partners.10bet.com/reporting/quick_summary_report.asp'
        self.username = 'betfyuk'
        self.password = 'dontfuckwithme'
        self.timer = 0
        self.items = []
        self.report = SpiderReporter()
        
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

    def close(self):
        self.client.close()

    def get_page(self, url, timer = 10):
        self.client.open_url(url)
        time.sleep(timer)

    def log(self, message, type = 'info'):
        self.report.write_log("Bet10", message, self.get_delta_date(), type)

    def report_error_log(self, message):
        self.log(message, "error")

    def login(self):
        self.client.set_loginform('//*[@id="username"]')
        self.client.set_passform('//*[@id="password"]')
        self.client.set_loginbutton('//button[@type="submit"]')

        if self.client.login(self.username, self.password) is True:
            self._get_cookies()
            return True
        else:
            self.report_error_log("Failed to log in.")
            return False

    def extract_table_values(self):
        time.sleep(3)
        try:
            for tr in self.client.driver.find_elements_by_xpath('//table[@id="dashboard_quick_stats"]//tr[@class="row_light_color"]'):
                for td in tr.find_elements_by_tag_name('td'):
                    if td.text == '':
                        raise ValueError("Element Not found. Trying later...")
                    self.items.append(td.text)
        except:
            if (self.timer < 10):
                return self.extract_table_values()
            else:
                self.report_error_log("Failed to get table values")
                return False

    def parse_stats_tables(self):
        self.timer = 0
        self.extract_table_values()
        select = Select(self.client.driver.find_element_by_xpath('//*[@id="dashboard"]//select[@name="WRQSperiod"]'))
        select.select_by_value('YTD')
        
        self.timer = 0
        self.extract_table_values()

    def get_delta_date(self, delta = 2):
        today = datetime.datetime.today()
        diff = datetime.timedelta(days = delta)
        return (today - diff).strftime("%Y/%m/%d")

    def set_params_for_daily_report(self):
        time.sleep(3)
        try:
            merchant = Select(self.client.driver.find_element_by_xpath('//form[@id="FRMReportoptions"]//select[@name="merchantid"]'))
            paramDate = self.get_delta_date()
            self.client.driver.execute_script("document.getElementById('startdate').value = '{0}'".format(paramDate))
            self.client.driver.execute_script("document.getElementById('enddate').value = '{0}'".format(paramDate))
            merchant.select_by_value('0')
            self.client.driver.find_element_by_class_name("button").click()
        except:
            self.report_error_log("Failed to set params for daily report.")

    def parse_daily_data(self):
        self.timer = 0
        self.set_params_for_daily_report()

        temp_array = []
        for tr in self.client.driver.find_elements_by_xpath('//*[@id="internalreportdata"]//tr'):
            for td in tr.find_elements_by_tag_name('td'):
                temp_array.append(td.text)
        
        pattern = re.compile(r'[\-\d.\d]+')
        self.items.append(pattern.search(temp_array[1]).group(0))
        self.items.append(pattern.search(temp_array[2]).group(0))
        self.items.append(pattern.search(temp_array[4]).group(0))
        self.items.append(pattern.search(temp_array[7]).group(0))
        self.items.append(pattern.search(temp_array[-1]).group(0))

    def save(self):
        merchant = str(self.items[0])
        impression = int(self.items[1])
        click = int(self.items[2])
        registration = int(self.items[3])
        new_deposit = int(self.items[4])
        commission = float(self.items[5])
        impreytd = int(self.items[7])
        cliytd = int(self.items[8])
        regytd = int(self.items[9])
        ndytd = int(self.items[10])
        commiytd = float((self.items[11]).replace(",", ""))
        impreto = int(self.items[12])
        clito = int(self.items[13])
        regto = int(self.items[14])
        ndto = int(self.items[15])
        commito = float(self.items[16])
        dateto = datetime.datetime.strptime(self.get_delta_date(), '%Y/%m/%d').date()

        engine = create_engine(get_database_connection_string())
        result = engine.execute("INSERT INTO bet10s (merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regytd, ndytd, commiytd, impreto, clito, regto, ndto, commito, dateto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regytd, ndytd, commiytd, impreto, clito, regto, ndto, commito, dateto)
        
        return result

    def parse(self):
        self.log('getting page...')
        self.get_page(self.login_url, 5)

        self.log('getting pass the gate page...')
        # time.sleep(5)
        self.login()

        self.log('getting quick stats table...')
        self.parse_stats_tables()

        self.log('getting summary page content')
        self.get_page(self.report_url, 1)
        self.parse_daily_data()

        self.log("Saving to Database...")
        self.save()
        self.close()


# Run spider
if __name__ == '__main__':
    bet10 = Bet10()
    items_list = bet10.parse()