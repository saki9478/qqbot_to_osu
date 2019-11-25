# -*- coding: utf-8 -*-
import os, shutil
import re
import zipfile

import requests
from fake_useragent import UserAgent

import config
import lib.alioss
from awesome.utils.operation_to_mysql import OsuMySQL


class OsuFile(object):
    def __init__(self, file_name, beatmap_id=None, beatmapset_id=None):
        self.ali = lib.alioss.AliOss()
        self.file_name = re.sub(r"\<|\>|\/|\\|\||\:|\"|\*|\?", "", file_name)
        self.search_url = config.MAP_SEARCH_BASE_URL.format(beatmap_id)
        self.map_download_url = config.MAP_DOWNLOAD_BASE_URL.format(beatmapset_id)

        self.mysql_cookie = OsuMySQL()

    async def file_is_exist(self):
        """判断文件是否存在"""
        return self.ali.file_is_exist(self.file_name)

    async def get_oss_file(self):
        """下载获取oss存储服务器中的文件"""

        file_path = config.OSU_TEMP_DOWNLOAD_DIR + self.file_name
        self.ali.download_file(self.file_name, file_path)

    async def get_osu_file(self):
        """下载osu官网下的文件，并将osu文件保存到oss存储服务器中"""
        # 从官网下载文件
        # 从数据库中获取cookie字符串
        # 设置headers
        headers = {"User-Agent": UserAgent(verify_ssl=False).random}

        # 下载osz的二进制文件
        response = requests.get(self.map_download_url, headers=headers)

        # 下载完成之后保存到本地, 把文件名中win禁止的文件字符名剔除
        zip_name = self.file_name.rsplit(" (", 1)[0]
        zip_osu_file = re.sub(r"\<|\>|\/|\\|\||\:|\"|\*|\?", "", zip_name)
        with open(config.OSU_TEMP_DOWNLOAD_DIR + zip_osu_file + ".zip", "wb") as f:
            f.write(response.content)
        # 保存完成进行解压
        zip_name = config.OSU_TEMP_DOWNLOAD_DIR + zip_osu_file + ".zip"  # 压缩文件名
        mk_zip_file_dir = config.OSU_TEMP_DOWNLOAD_DIR + zip_osu_file  # 准备创建新文件夹的路径

        r = zipfile.is_zipfile(zip_name)
        if r:
            # 创建目录
            os.makedirs(mk_zip_file_dir)
            # 将zip文件移动到该目录中
            shutil.move(zip_name, mk_zip_file_dir)
            # 此时文件位置在
            new_file_path = mk_zip_file_dir + "\\" + zip_osu_file + ".zip"  # 移动zip后的文件路径
            # 进行解压操作
            fz = zipfile.ZipFile(new_file_path, 'r')
            for file in fz.namelist():
                fz.extract(file, mk_zip_file_dir)

            # 解压完成遍历移动到临时存放目录进行文件读取
            for root, dirs, files in os.walk(mk_zip_file_dir):
                for file in files:
                    if file.endswith('.osu'):
                        # 进行文件移动操作
                        osu_file_path = mk_zip_file_dir + "\\" + file
                        shutil.move(osu_file_path, config.OSU_TEMP_DOWNLOAD_DIR)

    async def upload_all_osu_file(self):
        """上传临时文件目录内所有的osu文件"""
        try:
            for root, dirs, files in os.walk(config.OSU_TEMP_DOWNLOAD_DIR):
                for file in files:
                    if file.endswith('.osu'):
                        self.ali.upload_local_file(file, config.OSU_TEMP_DOWNLOAD_DIR + file)
        except:
            pass

    async def delete_local_all_file(self):
        """删除所有无用的文件"""
        try:
            # 获取文件目录名
            del_dir_name = self.file_name.rsplit(" (", 1)[0]
            del_dir_name = re.sub(r"\<|\>|\/|\\|\||\:|\"|\*|\?", "", del_dir_name)
            # 首先将目录中的所有的子文件删除
            for root, dirs, files in os.walk(config.OSU_TEMP_DOWNLOAD_DIR + del_dir_name):
                for file in files:
                    os.remove(config.OSU_TEMP_DOWNLOAD_DIR + del_dir_name + "\\" + file)

            # 最后删除空目录
            if os.path.exists(config.OSU_TEMP_DOWNLOAD_DIR + del_dir_name):
                # 删除目录, 若直接使用remove删除会出现permission权限异常
                os.rmdir(config.OSU_TEMP_DOWNLOAD_DIR + del_dir_name)

            # 删除osu后缀文件
            # 拆分文件名提出标题
            for root, dirs, files in os.walk(config.OSU_TEMP_DOWNLOAD_DIR):
                for file in files:
                    if file.endswith('.osu'):
                        os.remove(config.OSU_TEMP_DOWNLOAD_DIR + file)
        except:
            pass

    async def delete_local_file(self):
        """删除本地单个的osu文件，腾出空间"""
        if os.path.exists(config.OSU_TEMP_DOWNLOAD_DIR + self.file_name):
            os.remove(config.OSU_TEMP_DOWNLOAD_DIR + self.file_name)
            return True
        return False


if __name__ == '__main__':
    pass
