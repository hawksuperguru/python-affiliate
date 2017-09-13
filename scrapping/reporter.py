from settings.config import *
from sqlalchemy import create_engine
from sqlalchemy import create_engine

import datetime

class SpiderReporter(object):
    """docstring for SpiderLoger"""
    def __init__(self):
        self.temp = 0

    def write_error_log(self, provider, message):
        if ENV == 'dev':
            print(message)
        else:
            # Writing to DB.
            pass

    def write_log(self, provider, message, type = 'info'):
        if type == 'error':
            self.write_error_log(message)
        elif ENV == 'dev':
            print(message)
        else:
            pass

    def write_db(self, message):
        engine = create_engine(get_database_connection_string())
        result = engine.execute("INSERT INTO bet10s (merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regytd, ndytd, commiytd, impreto, clito, regto, ndto, commito, dateto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regytd, ndytd, commiytd, impreto, clito, regto, ndto, commito, dateto)

if __name__ == "__main__":
    report = SpiderLoger()