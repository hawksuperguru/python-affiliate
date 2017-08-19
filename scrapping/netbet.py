
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
from selenium.common.exceptions import TimeoutException
import time, datetime

def netbet_scrapping():

        display = Display(visible = 0, size = (1200, 900))
        display.start()
        try:
            Netbet = webdriver.Chrome(executable_path=os.path.abspath("/usr/bin/chromedriver"))
            Netbet.get("https://www.livepartners.com/")
            Netbet.find_element_by_xpath('//*[@id="top"]/div/a').click()
            Netbet.implicitly_wait(10)
            Netbet.find_element_by_id("login_username").send_keys("betfyuk")
            time.sleep(2)
            Netbet.find_element_by_id("login_password").send_keys("dontfuckwithme")
            time.sleep(5)
            pwd = Netbet.find_element_by_id("login_password")
            pwd.send_keys(Keys.RETURN)

            # waiter = wait(Netbet, 15)
            # # waiter.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="contentwrapper"]/div/div[1]/div[2]/div')))
            # # print(Netbet.find_element_by_xpath('//*[@id="contentwrapper"]/div/div[3]').text)
            # # balance = Netbet.find_element_by_xpath('//*[@id="contentwrapper"]/div/div[1]/div[2]/div/strong').text
            # balance = waiter.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="contentwrapper"]/div/div[1]/div[2]/div/strong'))).text
            # pattern = re.compile(r'[\d.\d]+')
            # tmp = pattern.search(balance)
            # balance = tmp.group(0)
            # print(balance)
            time.sleep(30)
            assert "Live Partners - Dashboard" in Netbet.title
            print(Netbet.title)
            header = Netbet.find_element_by_class_name('dshb_icoNav')
            statistics = header.find_elements_by_tag_name('li')[2]
            statistics.click()
            time.sleep(4)
            Netbet.find_element_by_xpath('//*[@id="search_period"]/option[12]').click()
            time.sleep(3)
            toDate = Netbet.find_element_by_id('date_start').get_attribute('value')
            toDateObj = datetime.datetime.strptime(toDate, '%Y-%m-%d').date()
            delta = datetime.timedelta(days = 2)

            aDayAgo = toDateObj - delta

            aDayAgoObj = aDayAgo.strftime("%Y-%m-%d")

            Netbet.execute_script("document.getElementById('date_start').value = '{0}'".format(aDayAgoObj))
            Netbet.execute_script("document.getElementById('date_end').value = '{0}'".format(aDayAgoObj))

            time.sleep(5)
            Netbet.find_element_by_id('ToolTables_results_0').click()
            time.sleep(3)
            tblWrapper = Netbet.find_element_by_class_name('datatable_result_row')
            table = tblWrapper.find_element_by_tag_name('table')
            tfoot = table.find_element_by_tag_name('tfoot')
            depo = tfoot.find_elements_by_tag_name('th')[-1].text
            print(depo)
            return depo
        except TimeoutException:
            print("Required element not found")
        finally:
            Netbet.quit()
            display.stop()  

data = netbet_scrapping()
balance = data
engine = create_engine('postgresql://postgres:root@localhost/kyan')
result = engine.execute("INSERT INTO netbets (balance) VALUES (%s);", balance)
