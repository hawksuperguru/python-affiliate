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


def eight88_scrapping():

	display = Display(visible = 0, size = (1200, 900))
	display.start()
	try:
		eight88 = webdriver.Chrome(executable_path=os.path.abspath("/usr/bin/chromedriver"))
		eight88.set_window_size(1120, 550)
		eight88.get("http://affiliates.888.com/")
		assert "Earn Real Money" in eight88.title
		eight88.find_element_by_class_name("hide-under-480").click()
		wait(eight88, 10).until(EC.frame_to_be_available_and_switch_to_it(eight88.find_element_by_xpath('//iframe[contains(@src, "Auth/Login")]')))
		eight88.find_element_by_id("userName").send_keys("betfyuk")
		eight88.find_element_by_id("password").send_keys("LALB37hUhs")
		eight88.find_element_by_id("btnLogin").click()
		balance_arr = []
		eight88.find_element_by_id("rbQuickStatID_This Month (1st - Today)").click()
		bal = eight88.find_element_by_class_name("BoxSum").text
		balCents = eight88.find_element_by_class_name("BoxCents").text
		netBal = bal + balCents
		for summarise in eight88.find_elements_by_xpath('.//span[@class = "summariseTab"]'):
		    balance_arr.append(summarise.text)
		balance_arr.append(netBal)
		return balance_arr
		
	finally:
		eight88.quit()
		display.stop()

data = eight88_scrapping()
impression = int(data[0])
click = int(data[1])
registration = int(data[2])
lead = int(data[3])
money_player = int(data[4])
balance = float(data[5])

engine = create_engine('postgresql://postgres:root@localhost/kyan')
result = engine.execute("INSERT INTO eight88s (impression, click, registration, lead, money_player, balance) VALUES (%s, %s, %s, %s, %s, %s);", impression, click, registration, lead, money_player, balance)
