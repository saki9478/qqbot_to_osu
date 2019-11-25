# -*- coding: UTF-8 -*-
import nonebot
from nonebot import on_command, CommandSession

import config
from awesome.utils.format_json import format_json
from .app import get_user_json


@on_command('search_user', only_to_me=False,
            aliases=(config.SEARCH_USER, config.SEARCH_ME, config.SEARCH_USER_UPPER, config.SEARCH_ME_UPPER))
async def search_user(session: CommandSession):
    """将数据发送给对方客户端"""
    bot = nonebot.get_bot()
    message_type = session.ctx['message_type']  # 消息类型
    message = session.ctx['message']  # 发送的信息
    user_id = session.ctx['user_id']
    # 判断消息是否为群消息
    if message_type == "group":
        await bot.send(context=session.ctx, message="请稍等，正在查询{}玩家信息".format(user_id))
        message = str(message)[1:]
        if message == config.SEARCH_ME or message == config.SEARCH_ME_UPPER:
            # 若直接发送username进行查询则对命令进行分割
            user_id = session.ctx['user_id']
            osu_msg = app.get_osu_id(user_id)
            if not osu_msg:
                return await bot.send(context=session.ctx, message="未查询到该用户，请!set osu_name 进行绑定")
                # 获取osu的id值和模式mode (0 = osu!, 1 = Taiko, 2 = CtB, 3 = osu!mania)
            osu_id = osu_msg.get("osu_id")
            mode = osu_msg.get("mode")
            data_send = await get_user_msg(osu_id, mode)
        elif message == config.SEARCH_USER or config.SEARCH_USER_UPPER:
            # 若直接发送username进行查询则对命令进行分割
            try:
                username = str(message).split(" ", 1)
                username = username[1]
                mode = 0
                data_send = await get_user_msg(username, mode)
            except Exception:
                return await bot.send(context=session.ctx, message="格式错误：请按照!{} 用户名格式进行查询".format(config.SEARCH_USER))
        else:
            return await bot.send(context=session.ctx, message="格式错误：请按照!{} 用户名格式进行查询".format(config.SEARCH_USER))

        if data_send is None:
            return await bot.send(context=session.ctx, message="未查询到该用户")

        # 获取到数据之后提取用户id 用户姓名......
        # 将json数据转化为字符串形式返回给qq客户端
        send_str = format_json(data_send)

        return await bot.send(context=session.ctx, message=send_str)
    else:
        pass


async def get_user_msg(user, mode):
    """发送用户的请求并返回用户响应"""
    return await get_user_json(user, mode)
