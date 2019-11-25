# -*- coding: UTF-8 -*-
import nonebot
import config
from os import path


# qqbot启动入口
nonebot.init(config)
nonebot.load_plugins(
    path.join(path.dirname(__file__), "awesome", "plugins"),
    "awesome.plugins"
)
nonebot.run()

