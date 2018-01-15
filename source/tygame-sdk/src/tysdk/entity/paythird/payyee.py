# -*- coding=utf-8 -*-

import hmac
import types
from urllib import quote

from tyframework.context import TyContext
from tysdk.entity.pay3.constants import PayConst
from tysdk.entity.paythird.helper import PayHelper

'''
pd_FrpId支付通道编码列表

参数值    对应支付通道名称
SZX    神州行
UNICOM    联通卡
TELECOM    电信卡
JUNNET    骏网一卡通
ZHENGTU    征途卡
QQCARD    Q币卡
JIUYOU    久游卡
NETEASE    网易卡
WANMEI    完美卡
SOHU    搜狐卡
ZONGYOU    纵游一卡通
TIANXIA    天下一卡通
TIANHONG    天宏一卡通
SNDACARD    盛大卡
'''


# 易宝非银联卡支付
class TuYouPayYee():
    # 商户编号p1_MerId,以及密钥merchantKey 需要从易宝支付平台获得
    p1_MerId = "10012097952"  # 在线途游
    merchantKey = "S31ka5Lw8aA256Gum8FA31F5x9F610f5rv529e8p2W0g3kYUMcg587125m1u"
    # 非银行卡支付专业版请求地址,无需更改.
    reqURL_SNDApro = "https://www.yeepay.com/app-merchant-proxy/command.action?"
    # 易宝回调的地址
    callback_url = "/v1/pay/yee/callback"

    code_map = {
        0: u'销卡成功，订单成功',
        1: u'销卡成功，订单失败',
        2: u'撤销订单',
        7: u'卡号卡密或卡面额不符合规则',
        1002: u'本张卡密您提交过于频繁，请您稍后再试',
        1003: u'不支持的卡类型（比如电信地方卡）',
        1004: u'密码错误或充值卡无效',
        1006: u'充值卡无效',
        1007: u'卡内余额不足',
        1008: u'余额卡过期（有效期1个月）',
        1010: u'此卡正在处理中',
        10000: u'未知错误',
        2005: u'此卡已使用',
        2006: u'卡密在系统处理中',
        2007: u'该卡为假卡',
        2008: u'该卡种正在维护中，请稍后再试',
        2009: u'浙江省移动维护中，请稍后再试',
        2010: u'江苏省移动维护中，请稍后再试',
        2011: u'福建省移动维护中，请稍后再试',
        2012: u'辽宁省移动维护中，请稍后再试',
        3001: u'卡不存在',
        3002: u'卡已使用过',
        3003: u'卡已作废',
        3004: u'卡已冻结',
        3005: u'卡未激活',
        3006: u'密码不正确',
        3007: u'卡正在处理中',
        3101: u'系统错误',
        3102: u'卡已过期'}

    @classmethod
    def createQueryString(self, rparam):
        sk = rparam.keys()
        ret = ""
        for k in sk:
            ret = ret + str(k) + '=' + quote(str(rparam[k]), '') + '&'
        return ret[:-1]

    @classmethod
    def getHmacString(cls, hstr):
        # 易宝仅支持GBK编码
        TyContext.ftlog.debug('getHmacString==', repr(hstr))
        if type(hstr) != types.UnicodeType:
            hstr = unicode(hstr, "utf8")
        sbOld = hstr.encode("GBK")
        mac = hmac.new(TuYouPayYee.merchantKey)
        mac.update(sbOld)
        hmacStr = mac.hexdigest()
        TyContext.ftlog.debug('getHmacString==', repr(hmacStr))
        return hmacStr

    @classmethod
    def getReqHmacString(self, rparam, p0_Cmd, pr_NeedResponse):

        # 进行加密串处理，一定按照下列顺序进行
        sbOld = ""
        # 加入业务类型
        sbOld += p0_Cmd
        # 加入商户代码
        sbOld += TuYouPayYee.p1_MerId
        # 加入商户订单号
        sbOld += rparam['p2_Order']
        # 加入支付卡面额
        sbOld += rparam['p3_Amt']
        # 是否较验订单金额
        sbOld += rparam['p4_verifyAmt']
        # 产品名称
        sbOld += rparam['p5_Pid']
        # 产品类型
        sbOld += rparam['p6_Pcat']
        # 产品描述
        sbOld += rparam['p7_Pdesc']
        # 加入商户接收交易结果通知的地址
        httpdomain = PayHelper.getSdkDomain()
        sbOld += httpdomain + TuYouPayYee.callback_url
        # 加入临时信息
        sbOld += rparam['pa_MP']
        # 加入卡面额组
        sbOld += rparam['pa7_cardAmt']
        # 加入卡号组
        sbOld += rparam['pa8_cardNo']
        # 加入卡密组
        sbOld += rparam['pa9_cardPwd']
        # 加入支付通道编码
        sbOld += rparam['pd_FrpId']
        # 加入应答机制
        sbOld += pr_NeedResponse
        # 加入用户ID
        sbOld += str(rparam['pz_userId'])
        # 加入用户注册时间
        sbOld += rparam['pz1_userRegTime']

        return self.getHmacString(sbOld)

    @classmethod
    def annulCard(self, chargeInfo, mi, mo, rparam):
        TyContext.ftlog.info('TuYouPayYee->annulCard->rparam=', rparam, 'chargeInfo=', chargeInfo)
        # 非银行卡支付专业版支付请求，固定值 "ChargeCardDirect".
        p0_Cmd = "ChargeCardDirect"
        # 应答机制.为"1": 需要应答机制;为"0": 不需要应答机制.
        pr_NeedResponse = "1"

        # 调用签名函数生成签名串
        hmacstr = self.getReqHmacString(rparam, p0_Cmd, pr_NeedResponse)
        TyContext.ftlog.debug('TuYouPayYee->annulCard->hmacstr=', hmacstr)
        # 进行加密串处理，一定按照下列顺序进行
        httpdomain = PayHelper.getSdkDomain()
        params = {
            'p0_Cmd': p0_Cmd,  # 加入业务类型
            'p1_MerId': TuYouPayYee.p1_MerId,  # 加入商家ID
            'p2_Order': rparam['p2_Order'],  # 加入商户订单号
            'p3_Amt': rparam['p3_Amt'],  # 加入支付卡面额
            'p4_verifyAmt': rparam['p4_verifyAmt'],  # 加入是否较验订单金额
            'p5_Pid': rparam['p5_Pid'],  # 加入产品名称
            'p6_Pcat': rparam['p6_Pcat'],  # 加入产品类型
            'p7_Pdesc': rparam['p7_Pdesc'],  # 加入产品描述
            'p8_Url': httpdomain + TuYouPayYee.callback_url,  # 加入商户接收交易结果通知的地址
            'pa_MP': rparam['pa_MP'],  # 加入临时信息
            'pa7_cardAmt': rparam['pa7_cardAmt'],  # 加入卡面额组
            'pa8_cardNo': rparam['pa8_cardNo'],  # 加入卡号组
            'pa9_cardPwd': rparam['pa9_cardPwd'],  # 加入卡密组
            'pd_FrpId': rparam['pd_FrpId'],  # 加入支付通道编码
            'pr_NeedResponse': pr_NeedResponse,  # 加入应答机制
            'hmac': hmacstr,  # 加入校验码
            'pz_userId': rparam['pz_userId'],  # 用户唯一标识
            'pz1_userRegTime': rparam['pz1_userRegTime']  # 用户的注册时间
        }
        payUrl = TuYouPayYee.reqURL_SNDApro + TuYouPayYee.createQueryString(params)
        TyContext.ftlog.info('TuYouPayYee->annulCard->payUrl=', payUrl)
        response, payUrl = TyContext.WebPage.webget(payUrl)
        TyContext.ftlog.info('TuYouPayYee->annulCard->payUrl=', payUrl, 'response=', response)
        return TuYouPayYee.getPayResult(response, chargeInfo, mo)

    @classmethod
    def getPayResult(self, ret, datas, mo):

        r0_Cmd = ""  # 业务类型
        r1_Code = ""  # 支付结果
        r2_TrxId = ""  # 易宝支付交易流水号
        r6_Order = ""  # 商户订单号
        rq_ReturnMsg = ""  # 返回信息
        rethmac = ""  # 签名数据
        unkonw = ""  # 未知错误
        result = ret.split("\n")
        for data in result:
            dsp = data.split('=')
            if len(dsp) != 2:
                continue
            sKey, Svalue = dsp
            if sKey == 'r0_Cmd':
                r0_Cmd = Svalue
            elif sKey == 'r1_Code':
                r1_Code = Svalue
            elif sKey == 'r2_TrxId':
                r2_TrxId = Svalue
            elif sKey == 'r6_Order':
                r6_Order = Svalue
            elif sKey == 'rq_ReturnMsg':
                rq_ReturnMsg = Svalue
            elif sKey == 'hmac':
                rethmac = Svalue
            else:
                unkonw = Svalue

        sbOld = str(r0_Cmd) + str(r1_Code) + str(r6_Order) + str(rq_ReturnMsg)
        hmacStr = self.getHmacString(sbOld)

        status = PayConst.CHARGE_STATE_REQUEST
        if (rethmac == hmacStr):
            if r1_Code == '1':
                info = '提交成功！'
                status = PayConst.CHARGE_STATE_REQUEST
            elif r1_Code == '2':
                info = '充值交易失败,卡密成功处理过或者提交卡号过于频繁'
                status = PayConst.CHARGE_STATE_REQUEST_IGNORE
            elif r1_Code == '11':
                info = '充值交易失败,订单号重复'
                status = PayConst.CHARGE_STATE_REQUEST_IGNORE
            elif r1_Code == '66':
                info = '充值交易失败,支付金额有误'
                status = PayConst.CHARGE_STATE_REQUEST_IGNORE
            else:
                info = '充值交易失败,请检查后重新测试支付'
                status = PayConst.CHARGE_STATE_REQUEST_IGNORE
        else:
            info = '充值交易失败,' + rq_ReturnMsg
            status = PayConst.CHARGE_STATE_REQUEST_IGNORE

        if status != PayConst.CHARGE_STATE_REQUEST:
            errinfo = info.decode('utf-8')
            mo.setError(1, errinfo)

        return status

    @classmethod
    def doPayRequestCard(cls, chargeInfo, mi, mo):
        userId = chargeInfo['uid']
        uct = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'createTime')

        card_amount = mi.getParamStr('card_amount', '')
        card_number = mi.getParamStr('card_number', '')
        card_pwd = mi.getParamStr('card_pwd', '')
        card_code = mi.getParamStr('card_code', 'SZX')
        params = {
            'p2_Order': chargeInfo['platformOrderId'],
            'p3_Amt': card_amount,
            'p4_verifyAmt': 'true',
            'p5_Pid': '',
            'p6_Pcat': '',
            'p7_Pdesc': '',
            'pa_MP': '',
            'pa7_cardAmt': card_amount,  # 多卡号以逗号隔开
            'pa8_cardNo': card_number,  # 多卡号以逗号隔开
            'pa9_cardPwd': card_pwd,  # 多卡号以逗号隔开
            'pd_FrpId': card_code,  # 支付卡的通道编码
            'pz_userId': str(userId),
            'pz1_userRegTime': str(uct)
        }
        status = cls.annulCard(chargeInfo, mi, mo, params)
        return status

    @classmethod
    def getCallBackHmacString(self):
        # 进行加密串处理，一定按照下列顺序进行
        sbOld = ""
        sbOld += TyContext.RunHttp.getRequestParam('r0_Cmd', '')
        sbOld += TyContext.RunHttp.getRequestParam('r1_Code', '')
        sbOld += TyContext.RunHttp.getRequestParam('p1_MerId', '')
        sbOld += TyContext.RunHttp.getRequestParam('p2_Order', '')
        sbOld += TyContext.RunHttp.getRequestParam('p3_Amt', '')
        sbOld += TyContext.RunHttp.getRequestParam('p4_FrpId', '')
        sbOld += TyContext.RunHttp.getRequestParam('p5_CardNo', '')
        sbOld += TyContext.RunHttp.getRequestParam('p6_confirmAmount', '')
        sbOld += TyContext.RunHttp.getRequestParam('p7_realAmount', '')
        sbOld += TyContext.RunHttp.getRequestParam('p8_cardStatus', '')
        sbOld += TyContext.RunHttp.getRequestParam('p9_MP', '')
        sbOld += TyContext.RunHttp.getRequestParam('pb_BalanceAmt', '')
        sbOld += TyContext.RunHttp.getRequestParam('pc_BalanceAct', '')
        return self.getHmacString(sbOld)

    @classmethod
    def doCardCallback(cls, rpath):
        iHmacStr = TyContext.RunHttp.getRequestParam('hmac', '')
        cHmacStr = cls.getCallBackHmacString()
        if iHmacStr != cHmacStr:
            TyContext.ftlog.error('TuYouPayYee.doCardCallback, hmac verification error')
            return 'error'
        rparam = TyContext.RunHttp.convertArgsToDict()

        mer_code = TyContext.RunHttp.getRequestParam('p1_MerId')
        if mer_code != TuYouPayYee.p1_MerId:
            TyContext.ftlog.error('TuYouPayYee.doCardCallback error, mer_code is not me !!!')
            return 'error'

        platformOrderId = TyContext.RunHttp.getRequestParam('p2_Order')
        chargeKey = 'sdk.charge:' + platformOrderId
        chargeInfo = TyContext.RedisPayData.execute('HGET', chargeKey, 'charge')
        try:
            import json
            chargeInfo = json.loads(chargeInfo)
            rparam['chargeType'] = chargeInfo['chargeType']
        except:
            TyContext.ftlog.exception()

        rparam['chargeType'] = 'yee.card'
        rparam['sub_paytype'] = TyContext.RunHttp.getRequestParam('p4_FrpId', 'na')
        r1_Code = TyContext.RunHttp.getRequestParam('r1_Code')
        if r1_Code != '1':
            # 长连接通知，客户端支付失败
            status = TyContext.RunHttp.getRequestParamInt('p8_cardStatus', 10000)
            TyContext.ftlog.error('TuYouPayYee.doCardCallback error, charge return error !!! status=', status)
            errorInfo = u'支付失败，' + TuYouPayYee.code_map.get(status, 'status' + str(status))
            PayHelper.callback_error(platformOrderId, errorInfo, rparam)
            return 'success'

        total_fee = float(rparam['p3_Amt'])
        isOK = PayHelper.callback_ok(platformOrderId, total_fee, rparam)
        if isOK:
            return 'success'
        else:
            return 'error'
