# 创建数据库
create database osudb default charset=utf8;

# 进入数据库
use osudb;

# 创建数据表
create table osuinformation(
    qq_id varchar(20) primary key,
    osu_id varchar(20) not null,
    mode varchar(2) not null default 0
);

# 设置cookie表
create table cookie(
    cookie text
);