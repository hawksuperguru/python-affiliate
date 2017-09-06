#!/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
from sqlalchemy import create_engine
import psycopg2, time
import os, datetime, re

class Bet10Spider():
    def __init__(self):
        self.url_to_crawl = 'http://partners.10bet.com/'
        self.items = []

    def start_driver(self):
		print('starting driver...')
		# self.display = Display(visible=0, size=(800, 600))
		# self.display.start()
		# self.driver = webdriver.Chrome("/usr/bin/chromedriver")
        self.driver = webdriver.Chrome("/usr/bin/chromedriver")
		sleep(4)

    def close_driver(self):
		print('closing driver...')
		# self.display.stop()
		self.driver.quit()
		print('closed!')

    def get_page(self, url):
		print('getting page...')
		self.driver.get(url)
		sleep(10)

    def login(self):
		print('getting pass the gate page...')
		try:
			form = self.driver.find_element_by_id('FMlogins')
			form.find_element_by_id('username').send_keys('betfyuk')
			form.find_element_by_id('password').send_keys('dontfuckwithme')
			form.find_element_by_xpath('.//*[@class="btn btn-primary btn-lg"]').click()
			sleep(30)
		except Exception:
            print("Exception found in login process...")
			pass

    def grab_list_items(self):
		print('grabbing list of items...')
		for div in self.driver.find_elements_by_xpath('//ul[@class="menu-items row"]//li'):
			data = self.process_elements(div)
			if data:
				self.all_items.append(data)
			else:
				pass

    def process_elements(self, div):
		prd_image = ''
		prd_title = ''
		prd_price = ''

		try:
			prd_image = div.find_element_by_xpath('.//*[@class="photo item-photo"]').get_attribute("source")
			prd_title = div.find_element_by_xpath('.//*[@class="text ng-binding"]').text
			prd_price = div.find_element_by_xpath('.//*[@class="price ng-scope ng-binding"]').text
		except Exception:
			pass

		if prd_image and prd_title and prd_price:
			single_item_info = {
				'image': prd_image.encode('UTF-8'),
				'title': prd_title.encode('UTF-8'),
				'price': prd_price.encode('UTF-8')
			}
			return single_item_info
		else:
			return False

	def parse(self):
		self.start_driver()
		self.get_page(self.url_to_crawl)
		self.login()
		# self.grab_list_items()
		# self.close_driver()

		# if self.all_items:
		# 	return self.all_items
		# else:
		# 	return False, False

		
# Run spider
Bet10 = Bet10Spider()
items_list = Bet10.parse()

# Do something with the data touched
for item in items_list:
	print(item)
        

def bet10_scrapping():
	display = Display(visible=0, size=(1200, 900))
	display.start()
	try:		
		bet10 = webdriver.Chrome(executable_path=os.path.abspath("/usr/bin/chromedriver"))
		bet10.get("http://partners.10bet.com/")
		bet10.find_element_by_id("username").send_keys("betfyuk")
		bet10.find_element_by_id("password").send_keys("dontfuckwithme")
		pwd = bet10.find_element_by_id("password")
		pwd.send_keys(Keys.RETURN)
		bet10.implicitly_wait(10)
		mtd_valArr = []
		table = bet10.find_element(by=By.ID, value = "dashboard_quick_stats")
		mtds_val = table.find_element(by=By.CLASS_NAME, value = "row_light_color")
		for mtd_val in mtds_val.find_elements_by_tag_name("td"):
			mtd_valArr.append(mtd_val.text)
		bet10.find_element_by_xpath('//*[@id="dashboard"]/div[1]/div[1]/div/div[1]/div/div/select[1]/option[2]').click()
		time.sleep(60)
		table = bet10.find_element(by=By.ID, value = "dashboard_quick_stats")
		mtds_val = table.find_element(by=By.CLASS_NAME, value = "row_light_color")
		for mtd_val in mtds_val.find_elements_by_tag_name("td"):
			if mtd_val.text != 'Total -':
				mtd_valArr.append(mtd_val.text)
		
		bet10.get("https://partners.10bet.com/reporting/quick_summary_report.asp")
		toDate = bet10.find_element_by_id('enddate').get_attribute('value')
		toDateObj = datetime.datetime.strptime(toDate, '%Y/%m/%d').date()
		delta = datetime.timedelta(days = 1)
		aDayAgo = toDateObj - delta
		aDayAgoObj = aDayAgo.strftime("%Y/%m/%d")
		reportDiv = bet10.find_element_by_id("reportcriteria")
		merchantDiv = reportDiv.find_elements_by_tag_name("tr")[3]
		merchantId = merchantDiv.find_element_by_tag_name("select")
		merchant = merchantId.find_elements_by_tag_name("option")[0]
		
		bet10.execute_script("document.getElementById('startdate').value = '{0}'".format(aDayAgoObj))
		bet10.execute_script("document.getElementById('enddate').value = '{0}'".format(aDayAgoObj))
		merchant.click()
		time.sleep(5)
		bet10.find_element_by_class_name("button").click()
		time.sleep(10)
		tableDiv = bet10.find_element_by_id("internalreportdata")
		table = tableDiv.find_element_by_tag_name("table")
		todayVal = table.find_elements_by_tag_name("tr")

		pattern = re.compile(r'[\-\d.\d]+')
		impreto = pattern.search(todayVal[1].text).group(0)
		mtd_valArr.append(impreto)
		clito = pattern.search(todayVal[2].text).group(0)
		mtd_valArr.append(clito)
		regto = pattern.search(todayVal[4].text).group(0)
		mtd_valArr.append(regto)
		ndto = pattern.search(todayVal[7].text).group(0)
		mtd_valArr.append(ndto)
		commito = pattern.search(todayVal[-1].text).group(0)
		mtd_valArr.append(commito)
		mtd_valArr.append(aDayAgoObj)
		print(mtd_valArr)
		return mtd_valArr
	finally:
		bet10.quit()
		display.stop()


data = bet10_scrapping()

merchant = str(data[0])
impression = int(data[1])
click = int(data[2])
registration = int(data[3])
new_deposit = int(data[4])
commission = float(data[5])
impreytd = int(data[6])
cliytd = int(data[7])
regytd = int(data[8])
ndytd = int(data[9])
commiytd = float((data[10]).replace(",", ""))
impreto = int(data[11])
clito = int(data[12])
regto = int(data[13])
ndto = int(data[14])
commito = float(data[15])
dateto = datetime.datetime.strptime(data[16], '%Y/%m/%d').date()


engine = create_engine('postgresql://postgres:root@localhost/kyan')
result = engine.execute("INSERT INTO bet10s (merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regytd, ndytd, commiytd, impreto, clito, regto, ndto, commito, dateto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regytd, ndytd, commiytd, impreto, clito, regto, ndto, commito, dateto)
