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

engine = create_engine('postgresql://postgres:root@localhost/kyan')
result = engine.execute("INSERT INTO corals (merchant, impression, click, registration, new_deposit, commission) VALUES (%s, %s, %s, %s, %s, %s);", merchant, impression, click, registration, new_deposit, commission)
