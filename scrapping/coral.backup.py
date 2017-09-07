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


def coral_scrapping():
	display = Display(visible = 0, size = (1200, 900))
	display.start()

	try:
		Coral = webdriver.Chrome(executable_path=os.path.abspath("/usr/bin/chromedriver"))
		Coral.get("http://affiliates.coral.co.uk/")
		Coral.find_element_by_link_text("Log In").click()
		window_after = Coral.window_handles[1]
		Coral.switch_to_window(window_after)
		Coral.find_element_by_id("username").send_keys("betfyuk1")
		Coral.find_element_by_id("password").send_keys("dontfuckwithme")
		pwd = Coral.find_element_by_id("password")
		pwd.send_keys(Keys.RETURN)
		waiter = wait(Coral, 30)
		waiter.until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="dashboard_quick_stats"]/tbody/tr[1]/td[1]'), "Merchant"))
		mtd_valArr = []
		table = Coral.find_element(by=By.ID, value = "dashboard_quick_stats")
		mtds_val = Coral.find_element(by=By.CLASS_NAME, value = "row_light_color")
		for mtd_val in mtds_val.find_elements_by_tag_name("td"):
			mtd_valArr.append(mtd_val.text)
		Coral.find_element_by_xpath('//*[@id="dashboard"]/div[1]/div[1]/div/div[1]/div/div/select[1]/option[2]').click()
		waiter = wait(Coral, 40)
		waiter.until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="dashboard_quick_stats"]/tbody/tr[1]/td[1]'), "Merchant"))
		table = Coral.find_element(by=By.ID, value = "dashboard_quick_stats")
		mtds_val = Coral.find_element(by=By.CLASS_NAME, value = "row_light_color")
		for mtd_val in mtds_val.find_elements_by_tag_name("td"):
			if mtd_val.text != 'Total -':
				mtd_valArr.append(mtd_val.text)
		Coral.get("https://affiliate.coral.co.uk/reporting/quick_summary_report.asp")
		toDate = Coral.find_element_by_id('enddate').get_attribute('value')
		toDateObj = datetime.datetime.strptime(toDate, '%Y/%m/%d').date()
		delta = datetime.timedelta(days = 1)
		aDayAgo = toDateObj - delta
		aDayAgoObj = aDayAgo.strftime("%Y/%m/%d")
		reportDiv = Coral.find_element_by_id("reportcriteria")
		merchantDiv = reportDiv.find_elements_by_tag_name("tr")[3]
		merchantId = merchantDiv.find_element_by_tag_name("select")
		merchant = merchantId.find_elements_by_tag_name("option")[0]
		
		Coral.execute_script("document.getElementById('startdate').value = '{0}'".format(aDayAgoObj))
		Coral.execute_script("document.getElementById('enddate').value = '{0}'".format(aDayAgoObj))
		merchant.click()
		time.sleep(5)
		Coral.find_element_by_class_name("button").click()
		time.sleep(20)
		tableDiv = Coral.find_element_by_id("internalreportdata")
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
		Coral.quit()
		display.stop()	

data = coral_scrapping()

merchant = data[0]
impression = int(data[1])
click = int(data[2])
registration = int(data[3])
new_deposit = int(data[4])
commission = float(data[5])
impreytd = int(data[6])
cliytd = int(data[7])
regytd = int(data[8])
ndytd = int(data[9])
commiytd = float(data[10])
impreto = int(data[11])
clito = int(data[12])
regto = int(data[13])
ndto = int(data[14])
commito = float(data[15])
dateto = datetime.datetime.strptime(data[16], '%Y/%m/%d').date()


engine = create_engine('postgresql://postgres:root@localhost/kyan')
result = engine.execute("INSERT INTO corals (merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regytd, ndytd, commiytd, impreto, clito, regto, ndto, commito, dateto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regytd, ndytd, commiytd, impreto, clito, regto, ndto, commito, dateto)
