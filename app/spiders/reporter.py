import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from env import *
from sqlalchemy import create_engine
from sqlalchemy import create_engine
from ..models import Log, db
import datetime

class SpiderReporter(object):
    """docstring for SpiderLoger"""
    def __init__(self):
        self.temp = 0

    def write_error_log(self, provider, message, created_at):
        if ENV == 'dev':
            self.write_db(provider, message, created_at)
        else:
            # Writing to DB.
            pass

    def write_log(self, provider, message, created_at, type = 'info'):
        if type == 'error':
            self.write_error_log(provider, message, created_at)
        elif ENV == 'dev':
            print(message)
        else:
            print(message)

    def write_db(self, provider, message, created_at):
        log = Log(
            affiliate = provider,
            message = message,
            created_at = created_at
        )
        db.session.add(log)
        db.session.commit()
        # engine = create_engine(get_database_connection_string())
        # result = engine.execute("INSERT INTO logs (provider, message, created_at) VALUES (%s, %s, %s);", provider, message, created_at)

if __name__ == "__main__":
    report = SpiderReporter()