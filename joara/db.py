import os
import configparser as cf

import mariadb

class DB(object):
    def __init__(self):
        path = os.path.realpath(__file__)
        path = os.path.dirname(path) + '/'

        config = cf.ConfigParser()
        config.read(path + 'db.conf')

        dbconf = config['MariaDB']
        host = dbconf['Host']
        port = int(dbconf['Port'])
        username = dbconf['User']
        password = dbconf['Password']
        db = dbconf['DB']

        self.conn = mariadb.connect(host=host, port=port, username=username, password=password, database=db)

    def insertData(self, table, data):
        sql = f'INSERT INTO {table} () VALUES ()'
        cursor = self.conn.cursor()
        cursor.excute(sql, data)