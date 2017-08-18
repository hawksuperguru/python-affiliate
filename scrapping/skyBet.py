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
import os


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
		sky.find_element_by_xpath('//*[@id="dashboard"]/div[1]/div[1]/div/div[1]/div/div/select[1]/option[3]').click()
		time.sleep(40)
		table = sky.find_element(by=By.ID, value = "dashboard_quick_stats")
		mtds_val = table.find_element(by=By.CLASS_NAME, value = "row_light_color")
		for mtd_val in mtds_val.find_elements_by_tag_name("td"):
			if mtd_val.text != 'Total -':
				mtd_valArr.append(mtd_val.text)
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
commission = float(data[5])
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


engine = create_engine('postgresql://postgres:root@localhost/kyan')
result = engine.execute("INSERT INTO skybets (merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regiytd, ndytd, commiytd, impreto, clito, regito, ndto, commito) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regiytd, ndytd, commiytd, impreto, clito, regito, ndto, commito)