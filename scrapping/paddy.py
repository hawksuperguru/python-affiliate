# encoding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
from sqlalchemy import create_engine
import psycopg2
import os, re


def paddy_scrapping():

        display = Display(visible = 0, size = (1200, 900))
        display.start()

        try:
                Paddy = webdriver.Chrome(executable_path=os.path.abspath("/usr/bin/chromedriver"))
                Paddy.get("http://www.paddypartners.com/")
                Paddy.find_element_by_id("login-button").click()
                wait(Paddy, 10).until(EC.frame_to_be_available_and_switch_to_it(Paddy.find_element_by_xpath('//iframe[contains(@id, "login-iframe")]')))
                Paddy.find_element_by_id("txtUsername").clear()
                Paddy.find_element_by_id("txtUsername").send_keys("betfyuk")
                pwd = Paddy.find_element_by_id("txtPassword")
                pwd.clear()
                pwd.send_keys("dontfuckwithme")
                pwd.send_keys(Keys.RETURN)
                Paddy.find_element_by_id("txtUsername").send_keys("betfyuk")
                Paddy.find_element_by_id("txtPassword").send_keys("dontfuckwithme")
                Paddy.find_element_by_id("txtPassword").send_keys(Keys.RETURN)
                waiter = wait(Paddy, 30)
                uniSign = unicode("€", encoding='utf-8')
                waiter.until(EC.text_to_be_present_in_element((By.XPATH, "//*[@id='ebContainer_latest']/div[2]/a/div/span[1]"), uniSign))
                balance = Paddy.find_element_by_xpath("//*[@id='ebContainer_latest']/div[2]/a/div/span[1]").text
                pattern = re.compile(r'[\d.\d]+')
                tmp = pattern.search(balance)
                balance = tmp.group(0)
                print(balance)
                return balance
        finally:
                Paddy.quit()


data = paddy_scrapping()
balance = data
engine = create_engine('postgresql://postgres:root@localhost/kyan')
result = engine.execute("INSERT INTO paddyies (balance) VALUES (%s);", balance)
