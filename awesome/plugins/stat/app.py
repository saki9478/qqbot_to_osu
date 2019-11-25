# -*- coding: UTF-8 -*-
import json

import config
from awesome.utils.get_content import send_request
from awesome.utils.operation_to_mysql import OsuMySQL


def get_osu_id(user_id):
    """
    根据qq号查询osu的id
    :param user_id: qq号
    :return: osu_id, mode
    """
    sql_str = "select osu_id, mode from {} where qq_id='{}'".format(config.MYSQL_TBNAME, user_id)
    o = OsuMySQL()
    try:
        result = o.query_data(sql_str)
        o.close()
    except Exception as e:
        o.close()
        return None

    if result:
        return {"osu_id": result[0][0], "mode": result[0][1]}
    return None


async def get_user_json(user, mode):
    """
    :param user: 传入的用户id
    :return: 返回json数据/空值
    """
    json_str = await send_request(part_url=config.GET_URER_URL, u=user, m=mode)
    print(json_str)
    json_dict = json.loads(json_str)  # 返回列表字典
    # 若查询出为空值
    if len(json_dict) == 0:
        return None

    # 出现异常情况 返回空
    if "error" in json_dict[0].keys():
        return None

    return json.loads(json_str)[0]
