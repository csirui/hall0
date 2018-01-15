# -*- coding=utf-8 -*-

'''
HTTP方法注册的decorating
被修饰的方法, 必须是一个object的子类,即一个class或class的实例
参数:
    httppath,   缺省为空, 含义为: 该方法对应的HTTP的请求路径
    jsonp,      缺省为False, 含义为: 是否返回JSONP的数据类型
    extend_tag, 缺省为None, 含义为: 进行参数检查时的扩展标记
    response,   缺省为json, 含义为: 最终返回的数据格式, 可选择的值为 : json或html
    ip_filter,  缺省为False, 含义为: 不进行IP过滤限制, 
        当为True时,将首先调用方法所在类的ip_filter(ip)方法, 以判定是否要继续进行执行
        ip_filter函数, 拥有一个参数,即当前请求的IP地址,如果不允许改IP访问,那么返回错误信息, 否则返回None,表示可以继续访问
        定义示例:
        def ip_filter(self, ip) :
            if not ip.find('192.168.') == 0 :
                return 'IP被禁止'
            return None
说明:
    当使用这个修饰符时, 修饰符认为将对该方法的所有参数进行检查,并且改方法的名称即为HTTP请求的路径
    例如:
    @http_request_entry
    def do_http_get_room_list(self, userid, clientid) :
        msg = ....
        return msg

    如果未给出httpath参数, 修饰符认为其定义的HTTP请求路径为: 
        htttp://xx.xx.xx/get/room/list?userid=123&clientid=Android
        即将方法名的头"do_http"去掉以后, 替换所有的下划线"_"至路径分隔符"/"

    当收到HTTP请求时, 将进行userid和clientid的检查, 即: 认为方法定义中的userid, clientid为必须检查的参数
    即执行方法所在类的方法:
    def _check_param_userid(self, name, params, extend_tag);
    def _check_param_clientid(self, name, params, extend_tag);
    进行输入参数的检查, 检查的顺序即为方法参数的顺序
    _check_http_param_xxxx方法,
    参数: name 为 参数的名称
        params 已经检查成功的参数的dict集合
    返回两个值:
        第一个值为: 检查的结果, 如果检查失败, 那么直接返回检查结果,结束HTTP请求
                            如果成功, 返回None
        第二个值为: 检查校验后的改参数的值
    参数检查成功后, 将所有检查后的参数值, 传递给原型函数进行执行调用
'''
from tyframework._private_.runmode.http.runhttp_register import http_request_entry

http_request_entry = http_request_entry
