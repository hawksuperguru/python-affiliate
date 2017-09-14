#!/bin/python
# -*- coding: utf-8 -*-

from time import gmtime, strftime
from scrapping.settings.config import *
from scrapping.reporter import SpiderReporter

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
        dumper = """ "%s" --host=%s --username=%s --format=p --file=%s --inserts %s  """

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
        
        # def log(string):
        #     print time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime()) + ": " + str(string)
        
        # # Change the value in brackets to keep more/fewer files. time.time() returns seconds since 1970...
        # # currently set to 2 days ago from when this script starts to run.
        
        # x_days_ago = time.time() - ( 60 * 60 * 24 * 2 )
        
        # os.putenv('PGPASSWORD', self.password)
        
        # database_list = subprocess.Popen('echo "select datname from pg_database" | psql -t -U %s -h %s template1' % (USER,HOST) , shell=True, stdout=subprocess.PIPE).stdout.readlines()
        
        # # Delete old backup files first.
        # for database_name in database_list :
        #     database_name = database_name.strip()
        #     if database_name == '':
        #         continue
        
        #     glob_list = glob.glob(BACKUP_DIR + database_name + '*' + '.pgdump')
        #     for file in glob_list:
        #         file_info = os.stat(file)
        #         if file_info.st_ctime < x_days_ago:
        #             log("Unlink: %s" % file)
        #             os.unlink(file)
        #         else:
        #             log("Keeping : %s" % file)
        
        # log("Backup files older than %s deleted." % time.strftime('%c', time.gmtime(x_days_ago)))
        
        # # Now perform the backup.
        # for database_name in database_list :
        #     log("dump started for %s" % database_name)
        #     thetime = str(strftime("%Y-%m-%d-%H-%M")) 
        #     file_name = database_name + '_' + thetime + ".sql.pgdump"
        #     #Run the pg_dump command to the right directory
        #     command = dumper % (USER,  BACKUP_DIR + file_name, database_name)
        #     log(command)
        #     subprocess.call(command,shell = True)
        #     log("%s dump finished" % database_name)

        # log("Backup job complete.")