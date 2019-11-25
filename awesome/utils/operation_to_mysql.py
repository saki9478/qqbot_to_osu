# -*- coding: UTF-8 -*-
# 定义一个函数，完成数据库的连接
from pymysql import connect

from config import MYSQL_UNAME, MYSQL_PASSWD, MYSQL_HOST, MYSQL_PORT, MYSQL_DBNAME


class OsuMySQL(object):
    def __init__(self):
        try:
            self.conx = connect(user=MYSQL_UNAME, password=MYSQL_PASSWD,
                                host=MYSQL_HOST, port=MYSQL_PORT, database=MYSQL_DBNAME)
            self.cs = self.conx.cursor()
        except Exception as e:
            raise Exception(e)

    def query_data(self, sql_str):
        """查询数据库的个别字段值"""
        self.cs.execute(sql_str)
        self.conx.commit()
        res = self.cs.fetchall()
        return res

    def insert_data(self, sql_str):
        """将数据插入到数据库中"""
        self.cs.execute(sql_str)
        self.conx.commit()
        return True

    def update_data(self, sql_str):
        """将数据进行修改"""
        self.cs.execute(sql_str)
        self.conx.commit()
        return True

    def delete_data(self, sql_str):
        """删除该用户记录，因为是个人bot，不采取使用update方式删除"""
        self.cs.execute(sql_str)
        self.conx.commit()

    def close(self):
        self.cs.close()
        self.conx.close()
