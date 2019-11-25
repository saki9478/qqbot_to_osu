# -*- coding: UTF-8 -*-
import asyncio
import os
import re

import nonebot
from nonebot import CommandSession, on_command

import config
from awesome.utils.format_json import format_recent_json
from awesome.utils.osu_file import OsuFile
from awesome.utils.osu_pp import Calculate

from . import app


@on_command('get_user_recent', only_to_me=False,
            aliases=(config.RECENT, config.RECENT_PASS, config.RECENT_UPPER, config.RECENT_PASS_UPPER))
async def get_user_recent(session: CommandSession):
    """查询玩家的最近游玩记录"""
    bot = nonebot.get_bot()
    message_type = session.ctx['message_type']  # 消息类型
    user_id = session.ctx['user_id']  # qq群的qq成员id号
    message = session.ctx['message']  # 发送的信息

    # 判断消息是否为群消息
    if message_type == "group":
        await bot.send(context=session.ctx, message="请稍等，正在查询{}玩家最近记录".format(user_id))
        # 根据qq用户查询osu_id
        msg = await get_osu_msg(user_id)
        if msg is None:
            error_msg = "未查询到该用户，请!{}进行绑定".format(config.SET_USR)
            return await bot.send(context=session.ctx, message=error_msg)

        # 对命令进行严格限制
        message = str(message)[1:]
        if message == config.RECENT or message == config.RECENT_UPPER:
            # 查询该玩家历史记录
            osu_id = msg.get("osu_id")
            mode = msg.get("mode")
            temp = await play_recent(osu_id, mode, config.GET_NUM)
            if temp is None:
                error_msg = "{}最近并未游玩任何记录".format(user_id)
                return await bot.send(context=session.ctx, message=error_msg)
            recent, osu_map = temp
        elif message == config.RECENT_PASS or message == config.RECENT_PASS_UPPER:
            # 查询该玩家pass历史记录
            osu_id = msg.get("osu_id")
            mode = msg.get("mode")
            temp = await play_recent(osu_id, mode, config.GET_MANY_NUM)
            if temp is None:
                error_msg = "{}最近并未游玩任何记录".format(user_id)
                return await bot.send(context=session.ctx, message=error_msg)
            recent, osu_map = temp
        else:
            error_msg = "命令格式错误！请输入!{}或者!{}即可".format(config.RECENT, config.RECENT_PASS)
            return await bot.send(context=session.ctx, message=error_msg)

        if config.PP_START:
            # 获取到的数据进行stars和pp计算
            # 1.获取文件
            calculate = Calculate(recent, osu_map)
            osu_file_name = calculate.get_osu_file_name()

            # 发送打阿里云是否存在文件
            osu_file = OsuFile(osu_file_name, beatmap_id=osu_map["beatmap_id"], beatmapset_id=osu_map["beatmapset_id"])
            is_exist = await osu_file.file_is_exist()
            # await get_send_str_by_osu(osu_file, osu_file_name, calculate, session, bot, recent, osu_map)

            if is_exist is False:
                # 从官方下图获取osu文件对发送数据进行整合
                await get_send_str_by_osu(osu_file, osu_file_name, calculate, session, bot, recent, osu_map)
            else:
                # 从阿里云云存储下载osu文件对发送的数据进行整合
                await get_send_str_by_ali(osu_file, osu_file_name, calculate, session, bot, recent, osu_map)
        else:
            # 如果不启用pp则直接
            send_str = format_recent_json(recent, osu_map)
            return await bot.send(context=session.ctx, message=send_str)


async def get_osu_msg(user_id):
    """获取osuid"""
    return app.get_osu_id(user_id)


async def play_recent(osu_id, mode, play_time):
    """获取玩家的历史记录"""
    return await app.play_recent(osu_id, mode, play_time)


async def get_send_str_by_osu(osu_file, osu_file_name, calculate, session, bot, recent, osu_map):
    """获取官网beatmap进行osu数据整合"""
    # 对数据进行格式化
    # 在官网上下载文件并保存到临时目录
    await osu_file.get_osu_file()

    # 获取文件并计算
    osu_file_name = re.sub(r"\<|\>|\/|\\|\||\:|\"|\*|\?", "", osu_file_name)
    osu_file_name = config.OSU_TEMP_DOWNLOAD_DIR + osu_file_name
    stars, pp_value = calculate.calculate_osu_pp(osu_file_name)
    # 对数据进行格式化
    send_str = format_recent_json(recent, osu_map, stars, pp_value)

    # 对osu文件进行上传
    await osu_file.upload_all_osu_file()

    # 删除本地所有的文件
    await osu_file.delete_local_all_file()

    # 如果直接在qq上返回输出文字，则无法进行下面的操作，和return一
    return await bot.send(context=session.ctx, message=send_str)


async def get_send_str_by_ali(osu_file, osu_file_name, calculate, session, bot, recent, osu_map):
    """通过从阿里云存储服务器中获取osu数据进行数据的整合"""
    # 发送下载命令
    await osu_file.get_oss_file()
    # 等待文件下载
    i = 0
    osu_file_name = re.sub(r"\<|\>|\/|\\|\||\:|\"|\*|\?", "", osu_file_name)
    while not os.path.exists(config.OSU_TEMP_DOWNLOAD_DIR + osu_file_name):
        # 若三次等待时间之内未跳出循环，则进行异常通知
        await asyncio.sleep(config.WAIT_TIME)
        if i < 3:
            error_msg = "osu文件请求超时"
            return await bot.send(context=session.ctx, message=error_msg)
        i += 1
    osu_file_name = config.OSU_TEMP_DOWNLOAD_DIR + osu_file_name
    stars, pp_value = calculate.calculate_osu_pp(osu_file_name)
    # 对数据进行格式化
    send_str = format_recent_json(recent, osu_map, stars, pp_value)
    # 删除文件
    await osu_file.delete_local_file()
    return await bot.send(context=session.ctx, message=send_str)

