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
        sql = f'INSERT INTO {table} (id, title, author, startDate, lastDate, view) VALUES (? ? ? ? ? ? ? ? ?)'
        cursor = self.conn.cursor()
        cursor.excute(sql, data)

    def updateData(self, table, data):
        sql = f'UPDATE SET {table} id=? title=? author=? startDate=? lastDate=? view=?'
        cursor = self.conn.cursor()
        cursor.excute(sql, data * 2)

    def insertOrUpdateData(self, table, data):
        sql = f'INSERT INTO {table} (id, title, author, startDate, lastDate, view) VALUES (? ? ? ? ? ? ? ? ?)'
        sql += ' ON DUPLICATE KEY UPDATE id=? title=? author=? startDate=? lastDate=? view=?'
        cursor = self.conn.cursor()
        cursor.excute(sql, data * 2)
