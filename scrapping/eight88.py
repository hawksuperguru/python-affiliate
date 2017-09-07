#!/bin/python
# -*- coding: utf-8 -*-

from selenium_browser import UBrowse
from sqlalchemy import create_engine
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import ( Select, WebDriverWait )
from selenium.webdriver.common.keys import Keys

from settings.config import *

import psycopg2
import datetime
import json
import requests
import time
import re

class Eight88(object):
    """docstring for Eight88"""
    def __init__(self):
        self.client = UBrowse()
        self.login_url = 'http://affiliates.888.com/'
        self.report_url = 'https://affiliate.coral.co.uk/reporting/quick_summary_report.asp'
        self.username = 'betfyuk1'
        self.password = 'dontfuckwithme'
        self.items = []
        self.timer = 0

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

    def get_delta_date(self, delta = 1, format_string = "%Y/%m/%d"):
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
        except:
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
        except:
            print("An error occured in parsing page...")
            return False

    def save(self):
        impression = int(self.items[0])
        click = int(self.items[1])
        registration = int(self.items[2])
        lead = int(self.items[3])
        money_player = int(self.items[4])
        balance = float(self.items[5])
        imprwk = int(self.items[6])
        cliwk = int(self.items[7])
        regwk = int(self.items[8])
        leadwk = int(self.items[9])
        mpwk = int(self.items[10])
        imprpre = int(self.items[11])
        clipre = int(self.items[12])
        regpre = int(self.items[13])
        leadpre = int(self.items[14])
        mppre = int(self.items[15])
        imprto = int(self.items[16])
        clito = int(self.items[17])
        regto = int(self.items[18])
        leadto = int(self.items[19])
        mpto = int(self.items[20])
        prebal = int(self.items[21])
        dateto = self.get_delta_date()

        engine = create_engine(get_database_connection_string())
        result = engine.execute("INSERT INTO eight88s (impression, click, registration, lead, money_player, balance, imprwk, cliwk, regwk, leadwk, mpwk, imprpre, clipre, regpre, leadpre, mppre, imprto, clito, regto, leadto, mpto, prebalance, dateto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", impression, click, registration, lead, money_player, balance, imprwk, cliwk, regwk, leadwk, mpwk, imprpre, clipre, regpre, leadpre, mppre, imprto, clito, regto, leadto, mpto, prebal, dateto)

    def run(self):
        self.client.open_url(self.login_url)
        time.sleep(1)

        print("Logging in....")
        if self.login() is True:
            print("Successfully logged in.")
            if self.parse_page() is True:
                self.save()
            else:
                print("Parsing Error...")

        else:
            print("Failed to log in.")

        self.close()


if __name__ == "__main__":
    eight88 = Eight88()
    eight88.run()