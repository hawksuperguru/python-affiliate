#!/bin/python
# -*- coding: utf-8 -*-

from env import *

if ENV == 'dev':
    # DB_PROVIDER = 'mysql'
    DB_PROVIDER = 'postgresql'
    DB_NAME = 'affiliate'
    DB_USERNAME = 'postgres'
    DB_PASSWORD = 'postgres'
    DB_HOST = 'localhost'
    CHROME_DRIVER_PATH = "../chrome/chromedriver.exe"
    PG_DUMP_PATH = 'C:/Program Files/PostgreSQL/9.6/bin/pg_dump.exe'
    PG_BACKUP_PATH =  'F:/workspace/Kyan/affiliate/affiliate/storage'
elif ENV == 'staging':
    # DB_PROVIDER = 'mysql'
    DB_PROVIDER = 'postgresql'
    DB_NAME = 'affiliate'
    DB_USERNAME = 'postgres'
    DB_PASSWORD = 'y7I0]QfHBRKCvWp'
    DB_HOST = 'localhost'
    CHROME_DRIVER_PATH = "/usr/local/bin/chromedriver"
    PG_DUMP_PATH = 'pg_dump'
    PG_BACKUP_PATH = '/var/www/html/flaskapp/storage'
else:
    # DB_PROVIDER = 'mysql'
    DB_PROVIDER = 'postgresql'
    DB_NAME = 'kyan'
    DB_USERNAME = 'postgres'
    DB_PASSWORD = 'root'
    DB_HOST = 'localhost'
    CHROME_DRIVER_PATH = "../chrome/chromedriver"
    PG_DUMP_PATH = 'pg_dump'
    PG_BACKUP_PATH = '/var/www/html/flaskapp/storage'

def get_database_connection_string():
    if DB_PROVIDER == 'mysql':
        return "mysql+pymysql://{0}:{1}@{2}/{3}".format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME)
    elif DB_PROVIDER == 'postgresql':
        # postgresql://postgres:postgres@localhost/kyan
        return "postgresql://{0}:{1}@{2}/{3}".format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME)
    else:
        return None