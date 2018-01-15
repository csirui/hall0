# -*- coding=utf-8 -*-

import base64
from hashlib import md5

from tyframework.context import TyContext


class AccountVerify():
    APPKEY = 'tytyj83jfellmgl123uyrei98d6dn'

    @classmethod
    def encode64(cls, mstr):
        return base64.b64encode(mstr)

    @classmethod
    def decode64(cls, mstr):
        mstr = mstr.replace('%3d', '=')
        return base64.b64decode(mstr)

    @classmethod
    def md5(cls, mstr):
        if len(mstr) > 0:
            m = md5()
            m.update(mstr)
            md5str = m.hexdigest()
            return md5str
        return ''

    @classmethod
    def md5hexdigest(cls, *args):
        mstr = []
        for argv in args:
            mstr.append(str(argv))
        mstr = ''.join(mstr)
        return cls.md5(mstr)

    @classmethod
    def sing_verify(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        # # 客户端BUG补丁，imei为null时，客户端校验失败
        # imei = rparam.get('imei', '')
        # if imei == 'null' :
        #     return True

        sk = rparam.keys()
        sk.sort()
        ret = ''
        code = ''
        for k in sk:
            if k == 'code':
                code = rparam[k]
            else:
                ret = ret + str(k) + '=' + str(rparam[k]) + '&'

        md5str = ret[:-1] + '&' + cls.APPKEY
        TyContext.ftlog.debug('sing_verify 1->', md5str)
        # md5str = TyContext.strutil.tydes_encode(md5str)
        # TyContext.ftlog.debug('sing_verify 2->', md5str)

        m = md5()
        m.update(md5str)
        md5str = m.hexdigest().lower()
        TyContext.ftlog.debug('sing_verify 3->', md5str, code.lower())
        if md5str == code.lower():
            return True
        return False

    @classmethod
    def decode_item(self, dvalue):
        try:
            #             TyContext.ftlog.debug('decode_item', dvalue)
            value = dvalue.strip()
            #             TyContext.ftlog.debug('decode_item', value)
            return value
        #             if len(value) > 0 :
        #                 value = TyContext.strutil.tydes_decode(value)
        #                 if value == None :
        #                     value = ''
        #                 return value
        except:
            TyContext.ftlog.exception('decode_item error', dvalue)
        #         TyContext.ftlog.info('decode_item return empty')
        return ''
