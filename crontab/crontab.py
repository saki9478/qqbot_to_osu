# -*- coding: UTF-8 -*-
from threading import Timer

from .utils.getcookie import SaveCookie


# 每隔一天秒执行一次任务
def get_cookie_to_mysql():
    cookie = SaveCookie()
    day = 24 * 60 * 60
    t = Timer(day, cookie.save_cookie)
    t.start()


if __name__ == "__main__":
    get_cookie_to_mysql()
