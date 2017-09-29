
from env import *
from sqlalchemy import create_engine
from app import scheduler
from ..models import Log, db
import datetime

class SpiderReporter(object):
    """docstring for SpiderLoger"""
    def __init__(self):
        self.temp = 0

    def write_error_log(self, provider, message, created_at):
        self.write_db(provider, message, created_at)

    def write_log(self, provider, message, created_at, type = 'info'):
        if type == 'error':
            print(message)
            self.write_error_log(provider, message, created_at)
        elif ENV == 'dev':
            print(message)
        else:
            print(message)

    def write_db(self, provider, message, created_at):
        app = scheduler.app
        with app.app_context():
            try:
                log = Log(
                    affiliate = provider,
                    message = message,
                    created_at = created_at
                )
                db.session.add(log)
                db.session.commit()
                return True
            except Exception as e:
                print("Failed to write error logs.")
                print(str(e))
                return False

if __name__ == "__main__":
    report = SpiderReporter()