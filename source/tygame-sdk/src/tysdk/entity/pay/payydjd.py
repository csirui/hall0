# -*- coding=utf-8 -*-

from xml.etree import ElementTree

from tyframework.context import TyContext

'''<?xml version="1.0" encoding="UTF-8"?>
<request>
<userId>xxx</userId>
<contentId>000000000000</contentId>
<consumeCode>000000000000</consumeCode>
<cpid>701010</cpid>
<hRet>0</hRet>
<status>1800</status>
<versionId>xxx</versionId>
<cpparam>xxx</cpparam>
<packageID></packageID>
</request>'''

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
    'T50K': '001',
    'T60K': '002',
    'T80K': '003',
    'T100K': '004',
    'MOONKEY': '005',
    'MOONKEY3': '006',
    'VOICE100': '007',
    'CARDMATCH10': '008',
    'ZHUANYUN_6': '009',
    'ZHUANYUN_MEZZO': '010',
    'RAFFLE_NEW': '011',
}


class TuYouPayYdjd():
    # 返回接口
    # 标识符        重要性    类型    长度（字节）    描述
    # hRet        M        String    1                0-通知成功； 其它-其他错误
    # message    O        String    24                CP响应的消息，比如“Successful”或是合作方自定义的失败原因。
    XML_RET = '''<?xml version="1.0" encoding="UTF-8"?>
<response>
    <hRet>%d</hRet>
    <message>%s</message>
</response>
'''

    @classmethod
    def doBuyStraight(self, userId, params, mo):
        prodId = params['prodId']
        appId = params['appId']

        if prodId not in paycode_dict:
            mo.setError(-1, u'商品不存在')
            TyContext.ftlog.error('TuYouPayYdjd prodId', prodId, 'not configured, userId=', userId)
            return

        payCode = paycode_dict[prodId]

        '''
        # 炸金花
        if prodId == 'TGBOX1' :
            payCode = '30000827351601'
        if prodId == 'TGBOX2' :
            payCode = '30000827351602'
        if prodId == 'TGBOX3' :
            payCode = '30000827351603'
        if prodId == 'RAFFLE' and str(appId) == '1' :
            payCode = '30000827351604'

        # 德州
        if prodId == 'TEXAS_COIN1' :
            payCode = '30000826652101'
        if prodId == 'TEXAS_COIN6' :
            payCode = '30000826652102'
        if prodId == 'TEXAS_COIN2' :
            payCode = '30000826652103'
        if prodId == 'TEXAS_COIN3' :
            payCode = '30000826652104'
        if prodId == 'TEXAS_COIN_R6' :
            payCode = '30000826652105'
        if prodId == 'TEXAS_COIN_LUCKY_R6' :
            payCode = '30000826652107'

        # 麻将
        if prodId == 'C5' :
            payCode = '30000827347801'
        if prodId == 'C10' :
            payCode = '30000827347802'
        if prodId == 'C5_RAFFLE' :
            payCode = '30000827347803'
        if prodId == 'C2' :
            payCode = '30000827347804'
        if prodId == 'C6' :
            payCode = '30000827347805'
        if prodId == 'C8' :
            payCode = '30000827347806'
        if prodId == 'C6_RAFFLE' :
            payCode = '30000827347807'
        if prodId == 'C8_LUCKY' :
            payCode = '30000827347808'
        if prodId == 'C8_RAFFLE' :
            payCode = '30000827347809'
        '''

        # payCode = '000072803' + payCode
        payData = {'msgOrderCode': payCode}
        params['payData'] = payData
        mo.setResult('payData', payData)
        # ydjd need it to be 16-characters, we have only 14
        orderid = 'XX' + mo.getResult('orderPlatformId')
        mo.setResult('orderPlatformId', orderid)

    @classmethod
    def doYdjdCallback(self, rpath):
        xmldata = TyContext.RunHttp.get_body_content()
        TyContext.ftlog.debug('TuYouPayYdjd.doYdjdCallback in xmldata=', xmldata)
        ret = None
        status = None
        orderPlatformId = None
        try:
            xmlroot = ElementTree.fromstring(xmldata)
            ret = xmlroot.find('hRet').text
            status = xmlroot.find('status').text
            consumeCode = xmlroot.find('consumeCode').text
            orderPlatformId = xmlroot.find('cpparam').text[2:]
        except:
            pass
        if ret is None or status is None or orderPlatformId is None \
                or consumeCode is None:
            msg = 'missing one of hRet, status, consumeCode or cpparam'
            TyContext.ftlog.error('TuYouPayYdjd.doYdjdCallback:', msg)
            return TuYouPayYdjd.XML_RET % (-1, msg)

        from tysdk.entity.pay.pay import TuyouPay
        notifys = {'xml': xmldata, 'third_prodid': consumeCode}
        if ret != '0' or status != '1800':
            msg = 'ret(%s) is not 0 or status(%s) is not 1800' % (ret, status)
            TyContext.ftlog.error('TuYouPayYdjd.doYdjdCallback:', msg)
            TuyouPay.deliveryChargeError(orderPlatformId, notifys, str(ret) + '|' + str(status), 1)
            return TuYouPayYdjd.XML_RET % (-1, msg)

        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, -1, 'TRADE_FINISHED', notifys)
        if isOk:
            return TuYouPayYdjd.XML_RET % (0, 'successful')
        else:
            return TuYouPayYdjd.XML_RET % (-2, 'prod delivery failed')
