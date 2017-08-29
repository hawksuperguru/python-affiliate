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


def sky_scrapping():

	display = Display(visible = 0, size = (1200, 900))
	display.start()

	try:
		sky = webdriver.Chrome(executable_path=os.path.abspath("/usr/bin/chromedriver"))
		sky.get("https://www.skybet.com/affiliatehub/")
		sky.find_element_by_link_text("Login").send_keys(Keys.RETURN)
		sky.find_element_by_name("username").send_keys("betfy")
		time.sleep(2)
		sky.find_element_by_name("password").send_keys("dontfuckwithme")
		time.sleep(5)
		pwd = sky.find_element_by_name("password")
		pwd.send_keys(Keys.RETURN)
		sky.implicitly_wait(10)
		time.sleep(5)
		mtd_valArr = []
		table = sky.find_element(by=By.ID, value = "dashboard_quick_stats")
		mtds_val = table.find_element(by=By.CLASS_NAME, value = "row_light_color")
		for mtd_val in mtds_val.find_elements_by_tag_name("td"):
			mtd_valArr.append(mtd_val.text)
		time.sleep(2)
		sky.find_element_by_xpath('//*[@id="dashboard"]/div[1]/div[1]/div/div[1]/div/div/select[1]/option[2]').click()
		time.sleep(40)
		table = sky.find_element(by=By.ID, value = "dashboard_quick_stats")
		mtds_val = table.find_element(by=By.CLASS_NAME, value = "row_light_color")
		for mtd_val in mtds_val.find_elements_by_tag_name("td"):
			if mtd_val.text != 'Total -':
				mtd_valArr.append(mtd_val.text)
		
		sky.get("https://affiliatehub.skybet.com/reporting/quick_summary_report.asp")
		toDate = sky.find_element_by_id('enddate').get_attribute('value')
		toDateObj = datetime.datetime.strptime(toDate, '%Y/%m/%d').date()
		delta = datetime.timedelta(days = 1)
		aDayAgo = toDateObj - delta
		aDayAgoObj = aDayAgo.strftime("%Y/%m/%d")
		reportDiv = sky.find_element_by_id("reportcriteria")
		merchantDiv = reportDiv.find_elements_by_tag_name("tr")[3]
		merchantId = merchantDiv.find_element_by_tag_name("select")
		merchant = merchantId.find_elements_by_tag_name("option")[0]
		
		sky.execute_script("document.getElementById('startdate').value = '{0}'".format(aDayAgoObj))
		sky.execute_script("document.getElementById('enddate').value = '{0}'".format(aDayAgoObj))
		merchant.click()
		time.sleep(5)
		sky.find_element_by_class_name("button").click()
		time.sleep(20)
		tableDiv = sky.find_element_by_id("internalreportdata")
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
		sky.quit()
		display.stop()

data = sky_scrapping()


merchant = str(data[0])
impression = int(data[1])
click = int(data[2])
registration = int(data[3])
new_deposit = int(data[4])
commission = float((data[5]).replace(",", ""))
impreytd = int(data[6])
cliytd = int(data[7])
regiytd = int(data[8])
ndytd = int(data[9])
commiytd = float(data[10])
impreto = int(data[11])
clito = int(data[12])
regito = int(data[13])
ndto = int(data[14])
commito = float(data[15])
dateto = datetime.datetime.strptime(data[16], '%Y/%m/%d').date()


engine = create_engine('postgresql://postgres:root@localhost/kyan')
result = engine.execute("INSERT INTO skybets (merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regiytd, ndytd, commiytd, impreto, clito, regito, ndto, commito, dateto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regiytd, ndytd, commiytd, impreto, clito, regito, ndto, commito, dateto)