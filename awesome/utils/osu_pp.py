import pyttanko as osu


class Calculate(object):
    def __init__(self, recent_dict, map_dict, is_search_map=False):
        self.title = map_dict["title"]
        self.creator = map_dict["creator"]
        self.version = map_dict["version"]
        self.artist = map_dict["artist"]
        self.maxcombo = int(recent_dict["maxcombo"])
        self.count50 = int(recent_dict["count50"])
        self.count100 = int(recent_dict["count100"])
        self.count300 = int(recent_dict["count300"])
        self.countmiss = int(recent_dict["countmiss"])
        self.int_mods = int(recent_dict["enabled_mods"])

        # 是否对图进行查询
        self.is_search_map = is_search_map

    def calculate_osu_pp(self, osu_file, mods=0):
        """
        计算pp
        :param osu_file:    file osu后缀名的文件
        :param mods:        int 模式 HR HD DT NF等，可调用api进行查看
        :param n300:        int 300
        :param n100:        int 100
        :param n50:         int 50
        :param nmiss:       int miss
        :param combo:       int 最大的连击数
        :return:            (str stars星级, str pp点)
        """
        p = osu.parser()
        with open(osu_file, "r", encoding="utf-8") as f:
            bmap = p.map(f)

        stars = osu.diff_calc().calc(bmap)
        if self.is_search_map is True:
            pp, _, _, _, _ = osu.ppv2(stars.aim, stars.speed, bmap=bmap, mods=mods)
        else:
            pp, _, _, _, _ = osu.ppv2(
                stars.aim, stars.speed, bmap=bmap, mods=self.int_mods,
                n300=self.count300, n100=self.count100, n50=self.count50,
                nmiss=self.countmiss, combo=self.maxcombo
            )

        # pp, _, _, _, _ = osu.ppv2(
        #     stars.aim, stars.speed, bmap=bmap, mods=mods,
        #     n300=n300, n100=n100, n50=n50, nmiss=nmiss,
        #     combo=combo
        # )
        return "{:.1f}".format(stars.total), "{}".format(int(pp))

    def get_osu_file_name(self):
        return "{} - {} ({}) [{}].osu".format(self.artist, self.title, self.creator, self.version)

