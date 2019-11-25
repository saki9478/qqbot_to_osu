# -*- coding: UTF-8 -*-
def accuracy(c300, c100, c50, cmiss):
    """
    准确度 = 准确度总计/（点击总计*300）
    点击总计 = （点击失误总数+ 点击50总数 + 点击100总数 +点击300总数)
    准确度总计 = (玩家点击50总数*50 + 玩家点击100总数*100 + 玩家点击300总数*300)
    """
    total_click_num = c300 + c100 + c50 + cmiss
    total_acc_num = c50 * 50 + c100 * 100 + c300 * 300
    return total_acc_num / (total_click_num * 300) * 100