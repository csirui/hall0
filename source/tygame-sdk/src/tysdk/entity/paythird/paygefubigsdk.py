import collections
import json
import urllib
import urlparse

from Crypto.PublicKey import RSA
from OpenSSL.crypto import load_privatekey, FILETYPE_PEM

from tyframework.context import TyContext
from tysdk.entity.pay import rsacrypto
from tysdk.entity.paythird.helper import PayHelper

AIBEI_PRIVATE_KEY = '''-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDOXVDl97dmAEovx/BXuhz45OPfXTOHry2x7BEFPVh4o0pbaxAo
wxgnmWBpnC/9DdK/D20W0Dqf9JQPOyjS/w7fvz611bXfDPxLTwDAQL4+ZKNBGeKN
L0VpaUqxkcD8CZu5q/h9IKCq1dtJAQvaP5F0+Qy+g+mxSJ92dal32uFpxwIDAQAB
AoGATGGLrOKoNg/LZa4KTl4rlRAbK7Ryezkin6Uxk4/mLBi8T+PrwjqbuSRy5AQU
WwR/yYnrJbOCz2uWVaDe9mHDXfCL0CDFOkmJcfrvoiHyN6PAEdpkF11Xz1ZE2+zN
gquQqIhZ2JEhUiVdlsaCvm7ITDlIkIaP0Ei7xVdjpvFZCdECQQD981QG3ZZaCDFR
+fErSTR4wPl8iAUsn8ev7IQsJZppMchy9avPY1fdSTEmdAH2dFpJR3AK4nl7SXxf
bOL95Q5fAkEA0AesWlQpg/X+51fJUL5xnIYDaX5aXHehuSec5lthBjX/BCeAxah4
8kMr5Otw4snN3vgKO0O+rAnaRBI8ml8NmQJBAPpunH2MxbmRfLm/xuIN9g3jF+WD
6b5g7zaBArLaflSgwHEF7mG9MSfLBwpJuqnFgkfjiA1j27MF+/3KzmrdGPcCQC2t
YaS70hnNi9jUJ7n49w09R8aEHecrxXDYR9U0v0sT1Bjfa6D66wOWyC6Nm83QLcoF
gImeyGESEMDdmDz1HhECQQCvIKn4oW1z3SFH4Rb8+B7BeQDigZ6RO/cyD21anKgn
3bN1o5/+mBAdrGdcIV16VjJxzZWjCgzFsgGuZUkfJVRu
-----END RSA PRIVATE KEY-----'''

_aibei_privkey = load_privatekey(FILETYPE_PEM, AIBEI_PRIVATE_KEY)

AIBEI_PUB_KEY = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCc4qwDo1aPdUvs/veJ/tobXYPU
s1AXnEDmC4lEdKwguyi+LHHLPYYU+bHmPTko9h7di/d+croGDSPgGVIyelyOOQip
6UUSVEAqJwVqqWb7bxXmJchPeGm/MUXwAq09RV620wOkTc9rTuhVU1IJUc+LIRrw
K80IOALwEbhZcEvz8wIDAQAB
-----END PUBLIC KEY-----'''

_aibei_pubkey_py = RSA.importKey(AIBEI_PUB_KEY)


class TuYouPayGeFuBigSdk(object):
    createorder_url = ''

    @classmethod
    def charge_data(cls, chargeinfo):

        TyContext.ftlog.info('TuYouPayGeFuBigSdk charge_data chargeinfo', chargeinfo)

        geFuBigSdkconfig = TyContext.Configure.get_global_item_json('geFuBigSdk_config', {})

        rparam = collections.OrderedDict()

        rparam['appid'] = geFuBigSdkconfig['appId']
        rparam['appuserid'] = str(chargeinfo['uid'])
        rparam['cporderid'] = chargeinfo['platformOrderId']
        # rparam['cpprivateinfo'] = '在线途游'
        rparam['currency'] = 'RMB'
        rparam['price'] = int(chargeinfo['chargeTotal'])
        rparam['waresid'] = int(geFuBigSdkconfig['waresId'])
        rparam['notifyurl'] = PayHelper.getSdkDomain() + '/v1/pay/gefubigsdk/callback'

        msg = json.dumps(rparam, separators=(',', ':'))
        TyContext.ftlog.info('TuYouPayGeFuBigSdk charge_data msg', msg)
        msgsign = ''
        for i in msg:
            if i == '/':
                msgsign += '\/'
            else:
                msgsign += i

        TyContext.ftlog.info('TuYouPayGeFuBigSdk charge_data msgsign', msgsign)
        signMsg = rsacrypto._sign_with_privatekey_openssl_md5(msgsign, _aibei_privkey)

        TyContext.ftlog.info('TuYouPayGeFuBigSdk charge_data signMsg', signMsg)

        cls.createorder_url = geFuBigSdkconfig['createOrderUrl']
        params = {}
        params['transdata'] = msgsign
        params['sign'] = signMsg
        params['signtype'] = 'RSA'
        responsemsg, _ = TyContext.WebPage.webget(cls.createorder_url, params, None, params)

        TyContext.ftlog.info('TuYouPayGeFuBigSdk charge_data responsemsg', responsemsg)

        responsemsg = urllib.unquote(responsemsg)
        responseDict = urlparse.parse_qs(responsemsg)
        TyContext.ftlog.info('TuYouPayGeFuBigSdk charge_data Ditct', responseDict)

        response = str(responseDict['transdata'][0])
        TyContext.ftlog.info('TuYouPayGeFuBigSdk charge_data responseDict[transdata]', responseDict['transdata'],
                             'response', response)

        response = eval(str(response))
        TyContext.ftlog.info('TuYouPayGeFuBigSdk charge_data eval response', response)

        strtransdata = str(responseDict['transdata'][0])
        strsign = responseDict['sign'][0].replace(' ', '+')

        TyContext.ftlog.info('TuYouPayGeFuBigSdk charge_data strtransdata', strtransdata, 'strsign', strsign)

        if rsacrypto._verify_with_publickey_pycrypto_md5(strtransdata, strsign, _aibei_pubkey_py):
            if response['transid']:
                TyContext.ftlog.info('TuYouPayGeFuBigSdk success userId transid', response['transid'])
                chargeinfo['chargeData'] = {'transid': response['transid']}
            else:
                TyContext.ftlog.error('TuYouGeFuDaEAiBeiSdk Failed ', chargeinfo['userId'], 'code',
                                      responseDict['code'], 'errmsg', response['errmsg'])
        else:
            TyContext.ftlog.error('TuYouPayGeFuBigSdk Failed ', '验签失败')

    @classmethod
    def doGeFuBigPaySdkCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()

        TyContext.ftlog.info('TuYouPayGeFuBigSdk Callback ', rparam)

        strtransdata = rparam['transdata']
        sign = rparam['sign'].replace(' ', '+')

        params = eval(str(rparam['transdata']))
        TyContext.ftlog.info('TuYouPayGeFuBigSdk callback transdata ', params)

        orderPlatformId = params['cporderid']
        total_fee = float(params['money'])

        if rsacrypto._verify_with_publickey_pycrypto_md5(strtransdata, sign, _aibei_pubkey_py):
            if 0 == params['result']:
                rparam['third_orderid'] = params['transid']
                rparam['chargeType'] = 'gefubig'
                PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
                return 'SUCCESS'
            else:
                errinfo = '支付失败'
                PayHelper.callback_error(orderPlatformId, errinfo, rparam)
                return 'FAILURE'
        else:
            errinfo = '签名校验失败'
            PayHelper.callback_error(orderPlatformId, errinfo, rparam)
            return 'FAILURE'
