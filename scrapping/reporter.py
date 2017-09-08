from settings.config import *
from sqlalchemy import create_engine
import datetime

class SpiderReporter(object):
    """docstring for SpiderLoger"""
    def __init__(self):
        self.temp = 0

    def write_error_log(self, message):
        if ENV == 'dev':
            print(message)
        else:
            # Writing to DB.
            pass

    def write_log(self, message, type = 'info'):
        if type == 'error':
            self.write_error_log(message)
        elif ENV == 'dev':
            print(message)
        else:
            pass

if __name__ == "__main__":
    report = SpiderLoger()