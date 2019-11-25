# -*- coding: UTF-8 -*-
import nonebot
from nonebot import on_command, CommandSession

import config
from awesome.plugins.help import help_content
from . import app


@on_command('help_command', only_to_me=False, aliases=(config.HELP, config.HELP_UPPER))
async def help_func(session: CommandSession):
    """将数据发送给对方客户端"""
    # 因使用并非是pro版本，因此只能使用文字进行发送
    bot = nonebot.get_bot()
    message_type = session.ctx['message_type']  # 消息类型
    if message_type == "group":
        return await bot.send(context=session.ctx, message=help_content.HELP_CONTEXT)
