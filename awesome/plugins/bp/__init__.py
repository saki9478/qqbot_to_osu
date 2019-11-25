# -*- coding: UTF-8 -*-
import nonebot
from nonebot import CommandSession, on_command

import config
from awesome.utils.format_json import format_bp_json
from . import app


@on_command('get_user_best', only_to_me=False,
            aliases=(config.BEST_PLAY, config.BEST_PLAY_FOR_ME, config.BEST_PLAY_UPPER, config.BEST_PLAY_FOR_ME_UPPER))
async def get_user_best(session: CommandSession):
    """查询玩家的最近游玩记录"""
    bot = nonebot.get_bot()
    message_type = session.ctx['message_type']  # 消息类型
    user_id = session.ctx['user_id']  # qq群的qq成员id号
    message = session.ctx['message']  # 发送的信息

    # 判断消息是否为群消息
    if message_type == "group":
        await bot.send(context=session.ctx, message="请稍等，正在查询{}的bp记录".format(user_id))

        # 对命令进行严格限制
        message = str(message)[1:]
        # 对message进行分割
        msg = message.split(" ", 1)

        # 分两种情况一种是[bpme] 一种是[bp, osuplayer]
        if len(msg) == 1:
            # bpme的情况
            if msg[0] == config.BEST_PLAY_FOR_ME or msg[0] == config.BEST_PLAY_FOR_ME_UPPER:
                # 查看个人最好成绩
                # 根据qq用户查询osu_id
                msg = await get_osu_msg(user_id)
                if msg is None:
                    error_msg = "未查询到该用户，请!{}进行绑定".format(config.SET_USR)
                    return await bot.send(context=session.ctx, message=error_msg)

                osu_id = msg.get("osu_id")
                mode = msg.get("mode")
                data_send = await get_user_best(osu_id, mode, config.BP_LIMIT_NUM)
            else:
                error_msg = "格式错误! 请按照!{}形式进行指令发送!".format(config.BEST_PLAY_FOR_ME)
                return await bot.send(context=session.ctx, message=error_msg)

        elif len(msg) == 2:
            # bp osuplayer情况
            if msg[0] == config.BEST_PLAY or msg[0] == config.BEST_PLAY_UPPER:
                osu_user = msg[1]
                mode = 0
                data_send = await get_user_best(osu_user, mode, config.BP_LIMIT_NUM)
            else:
                error_msg = "格式错误! 请按照!{} [username]形式进行指令发送!".format(config.BEST_PLAY)
                return await bot.send(context=session.ctx, message=error_msg)
        else:
            error_msg = "格式错误! 请按照!{} [username]或者!{}形式进行指令发送!".format(config.BEST_PLAY, config.BEST_PLAY_FOR_ME)
            return await bot.send(context=session.ctx, message=error_msg)

        if data_send is None:
            error_msg = "{}用户无历史成绩".format(user_id)
            return await bot.send(context=session.ctx, message=error_msg)

        send_str = format_bp_json(data_send)

        return await bot.send(context=session.ctx, message=send_str)


async def get_osu_msg(user_id):
    """获取osuid"""
    return app.get_osu_id(user_id)


async def get_user_best(osu_id, mode, limit_num):
    """查看玩家的最好成绩"""
    return await app.get_user_best(osu_id, mode, limit_num)
