### coolq机器人配置

1. 系统：ubuntu16.04，因官方coolq建议使用ubuntu16.04版本

2. python环境：`sudo apt-get install python3.6`

   具体操作看这个

    https://www.jianshu.com/p/e047f3685a64 

   注意：ubuntu默认python为3.5。需要进行升级处理

3. 安装docker：`sudo apt-get install docker.io`

   具体操作

   https://blog.csdn.net/y353027520dx/article/details/88872643 

### 使用docker配置coolq

​	url： [https://cqhttp.cc/docs/4.12/#/?id=%E4%BD%BF%E7%94%A8-docker](https://cqhttp.cc/docs/4.12/#/?id=使用-docker) 

​	代码样例官方：

```shell
# 自己的填写
# 根据注释上的要求进行实际情况填写
$ sudo docker pull richardchien/cqhttp:latest
$ # ftp 将文件夹复制到/home/用户目录
$ sudo docker run -d -ti --rm --name coolq_osu \
             -v $(pwd)/coolq_osu:/home/user/coolq \  # /home/user/coolq不要改动
             -p 9000:9000 \  # noVNC 端口，用于从浏览器控制 酷Q
             -p 5700:5700 \  # HTTP API 插件开放的端口
             -e COOLQ_ACCOUNT=(你的QQ号) \
             -e VNC_PASSWD=(对noVNC设置密码) \  # noVNC密码
             -e CQHTTP_POST_URL=http://本机ip:8080 \
             richardchien/cqhttp:latest
```

然后访问 `http://<虚拟机IP/远程机房公网IP/win下本地的localhost>:9000/`

注意：官方中指出的data\app\io.github.richardchien.coolqhttpapi指适用于win环境下
若是linux中的话，需要在启动之后，直接在根目录下的app目录中进行配置文件设置

### 配置加载文件

将文件直接使用ftp传输的方式导入的linux中



### qqbot配置

1.创建虚拟环境: 

1) 先安装虚拟环境: 

- https://blog.csdn.net/liu_xzhen/article/details/79293373 

- https://blog.csdn.net/jingmin_heijie/article/details/86630005 

2) mkvirtualenv -p python3 qq_osubot

- 操作虚拟环境：

  1 选择虚拟环境：workon qq_osubot

  若前面已经出现(qq_osubot)则不需要执行该步骤

  

  2 进入目录	

- ```shell
  # 将pip设定为清华镜像源
  pip3 install pip3 -U
  pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
  ```

  3 安装python环境包，执行：pip3 install -r requirement 

  4 运行QQbot：python3 QQbot.py

  5 退出虚拟环境：deactivate
  

​	