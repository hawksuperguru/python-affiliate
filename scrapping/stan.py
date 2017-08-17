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


def stan_scrapping():
	
	display = Display(visible = 0, size = (1200, 900))
	display.start()

	try:
		Stan = webdriver.Chrome(executable_path=os.path.abspath("/usr/bin/chromedriver"))
		Stan.get("http://www.stanjamesaffiliates.com/")
		username = Stan.find_element_by_name("username")
		username.clear()
		username.send_keys("betfyuk")
		password = Stan.find_element_by_name("password")
		password.clear()
		password.send_keys("dontfuckwithme")
		password.send_keys(Keys.RETURN)
		time.sleep(20)
		mtd_valArr = []
		table = Stan.find_element(by=By.ID, value = "dashboard_quick_stats")
		mtds_val = table.find_element(by=By.CLASS_NAME, value = "row_light_color")
		for mtd_val in mtds_val.find_elements_by_tag_name("td"):
			mtd_valArr.append(mtd_val.text)
		time.sleep(2)
		Stan.find_element_by_xpath('//*[@id="dashboard"]/div[1]/div[1]/div/div[1]/div/div/select[1]/option[2]').click()
		time.sleep(40)
		table = Stan.find_element(by=By.ID, value = "dashboard_quick_stats")
		mtds_val = table.find_element(by=By.CLASS_NAME, value = "row_light_color")
		for mtd_val in mtds_val.find_elements_by_tag_name("td"):
			if mtd_val.text != 'Total -':
				mtd_valArr.append(mtd_val.text)
		Stan.find_element_by_xpath('//*[@id="dashboard"]/div[1]/div[1]/div/div[1]/div/div/select[1]/option[4]').click()
		time.sleep(40)
		table = Stan.find_element(by=By.ID, value = "dashboard_quick_stats")
		mtds_val = table.find_element(by=By.CLASS_NAME, value = "row_light_color")
		for mtd_val in mtds_val.find_elements_by_tag_name("td"):
			if mtd_val.text != 'Total -':
				mtd_valArr.append(mtd_val.text)
		print(mtd_valArr)
		return mtd_valArr
	finally:
		Stan.quit()
		display.stop()
data = stan_scrapping()

merchant = str(data[0])
impression = int(data[1])
click = int(data[2])
registration = int(data[3])
new_deposit = int(data[4])
commission = float(data[5])
imprytd = int(data[3])
cliytd = int(data[3])
regytd = int(data[3])
ndytd = int(data[3])
commiytd = float(data[5])
imprto = int(data[3])
clito = int(data[3])
regto = int(data[3])
ndto = int(data[3])
commito = float(data[5])

engine = create_engine('postgresql://postgres:root@localhost/kyan')
result = engine.execute("INSERT INTO stans (merchant, impression, click, registration, new_deposit, commission, imprytd, cliytd, regytd, ndytd, commiytd, imprto, clito, regto, ndto, commito) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", merchant, impression, click, registration, new_deposit, commission, imprytd, cliytd, regytd, ndytd, commiytd, imprto, clito, regto, ndto, commito)
