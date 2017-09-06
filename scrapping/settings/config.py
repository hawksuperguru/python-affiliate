#!/bin/python
# -*- coding: utf-8 -*-

from env import *

if ENV == 'dev':
    # DB_PROVIDER = 'mysql'
    DB_PROVIDER = 'postgresql'
    DB_NAME = 'kyan'
    DB_USERNAME = 'postgres'
    DB_PASSWORD = 'postgres'
    DB_HOST = 'localhost'
    CHROME_DRIVER_PATH = "../chrome/chromedriver.exe"
elif ENV == 'staging':
    # DB_PROVIDER = 'mysql'
    DB_PROVIDER = 'postgresql'
    DB_NAME = 'kyan'
    DB_USERNAME = 'postgres'
    DB_PASSWORD = 'postgres'
    DB_HOST = 'localhost'
    CHROME_DRIVER_PATH = "./chrome/chromedriver"
else:
    # DB_PROVIDER = 'mysql'
    DB_PROVIDER = 'postgresql'
    DB_NAME = 'kyan'
    DB_USERNAME = 'postgres'
    DB_PASSWORD = 'postgres'
    DB_HOST = 'localhost'
    CHROME_DRIVER_PATH = "./chrome/chromedriver"

def get_database_connection_string():
    if DB_PROVIDER == 'mysql':
        return "mysql+pymysql://{0}:{1}@{2}/{3}".format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME)
    elif DB_PROVIDER == 'postgresql':
        # postgresql://postgres:postgres@localhost/kyan
        return "postgresql://{0}:{1}@{2}/{3}".format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME)
    else:
        return None