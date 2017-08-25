from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
from sqlalchemy import create_engine
import psycopg2
import os, time, datetime, re

def betfred_scrapping():
	display = Display(visible=0, size=(1200, 900))
	display.start()
	try:
		Betfred = webdriver.Chrome(executable_path=os.path.abspath("/usr/bin/chromedriver"))
		Betfred.get("https://secure.activewins.com/registration.asp")
		Betfred.find_element_by_xpath("//*[@id='navbar']/ul[2]/li[2]/a").click()
		time.sleep(2)
		Betfred.find_element_by_id("username").send_keys("betfyuk")
		time.sleep(2)
		Betfred.find_element_by_id("password").send_keys("dontfuckwithme")
		pwd = Betfred.find_element_by_id("password")
		pwd.send_keys(Keys.RETURN)
		time.sleep(20)

		mtd_valArr = []
		table = Betfred.find_element(by=By.ID, value = "dashboard_quick_stats")
		mtds_val = table.find_element(by=By.CLASS_NAME, value = "row_light_color")
		for mtd_val in mtds_val.find_elements_by_tag_name("td"):
			mtd_valArr.append(mtd_val.text)
		Betfred.find_element_by_xpath('//*[@id="dashboard"]/div[1]/div[1]/div/div[1]/div/div/select[1]/option[2]').click()
		time.sleep(60)
		
		table = Betfred.find_element(by=By.ID, value = "dashboard_quick_stats")
		mtds_val = table.find_element(by=By.CLASS_NAME, value = "row_light_color")
		for mtd_val in mtds_val.find_elements_by_tag_name("td"):
			if mtd_val.text != 'Total -':
				mtd_valArr.append(mtd_val.text)		
		Betfred.get("https://secure.activewins.com/reporting/quick_summary_report.asp")
		toDate = Betfred.find_element_by_id('enddate').get_attribute('value')
		toDateObj = datetime.datetime.strptime(toDate, '%Y/%m/%d').date()

		delta = datetime.timedelta(days = 1)
		aDayAgo = toDateObj - delta
		aDayAgoObj = aDayAgo.strftime("%d/%m/%Y")

		Betfred.execute_script("document.getElementById('startdate').value = '{0}'".format(aDayAgoObj))
		Betfred.execute_script("document.getElementById('enddate').value = '{0}'".format(aDayAgoObj))

		Betfred.find_element_by_class_name("button").click()
		time.sleep(20)
		tableDiv = Betfred.find_element_by_id("internalreportdata")
		table = tableDiv.find_element_by_tag_name("table")
		todayVal = table.find_elements_by_tag_name("tr")

		pattern = re.compile(r'[\-\d.\d]+')
		impreto = pattern.search(todayVal[1].text).group(0)
		mtd_valArr.append(impreto)
		clito = pattern.search(todayVal[2].text).group(0)
		mtd_valArr.append(clito)
		regto = pattern.search(todayVal[5].text).group(0)
		mtd_valArr.append(regto)
		ndto = pattern.search(todayVal[8].text).group(0)
		mtd_valArr.append(ndto)
		commito = pattern.search(todayVal[-1].text).group(0)
		mtd_valArr.append(commito)
		mtd_valArr.append(aDayAgoObj)
		print(mtd_valArr)
		return mtd_valArr
	finally:
		Betfred.quit()
		display.stop()


data = betfred_scrapping()

merchant = str(data[0])
impression = int(data[1])
click = int(data[2])
registration = int(data[3])
new_deposit = int(data[4])
commissionStr = str(data[5]).replace(',', '')
pattern = re.compile(r'[\-\d.\d]+')
commission = float(pattern.search(commissionStr).group(0))
impreytd = int(data[6])
cliytd = int(data[7])
regytd = int(data[8])
ndytd = int(data[9])
commiytdStr = str(data[10]).replace(',', '')
pattern = re.compile(r'[\-\d.\d]+')
commiytd = float(pattern.search(commiytdStr).group(0))
impreto = int(data[11])
clito = int(data[12])
regto = int(data[13])
ndto = int(data[14])
commito = float(data[15])
dateto = datetime.datetime.strptime(data[16], '%d/%m/%Y').date()

engine = create_engine('postgresql://postgres:root@localhost/kyan')
result = engine.execute("INSERT INTO betfreds (merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regytd, ndytd, commiytd, impreto, clito, regto, ndto, commito, dateto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regytd, ndytd, commiytd, impreto, clito, regto, ndto, commito,dateto)
