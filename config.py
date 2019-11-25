# -*- coding: UTF-8 -*-
import os
from datetime import timedelta


# QQbot参数信息
HOST = "0.0.0.0"
PORT = 8080                                            # 事件端口

ACCESS_TOKEN = ""                                      # access_token
SECRET = ""                                            # secret

DEBUG = True                                           # 调试模式
SUPERUSERS = {1984594680}                              # QQ号，可以填多个
NICKNAME = {'bot'}
SESSION_RUN_TIMEOUT = timedelta(seconds=10)
COMMAND_START = {"!", "！"}                            # 触发指令
COMMAND_SEP = {' '}                                    # 指令分割符
APSCHEDULER_CONFIG = {'apscheduler.timezone': 'Asia/Shanghai'}  # 定时任务时间参数

# 设定等待时间
WAIT_TIME = 2.0                                        # 下载osu文件时等待时间

# 设定根路径
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # 项目的根目录
OSU_TEMP_DOWNLOAD_DIR = BASE_DIR + "\\osu_file\\"      # 存储osu文件的临时目录

# mysql配置
MYSQL_UNAME = "root"
MYSQL_PASSWD = "123456"
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DBNAME = "osudb"
MYSQL_TBNAME = "osuinformation"                         # 管理所有的osu账户
MYSQL_TBCOOKIE = "cookie"                               # 管理登录的cookie值

# 阿里云oss配置信息
ACCESSKEYID = ""
ACCESSKEYSECRET = ""
BUCKETNAME = ""
# ENDPOINT = "oss-cn-shanghai.aliyuncs.com"             # 上海云存储服务节点
# ENDPOINT = "oss-cn-beijing.aliyuncs.com"              # 北京云存储服务节点
ENDPOINT = "oss-us-west-1.aliyuncs.com"                 # 美国硅谷云存储服务节点

# 设置osu账户
LOGIN_OSU_USERNAME = ""                                 # osu登录用户名
LOGIN_OSU_PASSPORD = ""                                 # osu登录密码

# 配置api参数
BASE_URL = "https://osu.ppy.sh{}"                       # 拼接url基本格式
MAP_SEARCH_BASE_URL = "https://osu.ppy.sh/beatmapsets?q={}"           # 官网搜图url基本格式
MAP_DOWNLOAD_BASE_URL = "https://osu.ppy.sh/beatmapsets/{}/download"  # 官网下图url的基本格式
MAP_BASE_URL = "https://osu.ppy.sh/b/{}"                # 拼接图的url基本格式
GET_NUM = "1"                                           # 获取数量
GET_MANY_NUM = "10"                                     # 获取最近的10次记录
BP_LIMIT_NUM = "5"                                      # bp限制的数量

# api url
# 参考：https://github.com/ppy/osu-api/wiki
API_KEY = ""                                            # 需要到官网进行获取
GET_URER_URL = "/api/get_user"                          # 获取用户信息
GET_SCORES_URL = "/api/get_scores"                      # 检索有关指定节拍图的前100个得分的信息
GET_USER_BEST_URL = "/api/get_user_best"                # 获取指定用户的最高分数
GET_USER_RECENT = "/api/get_user_recent"                # 获取玩家最近游玩数据
GET_MAP = "/api/get_beatmaps"                           # 获取铺面的信息

# pp相关参数
PP_START = True                                         # 启动pp的计算

# 特殊玩法mod难度
mod_dict = dict(NONE=0,  # api中的None
                NF=1, EZ=2, TD=4, HD=8, HR=16, SD=32,
                DT=64, RX=128, HF=256, NC=512, FL=1024,
                Auto=2048, SO=4096, RX2=8192, PF=16384, )               # 难度对应的值
reverse_mod_dict = {value: key for key, value in mod_dict.items()}      # 对上面的字典进行翻转
mod_value = [i for i in mod_dict.values()]                              # 获取mod难度的值

# 模式mode
mode_dict = {0: "osu", 1: "taiko", 2: "ctb", 3: "mania"}                # mode
reverse_mode_dict = {value: key for key, value in mode_dict.items()}    # 翻转mode

# osu查询命令
HELP = "help"                                           # 帮助
HELP_UPPER = "HELP"                                     # (大写)帮助
SEARCH_USER = "stat"                                    # 根据osu玩家名称进行查询
SEARCH_USER_UPPER = "STAT"                              # (大写)根据osu玩家名称进行查询
SEARCH_ME = "statme"                                    # 查询自己的排名等成绩
SEARCH_ME_UPPER = "STATME"                              # (大写)查询自己的排名等成绩
SET_USR = "set"                                         # 绑定qq号和osuid
SET_USR_UPPER = "SET"                                   # (大写)绑定qq号和osuid
UNSET_USER = "unset"                                    # 注销绑定
UNSET_USER_UPPER = "UNSET"                              # (大写)注销绑定
RECENT = "recent"                                       # 查询个人最近游玩的成绩
RECENT_UPPER = "RECENT"                                 # (大写)查询个人最近游玩的成绩
RECENT_PASS = "pr"                                      # 查询个人最近pass图成绩
RECENT_PASS_UPPER = "PR"                                # (大写)查询个人最近pass图成绩
MODE = "mode"                                           # 切换其他模式
MODE_UPPER = "MODE"                                     # (大写)切换其他模式
BEST_PLAY = "bp"                                        # 查看玩家的最好成绩
BEST_PLAY_UPPER = "BP"                                  # (大写)查看玩家的最好成绩
BEST_PLAY_FOR_ME = "bpme"                               # 查看自己的最好成绩
BEST_PLAY_FOR_ME_UPPER = "BPME"                         # (大写)查看自己的最好成绩
