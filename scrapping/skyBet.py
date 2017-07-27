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
import os


def sky_scrapping():

	display = Display(visible = 0, size = (1200, 900))
	display.start()

	try:
		sky = webdriver.Chrome(executable_path=os.path.abspath("/usr/bin/chromedriver"))
		sky.get("https://www.skybet.com/affiliatehub/")
		sky.find_element_by_link_text("Login").send_keys(Keys.RETURN)
		sky.find_element_by_name("username").send_keys("betfy")
		sky.find_element_by_name("password").send_keys("dontfuckwithme")
		pwd = sky.find_element_by_name("password")
		pwd.send_keys(Keys.RETURN)
		sky.implicitly_wait(10)
		mtd_valArr = []
		table = sky.find_element(by=By.ID, value = "dashboard_quick_stats")
		mtds_val = table.find_element(by=By.CLASS_NAME, value = "row_light_color")
		for mtd_val in mtds_val.find_elements_by_tag_name("td"):
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
commission = str(data[5])

engine = create_engine('postgresql://postgres:root@localhost/kyan')
result = engine.execute("INSERT INTO skybets (merchant, impression, click, registration, new_deposit, commission) VALUES (%s, %s, %s, %s, %s, %s);", merchant, impression, click, registration, new_deposit, commission)