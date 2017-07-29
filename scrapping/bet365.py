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


def bet365_scrapping():
	display = Display(visible=0, size=(1200, 900))
	display.start()
	try:
		bet365 = webdriver.Chrome(executable_path=os.path.abspath("/usr/bin/chromedriver"))
		bet365.get("https://www.bet365affiliates.com/ui/pages/affiliates/Affiliates.aspx")
		assert "bet365" in bet365.title
		user = bet365.find_element_by_css_selector("input[name='ctl00$MasterHeaderPlaceHolder$ctl00$userNameTextbox']")
		user.clear()
		user.send_keys("betfyuk")	
		pwd =bet365.find_element_by_id("ctl00_MasterHeaderPlaceHolder_ctl00_tempPasswordTextbox") 
		pwd.clear() 
		pwd =bet365.find_element_by_css_selector("#ctl00_MasterHeaderPlaceHolder_ctl00_passwordTextbox") 
		pwd.send_keys("passiveincome") 
		pwd.send_keys(Keys.RETURN)
		bet365.implicitly_wait(10)
		status = bet365.find_element_by_id("ctl00_MasterHeaderPlaceHolder_ctl00_Statslink")
		status.click() 
		bet365.implicitly_wait(20)
		window_after = bet365.window_handles[1]
		bet365.switch_to.window(window_after)

		bet365.find_element_by_xpath('//*[@id="m_mainPlaceholder_ReportCriteria"]/option[2]').click()

		bet365.find_element_by_id('m_mainPlaceholder_Refresh').send_keys(Keys.RETURN)

		val = []
		# depo = bet365.find_element_by_xpath('//*[@id="m_mainPlaceholder_ResultsBody"]/tr[29]/td[3]').text
		fromDate = bet365.find_element_by_id('m_mainPlaceholder_FromDate').get_attribute('value')
		toDate = bet365.find_element_by_id('m_mainPlaceholder_ToDate').get_attribute('value')
		
		tblWrapper = bet365.find_element_by_class_name('dataTables_scrollBody')
		table = tblWrapper.find_element_by_tag_name('table')
		row = table.find_elements_by_tag_name('tr')[-1]
		depo = row.find_elements_by_tag_name('td')[-1].text
		click = row.find_elements_by_tag_name('td')[0].text
		total = row.find_elements_by_tag_name('td')[-6].text
		sports = row.find_elements_by_tag_name('td')[-5].text
		casino = row.find_elements_by_tag_name('td')[-4].text
		poker = row.find_elements_by_tag_name('td')[-3].text
		games_bingo = row.find_elements_by_tag_name('td')[-2].text

		val = [fromDate, toDate, click, total, sports, casino, poker, games_bingo, depo]
		print(val)		
		return val


	finally:
		bet365.quit()
		display.stop()


data = bet365_scrapping()

fromdate  = data[0]
todate = data[1]
click = int(data[2])
total = float(data[3].replace(',', ''))
sports = float(data[4].replace(',', ''))
casino = float(data[5].replace(',', ''))
poker = float(data[6].replace(',', ''))
games_bingo = float(data[7].replace(',', ''))
balance = float(data[8].replace(',', ''))
print(fromdate, todate, click, total, sports, casino, poker, games_bingo, balance)
engine = create_engine('postgresql://postgres:root@localhost/kyan')
result = engine.execute("INSERT INTO bet365s (fromdate, todate, click, total, sports, casino, poker, games_bingo, balance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);", fromdate, todate, click, total, sports, casino, poker, games_bingo, balance)
