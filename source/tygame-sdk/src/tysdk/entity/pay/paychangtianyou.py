# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
import json
from hashlib import md5
from xml.etree import ElementTree

import datetime
import time

from tyframework.context import TyContext
from tysdk.entity.paythird.helper import PayHelper


class TuYouChangeTianYou(object):
    '''
    CompanyID 1051 
    提交key:dfdf67
    回调key:756ffh 
    接口密码:m1n2b3
    厂商查询地址:http://wr.800617.com:6003/App/Admin/Logon.aspx
    用户名:bjtyzx 
    密码:123456（请厂商自行修改）
    正式服务器地址:http://wr.800617.com:6001/submit.aspx 
    短信签名:tygame 中文
    '''

    @classmethod
    def doChangTianYouChargeRequest(cls, gameId, userId, mo, couponCount, money):
        if TyContext.RunHttp.getRequestParam('chargePhone') == None:
            return False
        else:
            chargePhone = TyContext.RunHttp.getRequestParam('chargePhone')
            chargePhone = int(chargePhone.strip().replace(' ', ''))
            idcard = TyContext.RunHttp.getRequestParam('idcard')
            uname = TyContext.RunHttp.getRequestParam('name')

        ct = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        clientId = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'sessionClientId')
        clientId = str(clientId)
        orderId = TyContext.ServerControl.makeChangTianYouOrderIdV3(userId, gameId, clientId)

        TyContext.ftlog.info('doChangTianYouChargeRequest', userId, chargePhone, couponCount, money, orderId)
        mo.setResult('chargeId', orderId)
        mo.setResult('userId', userId)

        datas = {'amount': couponCount, 'phone': chargePhone, 'idcard': idcard, 'uname': uname, 'state': 0, 'rtime': ct,
                 'money': money}
        datas = json.dumps(datas)
        TyContext.RedisPayData.execute('HSET', 'cty:' + str(gameId) + ':' + str(userId), orderId, datas)
        TyContext.RedisPayData.execute('SADD', 'cty:' + str(gameId) + ':request', orderId + '.' + str(userId))

        isenable = TyContext.Configure.get_global_item_int('coupon.auto.confirm', 1)
        if not isenable:
            return True

        gamelimits = TyContext.Configure.get_global_item_json('coupon.day.auto.limited',
                                                              {'8': {'user': 100, 'game': 1000}})
        if str(gameId) in gamelimits:  # 德州扑克特殊处理
            day_max = gamelimits[str(gameId)]['user']
            datas = TyContext.Day1st.get_datas(userId, gameId)
            coupon10_flag = datas.get('coupon.day.auto', 0)
            if coupon10_flag > day_max:
                # 需要人工审核
                return True

            gamekey = 'coupon.day.auto.limited.' + datetime.datetime.now().strftime('%Y%m%d')
            game_max = gamelimits[str(gameId)]['game']
            gmax = TyContext.RedisMix.execute('HGET', gamekey, gameId)
            if gmax > game_max:
                # 需要人工审核
                return True

            datas['coupon.day.auto'] = coupon10_flag + money
            TyContext.Day1st.set_datas(userId, gameId, datas)
            TyContext.RedisMix.execute('HINCRBY', gamekey, gameId, money)

            # 自动审核通过
            mo2 = TyContext.Cls_MsgPack()
            TyContext.RunHttp.set_request_arg('chargeUserId', userId)
            TyContext.RunHttp.set_request_arg('chargeOrderId', orderId)
            cls.doChangTianYouChargeConfirm(gameId, mo2)
            TyContext.ftlog.info('doChangTianYouChargeRequest->confirm mo22=', mo2.packJson())

            return True

        # 新增逻辑:玩家当日首次兑换10元自动审核，其他额度或非当日首次兑换需要人工审核
        if int(money) == 10:
            datas = TyContext.Day1st.get_datas(userId, gameId)
            if 'coupon10_flag' in datas and datas['coupon10_flag'] == 1:
                return True
            else:
                mo2 = TyContext.Cls_MsgPack()
                TyContext.RunHttp.set_request_arg('chargeUserId', userId)
                TyContext.RunHttp.set_request_arg('chargeOrderId', orderId)
                cls.doChangTianYouChargeConfirm(gameId, mo2)
                TyContext.ftlog.info('doChangTianYouChargeRequest->confirm mo2=', mo2.packJson())

                datas['coupon10_flag'] = 1
                TyContext.Day1st.set_datas(userId, gameId, datas)
        return True

    @classmethod
    def doChangTianYouChargeConfirm(cls, gameId, mo):
        chargeUserId = TyContext.RunHttp.getRequestParamInt('chargeUserId')
        orderId = TyContext.RunHttp.getRequestParam('chargeOrderId', '')
        if len(orderId) <= 8:
            mo.setError(1, 'order id is empty')
            return mo
        TyContext.ftlog.info('doChangTianYouChargeConfirm', chargeUserId, orderId)

        datas = TyContext.RedisPayData.execute('HGET', 'cty:' + str(gameId) + ':' + str(chargeUserId), orderId)
        if datas == None:
            mo.setError(1, 'the order id error!' + orderId)
            return

        datas = json.loads(datas)
        if datas['state'] != 0:
            mo.setError(1, 'the order state error!' + orderId)
            return mo

        phone = datas['phone']
        money = int(datas['money'])
        money = money * 100

        sendOrderId = orderId + '.' + str(gameId) + '.' + str(chargeUserId)
        # sendOrderId = '201310312O'
        md5code = '1051' + 'm1n2b3' + str(phone) + str(money) + str(sendOrderId) + 'dfdf67'
        TyContext.ftlog.debug('md5code=', md5code)
        m = md5()
        m.update(md5code)
        md5code = m.hexdigest()

        rurl = 'http://wr.800617.com:6001/submit.aspx?CompanyID=%s&InterfacePwd=%s&Mobile=%s&Amount=%d&OrderID=%s&OrderSource=1&key=%s' % \
               ('1051', 'm1n2b3', phone, money, sendOrderId, md5code)

        TyContext.ftlog.info('doChangTianYouChargeConfirm url=', rurl)
        retxml, rurl = TyContext.WebPage.webget(rurl)
        TyContext.ftlog.info('doChangTianYouChargeConfirm url=', rurl, 'return=', retxml)

        xmlroot = ElementTree.fromstring(retxml)
        resultCode = xmlroot.find('result').text
        if resultCode == '0000':
            state = 1
            TyContext.RedisPayData.execute('SADD', 'cty:' + str(gameId) + ':confirm', orderId + '.' + str(chargeUserId))
            TyContext.RedisPayData.execute('SREM', 'cty:' + str(gameId) + ':request', orderId + '.' + str(chargeUserId))
        else:
            state = -1
        datas['ctime'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        datas['state'] = state
        datas['ccode'] = resultCode
        datas = json.dumps(datas)

        TyContext.RedisPayData.execute('HSET', 'cty:' + str(gameId) + ':' + str(chargeUserId), orderId, datas)

        mo.setResult('chargeUserId', chargeUserId)
        mo.setResult('orderId', orderId)
        mo.setResult('chargeAmount', (money / 10))
        mo.setResult('chargeState', state)
        mo.setResult('resultCode', resultCode)
        return mo

    @classmethod
    def doChangTianYouCallback(self, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        orderId = ''
        try:
            CompanyID = TyContext.RunHttp.getRequestParam('CompanyID', '')
            Mobile = TyContext.RunHttp.getRequestParam('Mobile', '')
            Amount = TyContext.RunHttp.getRequestParam('Amount', '')
            OrderID = TyContext.RunHttp.getRequestParam('OrderID', '')
            Result = TyContext.RunHttp.getRequestParam('Result', '')
            Key = TyContext.RunHttp.getRequestParam('Key', '')

            if OrderID.find('momo') > 0:
                mydomain = PayHelper.getSdkDomain()
                if mydomain != 'http://211.152.97.145':
                    TyContext.ftlog.error('not update ?? OrderID=', OrderID)
                    httpurl = 'http://211.152.97.145/v1/pay/changtianyou/callback'
                    datas = {'CompanyID': CompanyID, 'Mobile': Mobile, 'Amount': Amount,
                             'OrderID': OrderID, 'Result': Result, 'Key': Key}
                    response, httpurl = TyContext.WebPage.webget(httpurl, datas)
                    TyContext.ftlog.info('doChangTianYouCallback->redirect to momo->response=', response, 'httpurl=',
                                         httpurl)
                    return response

            if CompanyID == '1051':
                m = md5()
                m.update(CompanyID + Mobile + Amount + OrderID + Result + '756ffh')
                md5code = m.hexdigest()
                if md5code == Key:
                    odatas = OrderID.split('.')
                    orderId = odatas[0]
                    gameId = int(odatas[1])
                    userId = int(odatas[2])

                    TyContext.RunMode.get_server_link(orderId)

                    datas = TyContext.RedisPayData.execute('HGET', 'cty:' + str(gameId) + ':' + str(userId), orderId)
                    if datas != None:
                        datas = json.loads(datas)
                        if datas['state'] == 1:
                            if int(Result) == 0:
                                datas['state'] = 2
                                TyContext.RedisPayData.execute('SADD', 'cty:' + str(gameId) + ':done',
                                                               orderId + '.' + str(userId))
                                TyContext.RedisPayData.execute('SREM', 'cty:' + str(gameId) + ':confirm',
                                                               orderId + '.' + str(userId))
                            else:
                                TyContext.ftlog.error('doChangTianYouCallback->args=', params, ' charge result error!')
                                datas['state'] = -1
                            datas['ftime'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                            datas = json.dumps(datas)
                            TyContext.RedisPayData.execute('HSET', 'cty:' + str(gameId) + ':' + str(userId), orderId,
                                                           datas)
                            TyContext.ftlog.info('doChangTianYouCallback->args=', params, ' ok Done !')
                        else:
                            TyContext.ftlog.error('doChangTianYouCallback->args=', params, 'order state not 1')
                    else:
                        TyContext.ftlog.error('doChangTianYouCallback->args=', params, 'order id not found')
                else:
                    TyContext.ftlog.error('doChangTianYouCallback->args=', params, 'the md5 verify error')
            else:
                TyContext.ftlog.error('doChangTianYouCallback->args=', params, 'the CompanyID is error')

            TyContext.RunMode.del_server_link(orderId)

            return '<?xml version="1.0" encoding="utf-8" ?><ctuport><result>0000</result></ctuport>'''

        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.error('doChangTianYouCallback->args=', params, 'exception error')
            TyContext.RunMode.del_server_link(orderId)
            return '<?xml version="1.0" encoding="utf-8" ?><ctuport><result>1001</result></ctuport>'

    @classmethod
    def doChangTianYouChargeHistory(cls, gameId, userId, mo):
        itdata = TyContext.RedisPayData.execute('HGETALL', 'cty:' + str(gameId) + ':' + str(userId))
        TyContext.ftlog.info('ChargeHistory:', repr(itdata))
        datas = []
        if itdata:
            for ix in xrange(0, len(itdata) / 2):
                itemStr = itdata[ix * 2 + 1]
                item = json.loads(itemStr)
                date = time.strptime(item['rtime'], '%Y%m%d%H%M%S')
                item['rtime'] = time.strftime('%Y-%m-%d %H:%M', date)
                datas.append(item)
        mo.setResult('datas', datas)
        return mo
