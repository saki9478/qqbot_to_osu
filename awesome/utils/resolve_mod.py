# -*- coding: UTF-8 -*-
def resolve(mod_list, value):
    result = []
    # 如果一开始就为0那么直接返回
    if value == 0:
        return [0]

    # 如果不是则进行运算
    while len(mod_list) != 0:
        if mod_list[0] < value:
            new_value = mod_list.pop(0)
            result.append(new_value)
            value = value - new_value
        elif mod_list[0] == value:
            new_value = mod_list.pop(0)
            result.append(new_value)
            break
        else:
            mod_list.pop(0)

        if value == 0:
            break

    return result


if __name__ == '__main__':
    mod_list = [16384, 8192, 4096, 2048, 1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1, 0]
    value = 72
    print(resolve(mod_list, value))
