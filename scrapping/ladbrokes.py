# encoding=utf-8

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
import os, re


def ladbrokes_scrapping():
        display = Display(visible = 0, size = (1200, 900))
        display.start()
        try:
                Ladbrokes = webdriver.Chrome(executable_path=os.path.abspath("/usr/bin/chromedriver"))
                Ladbrokes.set_window_size(1120, 550)
                Ladbrokes.get("http://www.ladbrokespartners.com")
                Ladbrokes.find_element_by_class_name("top-login-link").click()
                Ladbrokes.find_element_by_id("loginusername").send_keys("betfyuk")
                Ladbrokes.find_element_by_id("loginPassword").send_keys("WjewEEUV")
                pwd = Ladbrokes.find_element_by_id("loginPassword")
                pwd.send_keys(Keys.RETURN)
                waiter = wait(Ladbrokes, 30)
                uniSign = unicode("£", encoding='utf-8')
                waiter.until(EC.text_to_be_present_in_element((By.XPATH, "//div[@ng-bind='currentEarning']"), uniSign))
                currentEaring = Ladbrokes.find_element_by_xpath('//div[@ng-bind="currentEarning"]').text
                pattern = re.compile(r'[\d\.\d]+')
                tmp = pattern.search(currentEaring)
                currentEaring = tmp.group(0)
                print(currentEaring)
                return currentEaring
        finally:
                Ladbrokes.quit()
                display.stop()

data = ladbrokes_scrapping()
balance = data
engine = create_engine('postgresql://postgres:root@localhost/kyan')
result = engine.execute("INSERT INTO ladbrokes (balance) VALUES (%s);", balance)
