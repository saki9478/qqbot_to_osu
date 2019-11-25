### 1.运行环境
python版本: python3.6
酷q软件: coolq air
系统环境: windows server/ubuntu 16.04

### 2.酷q软件获取
根据以下地址按照官网上获取coolq软件和插件即可: 
https://cqhttp.cc/

### 3.运行coolq
#### 1) win环境下运行
只需要将下载好的文件进行解压进入，找到"CQA.exe"文件双击运行即可

#### 2) ubuntu环境下运行
根据如下地址使用docker的方式配置coolq环境: 
https://cqhttp.cc/docs/4.12/#/?id=%E4%BD%BF%E7%94%A8-docker
也可以根据"coolq机器人配置.md"进行配置

### 4.运行QQbot.py程序
运行: `python QQbot.py`
后台运行: `pythonw QQbot.py`
输出日志: `pythonw QQbot.py > qqbot.log`

### 5.发送指令
在发送指令的前提是要让qq bot加入该群
以下指令全是根据配置文件进行发送，用户可自行根据配置文件进行命令的相应调整
#### 命令1 !stat/STAT [osu player name]
查询osu_用户排名等信息

#### 命令2 !statme/STATME
查询自己排名等信息(前提先!set绑定用户)

#### 命令3 !set/SET [osu player name]
绑定qq号和osuid号

#### 命令4 !unset/UNSET
解除绑定

#### 命令5 !recent/RECENT
查看最近的成绩不分pass

#### 命令6 !pr/PR
查看最近的pass的成绩

#### 命令7 !mode/MODE osu(osu, taiko, ctb, mania)
切换模式~~~~

### 注意点：
因为牵扯到qq的运算，所以需要安装pp算法模块
##### 模块地址：
https://github.com/Francesco149/pyttanko
##### 安装方法
进入目录找到setup.py文件，进行`python setup.py install`安装即可

### 计算pp下图功能注意
下载图必须要有cookie只要另执行`python crontab/crontab.py`即可


