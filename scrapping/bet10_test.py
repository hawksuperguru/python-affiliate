#!/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait, Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
from sqlalchemy import create_engine
import psycopg2, time
import os, datetime, re

class Bet10Spider():
    def __init__(self):
        self.url_to_crawl = 'http://partners.10bet.com/'
        self.summary_url = 'https://partners.10bet.com/reporting/quick_summary_report.asp'
        self.table_values = []
        self.items = []

    def start_driver(self):
        print('starting driver...')
        # self.display = Display(visible=0, size=(800, 600))
        # self.display.start()
        # self.driver = webdriver.Chrome("/usr/bin/chromedriver")
        self.driver = webdriver.Chrome("../chrome/chromedriver.exe")

    def close_driver(self):
        print('closing driver...')
        # self.display.stop()
        self.driver.quit()
        print('closed!')

    def get_page(self, url):
        print('getting page...')
        self.driver.get(url)
        time.sleep(10)

    def login(self):
        print('getting pass the gate page...')
        try:
            form = self.driver.find_element_by_id('FMlogins')
            form.find_element_by_id('username').send_keys('betfyuk')
            form.find_element_by_id('password').send_keys('dontfuckwithme')
            form.find_element_by_id('password').send_keys(Keys.RETURN)
            # form.find_element_by_xpath('//button[@class="btn btn-primary btn-lg", @type="submit"]').click()
            time.sleep(10)
        except Exception:
            print("Exception found in login process...")
            pass

    def extract_table_values(self):
        print('Extracting row_light_color record values...')
        for tr in self.driver.find_elements_by_xpath('//table[@id="dashboard_quick_stats"]//tr[@class="row_light_color"]'):
            for td in tr.find_elements_by_tag_name('td'):
                self.table_values.append(td.text)

    def parse_stats_tables(self):
        self.extract_table_values()
        select = Select(self.driver.find_element_by_xpath('//*[@id="dashboard"]//select[@name="WRQSperiod"]'))
        select.select_by_value('YTD')
        time.sleep(10)
        self.extract_table_values()

    def get_delta_date(self, delta = 1):
        today = datetime.datetime.today()
        diff = datetime.timedelta(days = delta)
        return (today - diff).strftime("%Y/%m/%d")

    def set_params_for_daily_report(self):
        merchant = Select(self.driver.find_element_by_xpath('//form[@id="FRMReportoptions"]//select[@name="merchantid"]'))
        paramDate = self.get_delta_date()
        self.driver.execute_script("document.getElementById('startdate').value = '{0}'".format(paramDate))
        self.driver.execute_script("document.getElementById('enddate').value = '{0}'".format(paramDate))
        merchant.select_by_value('0')
        self.driver.find_element_by_class_name("button").click()
        time.sleep(10)

    def parse_daily_data(self):
        self.set_params_for_daily_report()
        temp_array = []
        for tr in self.driver.find_elements_by_xpath('//*[@id="internalreportdata"]//tr'):
            for td in tr.find_elements_by_tag_name('td'):
                temp_array.append(td.text)
        
        pattern = re.compile(r'[\-\d.\d]+')
        self.table_values.append(pattern.search(temp_array[1]).group(0))
        self.table_values.append(pattern.search(temp_array[2]).group(0))
        self.table_values.append(pattern.search(temp_array[4]).group(0))
        self.table_values.append(pattern.search(temp_array[7]).group(0))
        self.table_values.append(pattern.search(temp_array[-1]).group(0))
        print(self.table_values)
        pass


    def save(self):
        merchant = str(self.table_values[0])
        impression = int(self.table_values[1])
        click = int(self.table_values[2])
        registration = int(self.table_values[3])
        new_deposit = int(self.table_values[4])
        commission = float(self.table_values[5])
        impreytd = int(self.table_values[7])
        cliytd = int(self.table_values[8])
        regytd = int(self.table_values[9])
        ndytd = int(self.table_values[10])
        commiytd = float((self.table_values[11]).replace(",", ""))
        impreto = int(self.table_values[12])
        clito = int(self.table_values[13])
        regto = int(self.table_values[14])
        ndto = int(self.table_values[15])
        commito = float(self.table_values[16])
        dateto = datetime.datetime.strptime(self.get_delta_date(), '%Y/%m/%d').date()

        # engine = create_engine('postgresql://postgres:root@localhost/kyan')
        engine = create_engine('mysql+pymysql://root:@localhost/kyan')
        result = engine.execute("INSERT INTO bet10s (merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regytd, ndytd, commiytd, impreto, clito, regto, ndto, commito, dateto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regytd, ndytd, commiytd, impreto, clito, regto, ndto, commito, dateto)

    def parse(self):
        self.start_driver()
        self.get_page(self.url_to_crawl)
        self.login()
        self.parse_stats_tables()
        self.get_page(self.summary_url)
        self.parse_daily_data()

        self.close_driver()
        self.save()

# Run spider
if __name__ == '__main__':
    Bet10 = Bet10Spider()
    items_list = Bet10.parse()