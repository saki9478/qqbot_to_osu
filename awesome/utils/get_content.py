# -*- coding: UTF-8 -*-
import requests
from fake_useragent import UserAgent

import config


async def send_request(part_url, **kwargs):
    """
    发送url获取api中的json参数
    :param part_url: 传入的部分url
    :param kwargs: requests模块中params参数
    :return: json信息
    """
    try:
        send_url = config.BASE_URL.format(part_url)
        headers = {"User-Agent": UserAgent(verify_ssl=False).random}
        kwargs["k"] = config.API_KEY
        response = requests.get(send_url, headers=headers, params=kwargs)
    except Exception as e:
        return {"error": "请求失败"}

    return response.content.decode()
