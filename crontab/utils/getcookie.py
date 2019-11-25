# -*- coding: UTF-8 -*-

import requests
from lxml import etree
from fake_useragent import UserAgent

from awesome.utils.operation_to_mysql import OsuMySQL
from config import MYSQL_TBCOOKIE, LOGIN_OSU_USERNAME, LOGIN_OSU_PASSPORD


class SaveCookie(object):
    def __init__(self):
        self.home_url = "https://osu.ppy.sh/home"
        self.login_url = "https://osu.ppy.sh/session"
        self.login_referer = "https://osu.ppy.sh/home"

        self.mysql_cookie = OsuMySQL()

    @property
    def _set_headers(self):
        """生成headers"""
        return {"User-Agent": UserAgent(verify_ssl=False).random}

    @property
    def _get_login_token(self):
        """登录主页获取token数据"""
        headers = self._set_headers
        # 获取官网主页
        response_html = requests.get(self.home_url, headers=headers)
        element = etree.HTML(response_html.content.decode())
        token = element.xpath("//form/input/@value")
        if len(token) > 0:
            return token[0]
        return None

    @property
    def get_cookie(self):
        """登录osu官网并获取cookies"""
        session = requests.Session()
        headers = self._set_headers  # 设置headers
        headers["referer"] = self.login_referer
        # 设置登录账号和密码
        data = {
            "_token": self._get_login_token,
            "username": LOGIN_OSU_USERNAME,
            "password": LOGIN_OSU_PASSPORD
        }
        response = session.post(self.login_url, headers=headers, data=data)
        return requests.utils.dict_from_cookiejar(response.cookies)

    def save_cookie(self):
        """保存cookie"""
        # 查询数据库是否存在cookie,因为只有一个账号所以只保存一条数据
        try:
            select_all = "select * from {};".format(MYSQL_TBCOOKIE)
            res_select = self.mysql_cookie.query_data(select_all)
            if len(res_select) > 0:
                # 如果有记录则删除
                delete_all = "delete from {};".format(MYSQL_TBCOOKIE)
                self.mysql_cookie.delete_data(delete_all)
            cookie_list = ["{}={}".format(key, value) for key, value in self.get_cookie.items()]
            cookie_value = "|".join(cookie_list)
            # 添加cookie
            insert_sql = "insert into {} values ('{}');".format(MYSQL_TBCOOKIE, cookie_value)
            result = self.mysql_cookie.insert_data(insert_sql)
            print("*" * 50)
            print(result)
            return result
        except:
            return False
        finally:
            self.mysql_cookie.close()


if __name__ == '__main__':
    s = SaveCookie()
    s.save_cookie()

