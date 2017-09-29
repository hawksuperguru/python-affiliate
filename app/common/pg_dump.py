#!/bin/python
# -*- coding: utf-8 -*-

from time import gmtime, strftime
from app.spiders.reporter import SpiderReporter
from app.spiders.env import *

import subprocess
import os
import glob
import time

class Backup(object):
    """
    This class can backup a specific database with bluk inserts
    """
    def __init__(self):
        self.username = DB_USERNAME
        self.password = DB_PASSWORD
        self.hostname = DB_HOST
        self.pg_dump_path = PG_DUMP_PATH
        self.pg_backup_path = PG_BACKUP_PATH
        self.report = SpiderReporter()

    def log(self, message, type = 'info'):
        if type == 'info':
            self.report.write_log("Backup", message, strftime("%Y-%m-%d"))
        else:
            self.report.write_error_log("Backup", message, strftime("%Y-%m-%d"))

    def dump(self, db_name = DB_NAME):
        # try:
        glob_list = glob.glob(self.pg_backup_path + '/' + db_name + '*' + '.sql')
        for file in glob_list:
            self.log("Unlink: %s" % file)
            os.unlink(file)

        os.putenv('PGPASSWORD', self.password)
        dumper = """ "%s" --host=%s --username=%s --format=p --file=%s --dbname=%s --inserts  """

        self.log("dump started for %s" % db_name)
        now = str(strftime("%Y-%m-%d-%H-%M")) 
        file_name = db_name + '_' + now + ".sql"
        command = dumper % (self.pg_dump_path, self.hostname, self.username, self.pg_backup_path + '/' + file_name, db_name)
        self.log(command)
        subprocess.call(command, shell = True)
        self.log("%s dump finished" % db_name)
        return {'full_path': self.pg_backup_path + '/' + file_name, 'file_name': file_name}
        # return file_name

if __name__ == "__main__":
    me = Backup()
    me.dump()