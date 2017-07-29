from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
from sqlalchemy import create_engine
from selenium.webdriver.support.ui import Select
import psycopg2
import os, time


def bet365_other_scrapping():
	display = Display(visible=0, size=(1200, 900))
	display.start()
	try:
		bet365 = webdriver.Chrome(executable_path=os.path.abspath("/usr/bin/chromedriver"))
		bet365.get("https://www.bet365affiliates.com/ui/pages/affiliates/Affiliates.aspx")
		assert "bet365" in bet365.title
		user = bet365.find_element_by_css_selector("input[name='ctl00$MasterHeaderPlaceHolder$ctl00$userNameTextbox']")
		user.clear()
		user.send_keys("bigfreebet1281")	
		pwd =bet365.find_element_by_id("ctl00_MasterHeaderPlaceHolder_ctl00_tempPasswordTextbox") 
		pwd.clear() 
		pwd =bet365.find_element_by_css_selector("#ctl00_MasterHeaderPlaceHolder_ctl00_passwordTextbox") 
		pwd.send_keys("Porsche911") 
		pwd.send_keys(Keys.RETURN)
		bet365.implicitly_wait(10)
		status = bet365.find_element_by_id("ctl00_MasterHeaderPlaceHolder_ctl00_Statslink")
		status.click() 
		bet365.implicitly_wait(20)
		window_after = bet365.window_handles[1]
		bet365.switch_to.window(window_after)

		bet365.find_element_by_xpath('//*[@id="m_mainPlaceholder_ReportCriteria"]/option[2]').click()
		bet365.find_element_by_xpath('//*[@id="m_mainPlaceholder_ChooseLink"]/option[2]').click()

		bet365.find_element_by_id('m_mainPlaceholder_Refresh').send_keys(Keys.RETURN)

		val = []
		# depo = bet365.find_element_by_xpath('//*[@id="m_mainPlaceholder_ResultsBody"]/tr[29]/td[3]').text
		fromDate = bet365.find_element_by_id('m_mainPlaceholder_FromDate').get_attribute('value')
		toDate = bet365.find_element_by_id('m_mainPlaceholder_ToDate').get_attribute('value')
		
		tblWrapper = bet365.find_element_by_class_name('dataTables_scrollBody')
		table = tblWrapper.find_element_by_tag_name('table')
		row = table.find_elements_by_tag_name('tr')[-1]
		depo = row.find_elements_by_tag_name('td')[2].text


		val = [depo, fromDate, toDate]
		print(val)		
		return val
	finally:
		bet365.quit()
		display.stop()

data = bet365_other_scrapping()

balance  = data[0]
fromdate = data[1]
todate = data[2]


engine = create_engine('postgresql://postgres:root@localhost/kyan')
result = engine.execute("INSERT INTO bet365others (balance, fromdate, todate) VALUES (%s, %s, %s);", balance, fromdate, todate)