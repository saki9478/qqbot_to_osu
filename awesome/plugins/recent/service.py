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


async def play_recent(user, mode, play_time):
    """
    根据osu_id查询历史记录
    :param osu_id:  osu玩家的id号
    :return:        dict
    """
    recent_resp = await send_request(part_url=config.GET_USER_RECENT, u=user, m=mode, limit=play_time)
    recent_dict = json.loads(recent_resp)  # 返回列表字典
    # 若查询出为空值 & 出现异常情况 返回空
    if len(recent_dict) == 0 or "error" in recent_dict[0].keys():
        return None

    if play_time == config.GET_NUM:
        # 获取当前谱面的id
        beatmap_id = recent_dict[0]["beatmap_id"]
        recent_dict = recent_dict[0]
    elif play_time == config.GET_MANY_NUM:
        rank_list = jsonpath(recent_dict, "$..rank")
        try:
            i = rank_list.index("F")
        except Exception as e:
            return None
        if i <= 0:
            return None
        recent_dict = recent_dict[i - 1]
        beatmap_id = recent_dict["beatmap_id"]
    else:
        return None

    # 再次对谱面信息进行查询
    map_resp = await send_request(part_url=config.GET_MAP, b=beatmap_id)
    map_dict = json.loads(map_resp)  # 返回列表字典

    # 若查询出为空值 & 出现异常情况 返回空
    if len(map_dict) == 0 or "error" in recent_dict.keys():
        return None

    return recent_dict, map_dict[0]
