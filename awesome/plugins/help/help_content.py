# -*- coding: UTF-8 -*-
# 因使用read()读取文件出现aiocqhttp.exceptions.ActionFailed异常
# 因此直接使用常量方式直接获取
HELP_CONTEXT = """帮助信息:
1.绑定信息
    !set osu用户名 / 取消绑定 !unset
2.查询信息
    1) 个人信息 !statme (注: 需要绑定账户)
    2) 查询osu玩家信息 !stat osu用户名
3.查询自己最近记录
    1) 自己的最近记录 !recent (注: 需要绑定账户)
    2) 查询自己最近pass记录 !pr
4.查询自己的top
    1) 查询自己的top记录 !bpme (注: 需要绑定账户)
    2) 查询玩家的top记录 !bp osu用户名
5.切换模式
    !set osu/taiko/ctb/mania (注: 需要绑定账户)
5.命令可大小写
    例如: !set | !SET | ！set | ！SET都可
"""
