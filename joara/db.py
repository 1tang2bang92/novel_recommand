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
        conn = mariadb.connect(host=host, port=port, username=username, password=password, database=db)
        self.conn = conn
        self.cursor = conn.cursor()

    def insertData(self, table, data):
        sql = f'INSERT INTO {table} (bookid, title, author, genre, view, recommand, size, start_date, last_date) VALUES {data}'
        self.cursor.execute(sql)
        self.conn.commit()

    def updateData(self, table, data):
        sql = f'UPDATE SET {table} id=? title=? author=? startDate=? lastDate=? view=?'
        cursor = self.cursor
        cursor.execute(sql, data * 2)
        self.conn.commit()

    def insertOrUpdateData(self, table, data):
        sql = f'INSERT INTO {table} (id, title, author, startDate, lastDate, view) VALUES (? ? ? ? ? ? ? ? ?)'
        sql += ' ON DUPLICATE KEY UPDATE id=? title=? author=? startDate=? lastDate=? view=?'
        cursor = self.cursor
        cursor.execute(sql, data * 2)
        self.conn.commit()
