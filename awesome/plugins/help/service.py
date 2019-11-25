# -*- coding: UTF-8 -*-
def get_help_content():
    """读取文档，因文档内容比较简短，可一次性取出"""
    content = ""
    with open("help_content.py", "r", encoding="utf-8") as f:
        content += f.read()
    return content


if __name__ == '__main__':
   print(get_help_content())