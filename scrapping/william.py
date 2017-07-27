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


def william_scrapping():

        display = Display(visible = 0, size = (1200, 900))
        display.start()

        try:
                William = webdriver.Chrome(executable_path=os.path.abspath("/usr/bin/chromedriver"))
                William.get("http://www.affutd.com/")
                William.find_element_by_xpath('//*[@id="site-header"]/div/div/div[2]/a').send_keys(Keys.RETURN)
                window_after = William.window_handles[1]
                William.switch_to_window(window_after)                
                William.find_element_by_id("txtUsername").clear()
                William.find_element_by_id("txtUsername").send_keys("betfy.co.uk")
                pwd = William.find_element_by_id("txtPassword")
                pwd.clear()
                pwd.send_keys("dontfuckwithme")
                pwd.send_keys(Keys.RETURN)
                
                waiter = wait(William, 30)
                uniSign = unicode("€", encoding='utf-8')
                waiter.until(EC.text_to_be_present_in_element((By.XPATH, "//*[@id='ebContainer_latest']/div[1]/a/div/span[1]"), uniSign))
                balance = William.find_element_by_xpath("//*[@id='ebContainer_latest']/div[1]/a/div/span[1]").text
                pattern = re.compile(r'[\d.\d]+')
                tmp = pattern.search(balance)
                balance = tmp.group(0)
                print(balance)
                return balance
        finally:
                William.quit()


data = william_scrapping()
balance = data
engine = create_engine('postgresql://postgres:root@localhost/kyan')
result = engine.execute("INSERT INTO williams (balance) VALUES (%s);", balance)
