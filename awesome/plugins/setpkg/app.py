# -*- coding: UTF-8 -*-
import json

import config
from awesome.utils.get_content import send_request
from awesome.utils.operation_to_mysql import OsuMySQL
from config import mode_dict


async def get_user_json(user):
    """
    :param user: 传入的用户id
    :return: 返回json数据/空值
    """
    json_str = await send_request(part_url=config.GET_URER_URL, u=user)
    json_dict = json.loads(json_str)  # 返回列表字典
    # 若查询出为空值
    if len(json_dict) == 0:
        return None

    # 出现异常情况 返回空
    if "error" in json_dict[0].keys():
        return None

    return json.loads(json_str)[0]


def get_osu_id(user_id):
    """
    根据qq号查询osu的id
    :param user_id: qq号
    :return:        osu_id, mode
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


def save_user(user_id, osu_id, mode):
    """
    对数据进行保存操作
    :param user_id: 用户的qq号
    :param osu_id:  osuid
    :param mode:    游玩模式
    :return:        ok
    """
    o = OsuMySQL()
    try:
        # 保存时先进行是否存在的校验
        sql_str = "select osu_id, mode from {} where qq_id='{}'".format(config.MYSQL_TBNAME, user_id)
        select_result = o.query_data(sql_str)
        if select_result:
            return "{}: 该账号已经被绑定过了".format(user_id)
        # 没有查询出值则进行保存处理
        sql = "insert into {} values ('{}', '{}', '{}');".format(config.MYSQL_TBNAME, user_id, osu_id, mode)
        result = o.insert_data(sql)
    except Exception as e:
        o.close()
        return "查询发生异常"
    if result:
        return "{}我已经记住你的名字啦！".format(user_id)
    return "发生异常"


def update_mode(user_id, mode):
    """
    对模式进行修改
    :param user_id: 用户的qq号
    :param mode:    模式 0 1 2 3
    :return:        保存成功信息
    """
    o = OsuMySQL()
    try:
        sql_str = "update {} SET mode={} where qq_id={}".format(config.MYSQL_TBNAME, mode, user_id)
        result = o.update_data(sql_str)
    except Exception as e:
        o.close()
        return None
    if not result:
        return None
    return "{}模式修改完成".format(mode_dict[mode])


def logout_user(user_id):
    """
    接触qq用户和osu账户的绑定
    :param user_id:  qq号
    :return:         删除成功信息
    """
    o = OsuMySQL()
    try:
        sql_str = "delete from {} where qq_id='{}'".format(config.MYSQL_TBNAME, user_id)
        o.delete_data(sql_str)
    except Exception as e:
        o.close()
        return

    return "{}不要丢下我，呜呜呜！！！！".format(user_id)
