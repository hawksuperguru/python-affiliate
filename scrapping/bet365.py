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

class Bet365Spider(object):
    """docstring for bet365Spider"""
    def __init__(self):
        self.client = UBrowse()
        self.login_url = 'https://www.bet365affiliates.com/ui/pages/affiliates/Affiliates.aspx'
        self.stats_url = 'https://www.bet365affiliates.com/members/CMSitePages/Router.aspx?TargetPage=Members%2fStatistics&lng=1'
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

    def report_error_log(self, message):
        self.report.write_error_log("Bet365", message)

    def parse_report_table(self, table_name):
        tblWrapper = self.client.driver.find_element_by_class_name('dataTables_scrollBody')
        table = tblWrapper.find_element_by_tag_name('table')
        row = table.find_elements_by_tag_name('tr')[-1]

        pattern = re.compile(r'[\-\d.\d]+')

        click = int(pattern.search(row.find_elements_by_tag_name('td')[0].text).group(0))
        nSignup = int(pattern.search(row.find_elements_by_tag_name('td')[1].text).group(0))
        nDepo = int(pattern.search(row.find_elements_by_tag_name('td')[2].text).group(0))
        valDepo = float(pattern.search(row.find_elements_by_tag_name('td')[8].text).group(0).replace(',', '.'))
        numDepo = int(pattern.search(row.find_elements_by_tag_name('td')[9].text).group(0))
        spotsTurn = float(pattern.search(row.find_elements_by_tag_name('td')[10].text).group(0).replace(',', '.'))
        numSptBet = int(pattern.search(row.find_elements_by_tag_name('td')[11].text).group(0))
        acSptUsr = int(pattern.search(row.find_elements_by_tag_name('td')[12].text).group(0))
        sptNetRev = float(pattern.search(row.find_elements_by_tag_name('td')[-10].text).group(0).replace(',', '.'))
        casinoNetRev = float(pattern.search(row.find_elements_by_tag_name('td')[-9].text).group(0).replace(',', '.'))
        pokerNetRev = float(pattern.search(row.find_elements_by_tag_name('td')[-8].text).group(0).replace(',', '.'))
        bingoNetRev = float(pattern.search(row.find_elements_by_tag_name('td')[-7].text).group(0).replace(',', '.'))
        netRev = float(pattern.search(row.find_elements_by_tag_name('td')[-6].text).group(0).replace(',', '.'))
        afSpt = float(pattern.search(row.find_elements_by_tag_name('td')[-5].text).group(0).replace(',', '.'))
        afCasino = float(pattern.search(row.find_elements_by_tag_name('td')[-4].text).group(0).replace(',', '.'))
        afPoker = float(pattern.search(row.find_elements_by_tag_name('td')[-3].text).group(0).replace(',', '.'))
        afBingo = float(pattern.search(row.find_elements_by_tag_name('td')[-2].text).group(0).replace(',', '.'))
        commission = float(pattern.search(row.find_elements_by_tag_name('td')[-1].text).group(0).replace(',', '.'))

        # val = [param_date, click, nSignup, nDepo, valDepo, numDepo, spotsTurn, numSptBet, acSptUsr, sptNetRev, casinoNetRev, pokerNetRev, bingoNetRev, netRev, afSpt, afCasino, afPoker, afBingo, commission]

        date = datetime.datetime.strptime(self.client.get_delta_date(1, "%d/%m/%Y"), '%d/%m/%Y').date()
        engine = create_engine(get_database_connection_string())
        
        if table_name == "bet365s":
            result = engine.execute("INSERT INTO bet365s (dateto, click, nSignup, nDepo, valDepo, numDepo, spotsTurn, numSptBet, acSptUsr, sptNetRev, casinoNetRev, pokerNetRev, bingoNetRev, netRev, afSpt, afCasino, afPoker, afBingo, commission) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", date, click, nSignup, nDepo, valDepo, numDepo, spotsTurn, numSptBet, acSptUsr, sptNetRev, casinoNetRev, pokerNetRev, bingoNetRev, netRev, afSpt, afCasino, afPoker, afBingo, commission)
        else:
            result = engine.execute("INSERT INTO bet365others (dateto, click, nSignup, nDepo, valDepo, numDepo, spotsTurn, numSptBet, acSptUsr, sptNetRev, casinoNetRev, pokerNetRev, bingoNetRev, netRev, afSpt, afCasino, afPoker, afBingo, commission) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", date, click, nSignup, nDepo, valDepo, numDepo, spotsTurn, numSptBet, acSptUsr, sptNetRev, casinoNetRev, pokerNetRev, bingoNetRev, netRev, afSpt, afCasino, afPoker, afBingo, commission)
        return result

    def parse_stats(self, wait_for = 10, table_name = "bet365s"):
        # time.sleep(10)
        val = []
        try:
            self.client.open_url(self.stats_url)
            time.sleep(10)
            param_date = self.client.get_delta_date(1, "%d/%m/%Y")

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

    def run(self, username = 'betfyuk', password = 'passiveincome'):
        self.client.open_url(self.login_url)
        time.sleep(10)
        
        self.client.driver.find_element_by_css_selector("input[name='ctl00$MasterHeaderPlaceHolder$ctl00$userNameTextbox']").send_keys(username)
        tmp_pass = self.client.driver.find_element_by_xpath("//*[@id='ctl00_MasterHeaderPlaceHolder_ctl00_tempPasswordTextbox']")
        tmp_pass.clear()
        self.client.driver.find_element_by_xpath("//*[@id='ctl00_MasterHeaderPlaceHolder_ctl00_passwordTextbox']").send_keys(password)
        self.client.driver.find_element_by_xpath("//*[@id='ctl00_MasterHeaderPlaceHolder_ctl00_passwordTextbox']").send_keys(Keys.RETURN)
        
        return True

if __name__ == '__main__':
    print("Bet365Spider is being initialized...")
    bet365 = Bet365Spider()

    print("Going to log in with the first account(betfyuk:passiveincome) ...")
    if bet365.run() is True:
        print("Getting reports...")
        bet365.parse_stats()
        print("Done!\n")
    else:
        bet365.report_error_log("Login failed!!")
    bet365.client.close()


    bet365Other = Bet365Spider()
    print("Going to log in with the first account(bigfreebet1281:Porsche911) ...")
    if bet365Other.run('bigfreebet1281', 'Porsche911') is True:
        print("Getting reports...")
        bet365Other.parse_stats(10, 'bet365others')
        print("Done!\n")
    else:
        bet365Other.report_error_log("Login failed!!")
    bet365Other.client.close()