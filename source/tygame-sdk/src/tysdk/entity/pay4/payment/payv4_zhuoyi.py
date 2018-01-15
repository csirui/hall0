#! encoding=utf-8
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment import PayBaseV4
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4
from tysdk.entity.pay4.payment.payv4_helper import PayHelperV4

__author__ = 'yuejianqiang'

from tyframework.context import TyContext
import hashlib


class TuYouPayZhuoyiV4(PayBaseV4):
    @payv4_order("zhuoyi")
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        zhuoyi_keys = TyContext.Configure.get_global_item_json('zhuoyi_keys', {})
        buttonId = chargeinfo['buttonId']
        buttonName = chargeinfo['buttonName']
        packageName = chargeinfo['packageName']
        try:
            payInfo = zhuoyi_keys[packageName]
            codes = payInfo['codes']
            code = codes.get(buttonId, codes.get(buttonName))
        except:
            config = GameItemConfigure(chargeinfo['appId']).get_game_channel_configure_by_package('zhuoyi', packageName,
                                                                                                  chargeinfo[
                                                                                                      'mainChannel'])
            prodConfig = config.get('products', {})
            diamondList = filter(lambda x: buttonId in x.values(), prodConfig)
            diamondConfig = diamondList[0] if diamondList else {}
            if not diamondConfig:
                raise PayErrorV4(1, "找不到商品%s的计费点配置" % buttonId)
            code = diamondConfig.get('code', '')
            payInfo = {
                'appId': config.get('zhuoyi_appId', '')
                , 'appKey': config.get('zhuoyi_appKey', '')}
        chargeinfo['chargeData'] = {
            'platformOrderId': chargeinfo['platformOrderId'],
            'appId': payInfo['appId'],
            'appKey': payInfo['appKey'],
            'code': code
        }
        return cls.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback("/open/ve/zhuoyi/callback")
    def doCallback(cls, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        platformOrderId = rparams['Extra']
        TyContext.ftlog.debug('TuYouPayZhuoyi->doCallback, rparams=', rparams)
        if not cls.check_sign(rparams):
            TyContext.ftlog.error('TuYouPayZhuoyi->ERROR, sign error !! rparam=', rparams)
            return 'failure'
        # do charge
        isOk = PayHelperV4.callback_ok(platformOrderId, -1, rparams)
        if isOk:
            return 'success'
        else:
            return 'failure'

    @classmethod
    def check_sign(cls, rparams):
        # Recharge_Id = rparams['Recharge_Id']
        App_Id = rparams['App_Id']
        platformOrderId = rparams['Extra']
        # Uin=rparams['Uin']
        # Urecharge_Id=rparams['Urecharge_Id']
        # Extra=rparams['Extra']
        # Recharge_Money=rparams['Recharge_Money']
        # Recharge_Gold_Count=rparams['Recharge_Gold_Count']
        # Pay_Status=rparams['Pay_Status']
        # Create_Time=rparams['Create_Time']
        Sign = rparams['Sign']
        # find payKey by appId
        zhuoyi_keys = TyContext.Configure.get_global_item_json('zhuoyi_keys', {})
        payKey = ''
        for appInfo in zhuoyi_keys.values():
            if str(appInfo['appId']) == App_Id:
                payKey = appInfo['paySecret']
                break
        else:
            config = GameItemConfigure.get_game_channel_configure_by_orderId(platformOrderId, 'zhuoyi')
            payKey = config.get('zhuoyi_paySecret', "")
            if not payKey:
                TyContext.ftlog.debug("doZhuoyiCallback,cannot find zhuoyi config for ", App_Id)
                return False
        params = filter(lambda x: x[0] != '' and x[0] != 'Sign', rparams.items())
        params.sort(lambda x, y: cmp(x[0], y[0]))
        params = map(lambda x: '%s=%s' % x, params)
        text = '&'.join(params)
        if Sign != hashlib.md5('%s%s' % (text, payKey)).hexdigest():
            return False
        return True
