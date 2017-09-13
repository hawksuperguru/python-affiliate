# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display

import datetime
import time
from settings.config import *


class UBrowse(object):
    """ Create emulation user browsing """
    def __init__(self):
        chrome_option = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images":2}
        chrome_option.add_experimental_option("prefs",prefs)

        if ENV != 'dev':
            self.display = Display(visible=0, size=(1200, 900))
            self.display.start()

        self.driver = webdriver.Chrome(executable_path = CHROME_DRIVER_PATH, chrome_options=chrome_option)

    def create_screenshot(self, action):
        stime = datetime.datetime.now()
        year = str(stime.year)
        month = str(stime.month)
        day = str(stime.day)
        hour = str(stime.hour)
        minute = str(stime.minute)

        path_error = 'screens/errors/'
        full_path = path_error + "%s.%s.%s-%s-%s_%s.png"%(year, month, day, hour, minute, action)  

        self.driver.save_screenshot(full_path)

    def open_url(self, link):
        self.driver.get(link)

    def get_delta_date(self, delta = 2, formatString = '%Y/%m/%d'):
        today = datetime.datetime.today()
        diff = datetime.timedelta(days = delta)
        return (today - diff).strftime(formatString)

    def close(self):
        if ENV != 'dev':
            self.display.stop()

        self.driver.quit()
        # print("Browser client closed...")

    def click_link(self, link, type='xpath'):
        if type == 'by_xpath':
            self.driver.implicitly_wait(5)
            obj = self.driver.find_element_by_xpath(link)
        if type == 'by_class':
            self.driver.implicitly_wait(5)
            obj = self.driver.find_element_by_class_name(link)
        if type == 'by_id':
            self.driver.implicitly_wait(5)
            obj = self.driver.find_element_by_id(link)
        
        if obj:
            obj.click()
        return True

    def set_loginform(self, path_to_element, type = 'xpath'):
        self.driver.implicitly_wait(5)

        if type == 'xpath':
            self.loginform = self.driver.find_element_by_xpath(path_to_element)
        elif type == 'css':
            self.loginform = self.driver.find_element_by_css_selector(path_to_element)

    def set_passform(self, path_to_element, type = 'xpath'):
        self.driver.implicitly_wait(5)

        if type == 'xpath':
            self.passform = self.driver.find_element_by_xpath(path_to_element)
        elif type == 'css':
            self.passform = self.driver.find_element_by_css_selector(path_to_element)

    def set_loginbutton(self, path_to_element, type = 'xpath'):
        self.driver.implicitly_wait(5)

        if type == 'xpath':
            self.btn_ok = self.driver.find_element_by_xpath(path_to_element)
        elif type == 'css':
            self.btn_ok = self.driver.find_element_by_css_selector(path_to_element)

    def login(self, user, mypass):
        try:
            self.driver.implicitly_wait(10)
            time.sleep(0.5)
            self.loginform.clear()
            self.loginform.send_keys(user)
            time.sleep(0.5)
            self.passform.clear()
            self.passform.send_keys(mypass)
            time.sleep(0.5)

            if self.btn_ok is None:
                self.passform.send_keys(Keys.RETURN)
            else:
                self.btn_ok.click()
        except:
            return False
        return True

if __name__ == "__main__":
    run = UBrowse()
