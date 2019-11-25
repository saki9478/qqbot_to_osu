# -*- coding: UTF-8 -*-

from awesome.utils.calculate_accuracy import accuracy
from awesome.utils.resolve_mod import resolve
from config import *


def format_json(data_send):
    """
    将数据进行转化成所需要输出的数据
    """
    username = data_send["username"]
    pp_rank = data_send["pp_rank"]
    pp_raw = data_send["pp_raw"]
    level = float(data_send["level"])
    total_score = format(int(data_send["total_score"]), ",")
    accuracy = float(data_send["accuracy"])
    playcount = data_send["playcount"]
    send_str = "用户名: {}\n世界排名: {}\npp值: {}\n等级: {:.2f}\n总分: {}\n精确度: {:.2f}%\n游玩次数: {}". \
        format(username, pp_rank, pp_raw, level, total_score, accuracy, playcount)

    return send_str


def format_recent_json(recent_dict, map_dict, stars=None, pp_value=None):
    """
    将数据进行格式化字符串输出
    """
    # recent_dict数据
    # "beatmap_id": "987654",
    # "score": "1234567",
    # "maxcombo": "421",
    # "count50": "10",
    # "count100": "50",
    # "count300": "300",
    # "countmiss": "1",
    # "countkatu": "10",
    # "countgeki": "50",
    # "perfect": "0",
    # "enabled_mods": "76",
    # "user_id": "1",
    # "date": "2013-06-22 9:11:16",
    # "rank": "SH"

    # map_dict数据
    # {"beatmapset_id":"13019", "beatmap_id":"48416", "approved":"2", "total_length":"202",
    # "hit_length":"185", "version":"BASARA", "file_md5":"bcfbb61d5a6156fa9fb0708432c79d88",
    # "diff_size":"4", "diff_overall":"7", "diff_approach":"9", "diff_drain":"8",
    # "mode":"0", "count_normal":"789", "count_slider":"80", "count_spinner":"1",
    # "submit_date":"2010-02-12 10:17:22", "approved_date":"2010-12-28 22:17:38",
    # "last_update":"2010-09-08 10:10:59", "artist":"Daisuke Achiwa",
    # "title":"BASARA", "creator":"100pa-", "creator_id":"231631", "bpm":"130",
    # "source":"Ar tonelico II",
    # "tags":"ar tonelico ii 2","genre_id":"2",...

    # 对数据进行提取
    title = map_dict["title"]
    creator = map_dict["creator"]
    version = map_dict["version"]
    beatmap_id = map_dict["beatmap_id"]
    score = format(int(recent_dict["score"]), ",")
    maxcombo = int(recent_dict["maxcombo"])
    count50 = int(recent_dict["count50"])
    count100 = int(recent_dict["count100"])
    count300 = int(recent_dict["count300"])
    countmiss = int(recent_dict["countmiss"])
    countkatu = recent_dict["countkatu"]
    countgeki = recent_dict["countgeki"]
    perfect = "yes" if recent_dict["perfect"] == 1 else "no"
    int_mods = int(recent_dict["enabled_mods"])
    rank = recent_dict["rank"]

    # 对模式进行分解提取
    reverse_mod_value = mod_value[::-1]
    enabled_mods = resolve(reverse_mod_value, int_mods)
    enabled_mods = [reverse_mod_dict[i] for i in enabled_mods]
    enabled_mods = " ".join(enabled_mods)

    # acc计算
    acc_num = "{:.2f}%".format(accuracy(count300, count100, count50, countmiss))

    # map的url地址
    map_url = MAP_BASE_URL.format(beatmap_id)

    if stars is not None and pp_value is not None:
        # 如果有pp值则格式化带有pp值的字符串
        send_str = """图名: {}\n作图者: {}\n难度: {} ({} stars)\n玩家成绩: {}\n最大连击数: {}\n300: {}\t激: {}\n100: {}\t喝: {}\n50 : {}\tmiss: {}\nperfect: {}\tmod: {}\nacc: {}\trank: {}\npp: {}\n地址: {}"""
        send_str = send_str.format(title, creator, version, stars, score, maxcombo, count300, countgeki,
                                   count100, countkatu, count50, countmiss, perfect, enabled_mods,
                                   acc_num, rank, pp_value, map_url)
    else:
        # 否则不带参数进行格式化数据
        send_str = """图名: {}\n作图者: {}\n难度: {}\n玩家成绩: {}\n最大连击数: {}\n300: {}\t激: {}\n100: {}\t喝: {}\n50 : {}\tmiss: {}\nperfect: {}\tmod: {}\nacc: {}\trank: {}\n地址: {}"""
        send_str = send_str.format(title, creator, version, score, maxcombo, count300, countgeki,
                                   count100, countkatu, count50, countmiss, perfect, enabled_mods,
                                   acc_num, rank, map_url)

    return send_str


def format_bp_json(json_dict):
    """将bp数据进行格式化输出"""
    # [{
    #      "beatmap_id": "1582674",
    #      "score_id": "2791309545",
    #      "score": "5320058",
    #      "maxcombo": "472",
    #      "count50": "0",
    #      "count100": "28",
    #      "count300": "325",
    #      "countmiss": "0",
    #      "countkatu": "21",
    #      "countgeki": "64",
    #      "perfect": "0",
    #      "user_id": "3117824",
    #      "date": "2019-04-27 13:52:15",
    #      "rank": "S",
    #      "pp": "467.557"
    #      "replay_available": "1"
    #      }, {...}, ...]
    send_str = ""
    for d in json_dict:
        url = MAP_BASE_URL.format(d["beatmap_id"])
        # score = format(int(d["score"]), ",")
        rank = d["rank"]
        pp = int(float(d["pp"]))
        enabled_mods = int(d["enabled_mods"])
        # 对模式进行分解提取
        reverse_mod_value = mod_value[::-1]
        enabled_mods = resolve(reverse_mod_value, enabled_mods)
        enabled_mods = [reverse_mod_dict[i] for i in enabled_mods]
        enabled_mods = " ".join(enabled_mods)
        # 格式化输出的str
        temp = "map地址: {}\nrank: {}   pp值: {}   mod: {}".format(url, rank, pp, enabled_mods)
        if 0 < json_dict.index(d) < len(json_dict):
            send_str += "\n\n"
        send_str += temp

    return send_str
