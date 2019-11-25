# -*- coding: UTF-8 -*-
# 获取api中模式所对应的值
mod_dict = dict(NONE=0,  # api中的None
                NF=1, EZ=2, TD=4, HD=8, HR=16, SD=32,
                DT=64, RX=128, HF=256, NC=512, FL=1024,
                Auto=2048, SO=4096, RX2=8192, PF=16384, )

# 对字典进行翻转
reverse_mod_dict = {value: key for key, value in mod_dict.items()}

# 获取mod的值
mod_value = [i for i in mod_dict.values()]

# 对mod列表进行翻转
reverse_mod_value = mod_value[::-1]

# mode
mode_dict = {0: "osu", 1: "taiko", 2: "ctb", 3: "mania"}

# 翻转mode
reverse_mode_dict = {value: key for key, value in mode_dict.items()}

if __name__ == '__main__':
    print(mod_value)
    print(reverse_mod_value)
