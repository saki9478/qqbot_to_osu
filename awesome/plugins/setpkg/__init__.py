# -*- coding: UTF-8 -*-
import nonebot
from nonebot import on_command, CommandSession

import config
from awesome.utils.format_json import format_json
from . import app
from config import mode_dict, reverse_mode_dict


@on_command('set_user', only_to_me=False, aliases=(config.SET_USR, config.SET_USR_UPPER))
async def set_user(session: CommandSession):
    """将用户数据和osuid数据进行绑定"""
    bot = nonebot.get_bot()
    message_type = session.ctx['message_type']  # 消息类型
    user_id = session.ctx['user_id']  # qq群的qq成员id号
    message = session.ctx['message']  # 发送的信息

    # 判断消息是否为群消息
    if message_type == "group":
        # 若直接发送username进行查询则对命令进行分割
        try:
            osu_user = str(message).split(" ", 1)
            osu_user = osu_user[1]
        except Exception:
            error_msg = "格式错误：请按照!{} 用户名 格式进行查询".format(config.SET_USR)
            return await bot.send(context=session.ctx, message=error_msg)

        # 对该用户进行查询验证
        await bot.send(context=session.ctx, message="正在验证：{}".format(osu_user))
        data_send = await set_user_msg(osu_user)
        if data_send is None:
            return await bot.send(context=session.ctx, message="未查询到该用户")

        send_str = format_json(data_send)
        await bot.send(context=session.ctx, message=send_str)

        # 校验完成之后对数据进行提取保存
        osu_id = data_send.get("user_id")
        mode = 0
        result = await save_user_msg(user_id, osu_id, mode)
        return await bot.send(context=session.ctx, message=result)


@on_command('unset_user', only_to_me=False, aliases=(config.UNSET_USER, config.UNSET_USER_UPPER))
async def unset_user(session: CommandSession):
    """注销绑定"""
    bot = nonebot.get_bot()
    message_type = session.ctx['message_type']  # 消息类型
    user_id = session.ctx['user_id']  # qq群的qq成员id号
    # 判断消息是否为群消息
    if message_type == "group":
        message = session.ctx['message']
        message = str(message)[1:]
        if message == config.UNSET_USER or message == config.UNSET_USER_UPPER:
            result = await delete_user_msg(user_id)
            return await bot.send(context=session.ctx, message=result)
        else:
            error_msg = "指令错误，请输入!{}即可".format(config.UNSET_USER)
            return await bot.send(context=session.ctx, message=error_msg)



@on_command('switch_mode', only_to_me=False, aliases=(config.MODE, config.MODE_UPPER))
async def switch_mode(session: CommandSession):
    """注销绑定"""
    bot = nonebot.get_bot()
    message_type = session.ctx['message_type']  # 消息类型
    user_id = session.ctx['user_id']  # qq群的qq成员id号
    message = session.ctx['message']
    # 判断消息是否为群消息
    if message_type == "group":
        # 根据qq用户查询osu_id
        msg = await get_osu_msg(user_id)
        if msg is None:
            error_msg = "未查询到该用户，请!{}进行绑定".format(config.SET_USR)
            return await bot.send(context=session.ctx, message=error_msg)

        # 对命令进行严格限制 命令格式!mode osu(taiko ctb mania)
        message = str(message)[1:]
        msg_list = message.split(" ", 1)
        if len(msg_list) != 2:
            error_msg = "请按照!{} osu(taiko, ctb, mania)格式进行切换, 可大小写".format(config.MODE)
            return await bot.send(context=session.ctx, message=error_msg)
        # 如果命令格式不对也要进行格式写法提醒
        try:
            mode = msg_list[1]
        except Exception as e:
            error_msg = "请按照!{} osu(taiko, ctb, mania)格式进行切换, 可大小写".format(config.MODE)
            return await bot.send(context=session.ctx, message=error_msg)
        # 对模式格式写法错误也要进行写法提醒
        if mode.lower() not in mode_dict.values():
            error_msg = "请按照!{} osu(taiko, ctb, mania)格式进行切换, 可大小写".format(config.MODE)
            return await bot.send(context=session.ctx, message=error_msg)

        # 将数据中的mode字段进行修改操作
        mode = reverse_mode_dict[mode]
        result = await update_mode(user_id, mode)
        if not result:
            error_msg = "{}:模式未保存成功".format(user_id)
            return await bot.send(context=session.ctx, message=error_msg)

        return await bot.send(context=session.ctx, message=result)


async def set_user_msg(user):
    """发送用户的请求并返回用户响应"""
    return await app.get_user_json(user)


async def save_user_msg(user_id, osu_id, mode):
    """保存用户信息"""
    return app.save_user(user_id, osu_id, mode)


async def delete_user_msg(user_id):
    """删除用户信息"""
    return app.logout_user(user_id)


async def get_osu_msg(user_id):
    """查询用户信息"""
    return app.get_osu_id(user_id)


async def update_mode(user_id, mode):
    """修改字段"""
    return app.update_mode(user_id, mode)
