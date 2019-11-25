# -*- coding: UTF-8 -*-
import json

from jsonpath import jsonpath

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


async def get_user_best(user, mode, limit_num):
    """
    查询用户最好成绩
    :param user:        osuid
    :param mode:        模式
    :param play_time:   限制显示的数量和
    :return:            显示的成绩dict
    """
    bp_resp = await send_request(part_url=config.GET_USER_BEST_URL, u=user, m=mode, limit=limit_num)
    bp_dict = json.loads(bp_resp)  # 返回列表字典

    # 若查询出为空值 & 出现异常情况 返回空
    if len(bp_dict) == 0 or "error" in bp_dict[0].keys():
        return None

    return bp_dict
