# -*- coding=utf-8 -*-

import copy
from xml.etree import ElementTree

from helper import PayHelper
from tyframework.context import TyContext

'''回调POST的XML数据样例：
<?xml version="1.0" encoding="UTF-8"?>
<request>
<userId>1396032000</userId>
<contentId>621216015822</contentId>
<consumeCode>006041203002</consumeCode>
<cpid>772212</cpid>
<hRet>0</hRet>
<status>1800</status>
<versionId>21120</versionId>
<cpparam>XXc00601yGIlBS58</cpparam>
<packageID/>
</request>

其中cpid为cp标识，contentId为应用标识，consumeCode的后三位为支付时所指定的计费点。
无签名验证机制。
'''

status_dict = {
    "3004": "渠道鉴权未通过（渠道安全策略）",
    "1501": "机型不匹配",
    "3012": "PC验证码购买道具成功",
    "3010": "PC请求消费并产生验证码的请求成功",
    "3011": "PC请求消费并产生验证码的请求失败",
    "8007": "PC道具数量不合法",
    "8008": "PC消费次数超限制",
    "8009": "PC金额超限制（外码1）",
    "8009": "PC金额未超限制（外码0）",
    "8011": "PC验证码不存在或验证码验证请求处理失败",
    "8010": "PC验证码上传超时",
    "1621": "用户已经“沉迷”",
    "209": "自动充值超过次上限",
    "1800": "计费成功",
    "1900": "包体安全性校验失败",  # 使用移动游戏SDK接入网游业务，在自测阶段，
    # 出现此付费结果状态码是正常现象
    "1901": "非单点激活类业务不允许激活操作",
    "1902": "大厅渠道计费透传接口返回失败",
    "1903": "计费失败",
    "1904": "第三方安全服务器校验session失败",
    "1905": "对方用户不存在或状态不正常",
    "1906": "计费策略传入错误",
    "1907": "校验SC计费事务失败",
    "1908": "短信验证码校验失败",
    "1909": "VCODE不合法",
    "1910": "图形验证码校验失败",
    "1911": "其他错误",
    "1912": "计费策略不支持支付密码模式",
}

paycode_dict = {
    # 斗地主商品
    # 'T50K' : '001',
    # 'T80K' : '003',
    # 'T100K' : '004',
    # 'MOONKEY' : '005',
    # 'MOONKEY3' : '006',
    # 'VOICE100' : '007',
    # 'CARDMATCH10' : '008',
    # 'ZHUANYUN_6' : '009',
    'TY9999D0006001': '002',
    'TY9999D0008002': '010',
    'TY9999D0008001': '011',
    'TY9999R0008001': '012',
}


class TuYouPayYdjd(object):
    # 返回接口
    # 标识符        重要性    类型    长度（字节）    描述
    # hRet        M        String    1                0-通知成功； 其它-其他错误
    # message    O        String    24                CP响应的消息，比如“Successful”或是合作方自定义的失败原因。
    XML_RET = '''<?xml version="1.0" encoding="UTF-8"?><response><hRet>%d</hRet><message>%s</message></response>
'''

    @classmethod
    def charge_data(cls, chargeinfo):
        appId = chargeinfo['appId']
        buttonId = chargeinfo['buttonId']
        clientId = chargeinfo['clientId']
        userId = chargeinfo['uid']
        clientip = TyContext.UserSession.get_session_client_ip(userId)
        from tysdk.entity.pay_common.fengkong import Fengkong
        if Fengkong.is_ip_limited(clientip, clientId, 'ydjd'):
            raise TyContext.FreetimeException(
                1, '对不起，您已超出支付限制，请联系客服4008-098-000')
        paycodes = TyContext.Configure.get_global_item_json('paycodes', clientid=clientId)
        if paycodes:
            try:
                pdata = paycodes['ydjd']['paydata']
                for data in pdata:
                    if data['prodid'] == buttonId:
                        break
                else:
                    raise Exception('product %s not found in paycodes(%s) config' % (buttonId, clientId))
                cdata = copy.deepcopy(data)
                del cdata['prodid']
                chargeinfo['chargeData'] = cdata
            except Exception as e:
                TyContext.ftlog.error('TuYouPayYdjd.charge_data->config error:', paycodes, 'exception:', e)
                raise e
            return

        paycodes = TyContext.Configure.get_global_item_json('ydjd_paycodes', paycode_dict)
        if buttonId not in paycodes[str(appId)]:
            TyContext.ftlog.error('TuYouPayYdjd buttonId', buttonId,
                                  'not configured, paycodes=', paycodes)
            return
        paycode = paycodes[str(appId)][buttonId]
        chargeinfo['chargeData'] = {'msgOrderCode': paycode}

    @classmethod
    def doYdjdCallback(self, rpath):
        xmldata = TyContext.RunHttp.get_body_content()
        TyContext.ftlog.debug('TuYouPayYdjd.doYdjdCallback in xmldata=', xmldata)
        notifys = {'xml': xmldata, 'chargeType': 'ydjd'}

        try:
            xmlroot = ElementTree.fromstring(xmldata)
            ret = xmlroot.find('hRet').text
            status = xmlroot.find('status').text
            userId = xmlroot.find('userId').text
            contentId = xmlroot.find('contentId').text
            consumeCode = xmlroot.find('consumeCode').text
            orderPlatformId = xmlroot.find('cpparam').text[2:]
        except Exception as e:
            msg = 'failure'
            TyContext.ftlog.error('TuYouPayYdjd.doYdjdCallback:', msg, e)
            return TuYouPayYdjd.XML_RET % (1, msg)

        notifys['pay_appid'] = contentId
        notifys['third_prodid'] = consumeCode
        notifys['third_userid'] = userId

        if ret != '0' or status != '1800':
            msg = 'ret(%s) is not 0 or status(%s) is not 1800' % (ret, status)
            TyContext.ftlog.error('TuYouPayYdjd.doYdjdCallback:', msg)
            PayHelper.callback_error(orderPlatformId, msg, notifys)
            return TuYouPayYdjd.XML_RET % (1, 'failure')

        isOk = PayHelper.callback_ok(orderPlatformId, -1, notifys)
        if isOk:
            return TuYouPayYdjd.XML_RET % (0, 'successful')
        else:
            return TuYouPayYdjd.XML_RET % (1, 'failure')
