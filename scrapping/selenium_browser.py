# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import datetime
import time


class UBrowse(object):
    """ Create emulation user browsing """
    def __init__(self):
        chrome_option = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images":2}
        chrome_option.add_experimental_option("prefs",prefs)
        # self.driver = webdriver.Chrome(executable_path = "./chrome/chromedriver", chrome_options=chrome_option)
        self.driver = webdriver.Chrome(executable_path = "../chrome/chromedriver.exe", chrome_options=chrome_option)

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

    def set_loginform(self, path_to_element):
        self.driver.implicitly_wait(5)
        self.loginform = self.driver.find_element_by_xpath(path_to_element)

    def set_passform(self, path_to_element):
        self.driver.implicitly_wait(5)
        self.passform = self.driver.find_element_by_xpath(path_to_element)

    def set_loginbutton(self, path_to_element):
        self.driver.implicitly_wait(5)
        self.btn_ok = self.driver.find_element_by_xpath(path_to_element)

    def login(self, user, mypass):
        try:
            self.driver.implicitly_wait(10)
            time.sleep(0.5)
            self.loginform.send_keys(user)
            time.sleep(0.5)
            self.passform.send_keys(mypass)
            time.sleep(0.5)
            self.btn_ok.click()
        except:
            return False
        return True

if __name__ == "__main__":
    run = UBrowse()
