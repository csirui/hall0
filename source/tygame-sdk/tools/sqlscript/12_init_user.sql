#初始化步骤如下,服务器部分根据所部署的服务器选择执行

#以root用户登录mysql
mysql -u root


#------------------------测试服务器(IP: 192.168.10.19)---------------#

#创建用户并赋权
grant all on *.* to 'tuyoogame'@'localhost' identified by 'tuyoogame';
grant all on *.* to 'tuyoogame'@'192.168.10.19' identified by 'tuyoogame';

#刷新权限
flush privileges;

#查看权限
show grants for tuyoogame@localhost;
show grants for tuyoogame@192.168.10.19;

#------------------------测试服务器(IP: 192.168.10.19)---------------#

#------------------------测试服务器(IP: 192.168.10.22)---------------#

#创建用户并赋权
grant all on *.* to 'tuyoogame'@'localhost' identified by 'tuyoogame';
grant all on *.* to 'tuyoogame'@'192.168.10.22' identified by 'tuyoogame';

#刷新权限
flush privileges;

#查看权限
show grants for tuyoogame@localhost;
show grants for tuyoogame@192.168.10.22;

#------------------------测试服务器(IP: 192.168.10.22)---------------#


#------------------------AWS线上服务器(公网IP： 54.169.186.105  内网IP: 172.31.1.196 域名：mania.shediao.com)---------------#

#创建用户并赋权
grant all on *.* to 'tuyoogame'@'localhost' identified by 'tuyoogame';
grant all on *.* to 'tuyoogame'@'172.31.6.73' identified by 'tuyoogame';

#刷新权限
flush privileges;

#查看权限
show grants for tuyoogame@localhost;
show grants for tuyoogame@172.31.1.196;

#------------------------AWS线上服务器(公网IP： 54.169.186.105  内网IP: 172.31.1.196 域名：mania.shediao.com)---------------#

#------------------------国内线上服务器(公网IP： 192.10.3.0.29  内网IP: 10.3.0.29 域名：mania-china.shediao.com)---------------#

#创建用户并赋权
grant all on *.* to 'tuyoogame'@'localhost' identified by 'tuyoogame';
grant all on *.* to 'tuyoogame'@'192.10.3.0.29' identified by 'tuyoogame';

#刷新权限
flush privileges;

#查看权限
show grants for tuyoogame@localhost;
show grants for tuyoogame@172.31.1.196;

#------------------------国内线上服务器(公网IP： 192.10.3.0.29  内网IP: 10.3.0.29 域名：mania-china.shediao.com)---------------#


#使用tuyoogame用户登录
mysql -u tuyoogame -p
#输入密码 tuyoogame

#初始化表
source /home/sdk/source/tygame-sdk/tools/sqlscript/20140830.sql;
source /home/sdk/source/tygame-sdk/tools/sqlscript/table_ads.sql;
source /home/sdk/source/tygame-sdk/tools/sqlscript/table_avatar.sql;
source /home/sdk/source/tygame-sdk/tools/sqlscript/tygame12.sql;


#以下是用户反馈的初始化脚本，暂不执行
#游戏服中有接口存储用户反馈内容，是通过文本文件存档，暂时先采用游戏中存档的方式，后续可以调整为
#source /home/sdk/source/tygame-sdk/tools/sqlscript/table_feedback.sql
