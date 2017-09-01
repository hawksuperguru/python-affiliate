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
import os, time, datetime, re


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

		toDate = bet365.find_element_by_id('m_mainPlaceholder_ToDate').get_attribute('value')
		toDateObj = datetime.datetime.strptime(toDate, '%d/%m/%Y').date()
		delta = datetime.timedelta(days = 1)
		aDayAgo = toDateObj - delta
		aDayAgoObj = aDayAgo.strftime("%d/%m/%Y")

		bet365.find_element_by_xpath('//*[@id="m_mainPlaceholder_ReportCriteria"]/option[2]').click()

		bet365.execute_script("document.getElementById('m_mainPlaceholder_FromDate').value = '{0}'".format(aDayAgoObj))
		
		bet365.execute_script("document.getElementById('m_mainPlaceholder_InitialFromDate').value = '{0}'".format(aDayAgoObj))

		bet365.execute_script("document.getElementById('m_mainPlaceholder_ToDate').value = '{0}'".format(aDayAgoObj))
		
		bet365.execute_script("document.getElementById('m_mainPlaceholder_ToDate').value = '{0}'".format(aDayAgoObj))

		bet365.find_element_by_id('m_mainPlaceholder_Refresh').send_keys(Keys.RETURN)

		time.sleep(2)

		val = []
		# depo = bet365.find_element_by_xpath('//*[@id="m_mainPlaceholder_ResultsBody"]/tr[29]/td[3]').text
		


		tblWrapper = bet365.find_element_by_class_name('dataTables_scrollBody')
		table = tblWrapper.find_element_by_tag_name('table')

		row = table.find_elements_by_tag_name('tr')[-1]
		
		date = aDayAgoObj

		pattern = re.compile(r'[\-\d.\d]+')

		click = row.find_elements_by_tag_name('td')[0].text
		clicks = int(pattern.search(click).group(0))

		nSignup = row.find_elements_by_tag_name('td')[1].text
		nSignups = int(pattern.search(nSignup).group(0))

		nDepo = row.find_elements_by_tag_name('td')[2].text
		nDepos = int(pattern.search(nDepo).group(0))

		valDepo = row.find_elements_by_tag_name('td')[8].text
		valDepos = float(pattern.search(valDepo).group(0).replace(',', ''))

		numDepo = row.find_elements_by_tag_name('td')[9].text
		numDepos = int(pattern.search(numDepo).group(0))

		spotsTurn = row.find_elements_by_tag_name('td')[10].text
		spotsTurns = float(pattern.search(spotsTurn).group(0).replace(',', ''))

		numSptBet = row.find_elements_by_tag_name('td')[11].text
		numSptBets = int(pattern.search(numSptBet).group(0))

		acSptUsr = row.find_elements_by_tag_name('td')[12].text
		acSptUsrs = int(pattern.search(acSptUsr).group(0))

		sptNetRev = row.find_elements_by_tag_name('td')[-10].text
		sptNetRevs = float(pattern.search(sptNetRev).group(0).replace(',', ''))

		casinoNetRev = row.find_elements_by_tag_name('td')[-9].text
		casinoNetRevs = float(pattern.search(casinoNetRev).group(0).replace(',', '')) 

		pokerNetRev = row.find_elements_by_tag_name('td')[-8].text
		pokerNetRevs = float(pattern.search(pokerNetRev).group(0).replace(',', '')) 

		bingoNetRev = row.find_elements_by_tag_name('td')[-7].text
		bingoNetRevs = float(pattern.search(bingoNetRev).group(0).replace(',', '')) 

		netRev = row.find_elements_by_tag_name('td')[-6].text
		netRevs = float(pattern.search(netRev).group(0).replace(',', '')) 

		afSpt = row.find_elements_by_tag_name('td')[-5].text
		afSpts = float(pattern.search(afSpt).group(0).replace(',', '')) 

		afCasino = row.find_elements_by_tag_name('td')[-4].text
		afCasinos = float(pattern.search(afCasino).group(0).replace(',', '')) 

		afPoker = row.find_elements_by_tag_name('td')[-3].text
		afPokers = float(pattern.search(afPoker).group(0).replace(',', '')) 

		afBingo = row.find_elements_by_tag_name('td')[-2].text
		afBingos = float(pattern.search(afBingo).group(0).replace(',', '')) 

		commission = row.find_elements_by_tag_name('td')[-1].text
		commissions = float(pattern.search(commission).group(0).replace(',', '')) 

		val = [date, clicks, nSignups, nDepos, valDepos, numDepos, spotsTurns, numSptBets, acSptUsrs, sptNetRevs, casinoNetRevs, pokerNetRevs, bingoNetRevs, netRevs, afSpts, afCasinos, afPokers, afBingos, commissions]
		return val

	finally:
		bet365.quit()
		display.stop()

data = bet365_other_scrapping()

dateStr = data[0]
date = datetime.datetime.strptime(dateStr, '%d/%m/%Y').date()
click = int(data[1])
nSignup = int(data[2])
nDepo = int(data[3])
valDepo = float(data[4])
numDepo = int(data[5])
spotsTurn = float(data[6])
numSptBet = int(data[7])
acSptUsr = int(data[8])
sptNetRev = float(data[9])
casinoNetRev =float(data[10])
pokerNetRev = float(data[11])
bingoNetRev = float(data[12])
netRev = float(data[13])
afSpt = float(data[14])
afCasino = float(data[15])
afPoker = float(data[16])
afBingo = float(data[17])
commission = float(data[18])

# print(date, click, nSignup, nDepo, valDepo, numDepo, spotsTurn, numSptBet, acSptUsr, sptNetRev, casinoNetRev, pokerNetRev, bingoNetRev, netRev, afSpt, afCasino, afPoker, afBingo, commission)
engine = create_engine('postgresql://postgres:root@localhost/kyan')
result = engine.execute("INSERT INTO bet365others (dateto, click, nSignup, nDepo, valDepo, numDepo, spotsTurn, numSptBet, acSptUsr, sptNetRev, casinoNetRev, pokerNetRev, bingoNetRev, netRev, afSpt, afCasino, afPoker, afBingo, commission) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", date, click, nSignup, nDepo, valDepo, numDepo, spotsTurn, numSptBet, acSptUsr, sptNetRev, casinoNetRev, pokerNetRev, bingoNetRev, netRev, afSpt, afCasino, afPoker, afBingo, commission)
