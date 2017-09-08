from selenium_browser import UBrowse
from sqlalchemy import create_engine
from settings.config import *

import psycopg2
import datetime
import time
import json
import requests

class EuroPartners(object):
    """docstring for EuroPartners"""
    def __init__(self):
        self.client = UBrowse()
        
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Length': '8164',
            'Content-Type': 'application/json;charset=utf-8',
            'Host': 'portal.europartners.com',
            'Referer': 'https://portal.europartners.com/portal/',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
            }

    def _create_params(self):
        one_day = datetime.timedelta(days = 1)
        day_now = datetime.datetime.now()
        yesterday = day_now - one_day
        date = yesterday.strftime('%Y-%B-%d')
        # date = yesterday.strftime('%Y-%B-02')

        self.data = '{"report":{"campaignId":"101341","input":[{"name":"startDate","label":"Start Date","type":"date","required":true,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":"yyyy-MM-dd","jsDateTimeFormat":"yy-MM-dd","precision":3,"value":"%s","values":[],"sublist":[]},{"name":"endDate","label":"End Date","type":"date","required":true,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":"yyyy-MM-dd","jsDateTimeFormat":"yy-MM-dd","precision":3,"value":"%s","values":[],"sublist":[]},{"name":"products","label":"Product:","type":"list","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[{"id":"13523839","name":"Casino Tropez"},{"id":"14275502","name":"Luck"},{"id":"13523860","name":"Europa Casino"},{"id":"13523861","name":"Titan Casino"},{"id":"13523863","name":"Titan Poker"},{"id":"13523864","name":"Titan Bet"},{"id":"13523865","name":"Titan Bet UK Casino"},{"id":"13523866","name":"Titan Bet UK Poker"},{"id":"13523867","name":"Titan Bet UK Sport"},{"id":"13523868","name":"Europaplay Casino"},{"id":"13962520","name":"Casino Tropez Ru"},{"id":"13962521","name":"Europa Casino RU"},{"id":"13962522","name":"Titan Casino RU"},{"id":"13962524","name":"Titan Poker RU"},{"id":"13962525","name":"Titan Bet RU"},{"id":"13965943","name":"Redluck RU"}],"sublist":[]},{"name":"producttypes","label":"Product type :","type":"list","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[{"id":"13523838","name":"Casino"},{"id":"13523858","name":"Poker"},{"id":"13523859","name":"Sport"},{"id":"13966461","name":"bingo"}],"sublist":[]},{"name":"profilename","label":"Profile","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"reportBy1","label":"Report By","type":"list","required":true,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":"date","values":[{"id":"date","name":"Stat Date"},{"id":"month","name":"Stat Month"},{"id":"country","name":"Country"},{"id":"platform","name":"Platform"},{"id":"product","name":"Product"},{"id":"producttype","name":"Product type"},{"id":"profile","name":"Profile"},{"id":"var1","name":"Var1"},{"id":"var2","name":"Var2"},{"id":"var3","name":"Var3"},{"id":"var4","name":"Var4"},{"id":"var5","name":"Var5"},{"id":"var6","name":"Var6"},{"id":"var7","name":"Var7"},{"id":"var8","name":"Var8"},{"id":"var9","name":"Var9"},{"id":"var10","name":"Var10"},{"id":"player","name":"Player"}],"sublist":[]},{"name":"reportBy2","label":"Report By","type":"list","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[{"id":"date","name":"Stat Date"},{"id":"month","name":"Stat Month"},{"id":"country","name":"Country"},{"id":"platform","name":"Platform"},{"id":"product","name":"Product"},{"id":"producttype","name":"Product type"},{"id":"profile","name":"Profile"},{"id":"var1","name":"Var1"},{"id":"var2","name":"Var2"},{"id":"var3","name":"Var3"},{"id":"var4","name":"Var4"},{"id":"var5","name":"Var5"},{"id":"var6","name":"Var6"},{"id":"var7","name":"Var7"},{"id":"var8","name":"Var8"},{"id":"var9","name":"Var9"},{"id":"var10","name":"Var10"},{"id":"player","name":"Player"}],"sublist":[]},{"name":"reportBy3","label":"Report By","type":"list","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[{"id":"date","name":"Stat Date"},{"id":"month","name":"Stat Month"},{"id":"country","name":"Country"},{"id":"platform","name":"Platform"},{"id":"product","name":"Product"},{"id":"producttype","name":"Product type"},{"id":"profile","name":"Profile"},{"id":"var1","name":"Var1"},{"id":"var2","name":"Var2"},{"id":"var3","name":"Var3"},{"id":"var4","name":"Var4"},{"id":"var5","name":"Var5"},{"id":"var6","name":"Var6"},{"id":"var7","name":"Var7"},{"id":"var8","name":"Var8"},{"id":"var9","name":"Var9"},{"id":"var10","name":"Var10"},{"id":"player","name":"Player"}],"sublist":[]}],"output":[{"name":"stat_date","label":"Date","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"stat_month","label":"Stat Month","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"platform","label":"Platform","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"product_name","label":"Product","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"profilename","label":"Profile","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"producttype","label":"Product type","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"tlr_amount","label":"Top Level Revenue","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"REAL_CLICKS","label":"Real Clicks","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"CASINO_U_REAL_COUNT","label":"Casino Real Players","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"casino_d_rf_count","label":"Casino RFD Cnt","type":"number","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"casino_net_gaming","label":"Casino Net Gaming","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"POKER_U_REAL_COUNT","label":"Poker Real Players","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"poker_d_rf_count","label":"Poker RFD Cnt","type":"number","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"poker_net_gaming","label":"Poker Net Gaming","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"SPORT_U_REAL_COUNT","label":"Sport Real Players","type":"text","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]},{"name":"sport_d_rf_count","label":"Sport RFD Cnt","type":"number","required":false,"collapsed":false,"filter":false,"internal":false,"dateTimeFormat":null,"jsDateTimeFormat":null,"precision":3,"value":null,"values":[],"sublist":[]}],"language":"EN","name":"Advance Advertiser Stats","id":"1300"},"sc":{"offset":0,"limit":1000,"order":[{"ascending":true,"column":"1"}],"namedQuery":""}}'%(date, date)

    def _get_auth_token(self):
        try:
            self.headers['X-Auth-Token'] = self.client.driver.execute_script("return localStorage.authToken")
        except:
            return False
        return True

    def _get_cookies(self):
        self.cookies = dict()
        cookies = self.client.driver.get_cookies()
        for i in cookies:
            self.cookies[i['name']] = i['value']

    def get_delta_date(self, delta = 1, format_string = "%Y/%m/%d"):
        today = datetime.datetime.today()
        diff = datetime.timedelta(days = delta)
        return (today - diff).strftime(format_string)

    def get_data(self):
        self._get_auth_token()
        url = 'https://portal.europartners.com/portal/rest/reports/run/atOnce'
        response = requests.post(url, headers=self.headers, cookies=self.cookies, data=self.data)
        return response

    def run(self):
        self.client.open_url('https://portal.europartners.com/portal/#/login')
        self.client.set_loginform('//*[@id="userName"]')
        self.client.set_passform('//*[@id="password"]')
        self.client.set_loginbutton('/html/body/div[3]/section/div/form/div[5]/div/input')

        if self.client.login('betfyuk', 'qwerty123') is True:
            time.sleep(3)
            self._get_cookies()
            self._create_params()
        else:
            return False
        return True


if __name__ == '__main__':
    ep = EuroPartners()
    ep.run()
    response = json.loads(ep.get_data().content)

    print(response)

    data = dict()
    if response['data']['values']:
        values = response['data']['values'][0]['data']

        data['tlr_amount'] = values[1]
        data['real_clicks'] = values[2]
        data['casino_u_real_count'] = values[3]
        data['casino_d_rf_count'] = values[4]
        data['casino_net_gaming'] = values[5]
        data['poker_u_real_count'] = values[6]
        data['poker_d_rf_count'] = values[7]
        data['poker_net_gaming'] = values[8]
        data['sport_u_real_count'] = values[9]
        data['sport_d_rf_count'] = values[10]
        data['dateto'] = ep.get_delta_date()

    else:
        data['tlr_amount'] = 0
        data['real_clicks'] = 0
        data['casino_u_real_count'] = 0
        data['casino_d_rf_count'] = 0
        data['casino_net_gaming'] = 0
        data['poker_u_real_count'] = 0
        data['poker_d_rf_count'] = 0
        data['poker_net_gaming'] = 0
        data['sport_u_real_count'] = 0
        data['sport_d_rf_count'] = 0
        data['dateto'] = ep.get_delta_date()

    ep.client.driver.close()

    engine = create_engine(get_database_connection_string())
    
    result = engine.execute("INSERT INTO titanbets (tlr_amount, real_clicks, casino_u_real_count, casino_d_rf_count, casino_net_gaming, poker_u_real_count, poker_d_rf_count, poker_net_gaming, sport_u_real_count, sport_d_rf_count, dateto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", data['tlr_amount'], data['real_clicks'], data['casino_u_real_count'], data['casino_d_rf_count'], data['casino_net_gaming'], data['poker_u_real_count'], data['poker_d_rf_count'], data['poker_net_gaming'], data['sport_u_real_count'], data['sport_d_rf_count'], data['dateto'] )
