# -*- coding=utf-8 -*-

import base64
import json

from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5, AES
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as pk
from OpenSSL.crypto import sign as crypto_sign

from tyframework.context import TyContext

__yee_instances__ = {}


def get_yee_verify(account):
    yeekey_config = TyContext.Configure.get_global_item_json('yee2_paykeys', {})
    YEE_PUB_KEY = yeekey_config[str(account)][0]
    TY_PRIV_KEY = yeekey_config[str(account)][1]

    if account in __yee_instances__:
        return __yee_instances__[account]
    yee = Yee2Verify(account, TY_PRIV_KEY, YEE_PUB_KEY)
    __yee_instances__[account] = yee
    return yee


class Yee2Verify():
    def __init__(self, account, tyPrivateKey, yeePublicKey):
        self.account = account
        self.private_key = RSA.importKey(tyPrivateKey)
        self.public_key = RSA.importKey(yeePublicKey)

    #         print 'self.account=', self.account
    #         print 'self.private_key=', self.private_key, tyPrivateKey
    #         print 'self.public_key=', self.public_key, yeePublicKey

    def _pkcs7padding(self, data):
        """
        对齐块
        size 16
        999999999=>9999999997777777
        """
        size = AES.block_size
        count = size - len(data) % size
        if count:
            data += (chr(count) * count)
        return data

    def _depkcs7padding(self, data):
        """
        反对齐
        """
        newdata = ''
        for c in data:
            if ord(c) > AES.block_size:
                newdata += c
        return newdata

    '''
    aes加密base64编码
    '''

    def aes_base64_encrypt(self, data, key):

        """
        @summary:
            1. pkcs7padding
            2. aes encrypt
            3. base64 encrypt
        @return:
            string
        """
        cipher = AES.new(key)
        return base64.b64encode(cipher.encrypt(self._pkcs7padding(data)))

    def base64_aes_decrypt(self, data, key):
        """
        1. base64 decode
        2. aes decode
        3. dpkcs7padding
        """
        cipher = AES.new(key)
        return self._depkcs7padding(cipher.decrypt(base64.b64decode(data)))

    '''
    rsa加密
    '''

    def rsa_base64_encrypt(self, data, key):
        '''
        1. rsa encrypt
        2. base64 encrypt
        '''
        cipher = PKCS1_v1_5.new(key)
        return base64.b64encode(cipher.encrypt(data))

    def rsa_base64_decrypt(self, data, key):
        '''
        1. base64 decrypt
        2. rsa decrypt
        示例代码

       key = RSA.importKey(open('privkey.der').read())
        >>>
        >>> dsize = SHA.digest_size
        >>> sentinel = Random.new().read(15+dsize)      # Let's assume that average data length is 15
        >>>
        >>> cipher = PKCS1_v1_5.new(key)
        >>> message = cipher.decrypt(ciphertext, sentinel)
        >>>
        >>> digest = SHA.new(message[:-dsize]).digest()
        >>> if digest==message[-dsize:]:                # Note how we DO NOT look for the sentinel
        >>>     print "Encryption was correct."
        >>> else:
        >>>     print "Encryption was not correct."
        '''
        cipher = PKCS1_v1_5.new(key)
        return cipher.decrypt(base64.b64decode(data), Random.new().read(15 + SHA.digest_size))

    '''
    RSA签名
    '''

    def sign(self, signdata):
        '''
        @param signdata: 需要签名的字符串
        '''
        #         print 'self.account=', self.account
        #         print 'self.private_key=', self.private_key
        #         print 'self.public_key=', self.public_key
        try:
            h = SHA.new(signdata)
            signer = pk.new(self.private_key)
            signn = signer.sign(h)
            signn = base64.b64encode(signn)
        except:
            TyContext.ftlog.exception()
            d = crypto_sign(self.private_key, signdata, 'sha1')
            b = base64.b64encode(d)
            return b
        return signn

    '''
    RSA验签
    结果:如果验签通过，则返回The signature is authentic
         如果验签不通过，则返回"The signature is not authentic."
    '''

    def checksign(self, rdata):

        signn = base64.b64decode(rdata.pop('sign'))
        signdata = self.sort(rdata)
        #        print "signdata="+signdata
        verifier = pk.new(self.public_key)
        if verifier.verify(SHA.new(signdata), signn):
            #             print "The signature is authentic."
            return True
        else:
            #             print "The signature is not authentic."
            pass
        return False

    def sort(self, mes):
        '''
        作用类似与java的treemap,
        取出key值,按照字母排序后将value拼接起来
        返回字符串
        '''
        _par = []

        keys = mes.keys()
        keys.sort()
        for v in keys:
            d = mes[v]
            if isinstance(d, unicode):
                d = d.encode('utf-8')
            _par.append(str(d))
        sep = ''
        message = sep.join(_par)
        return message

    '''
    请求接口前的加密过程
    '''

    def requestprocess(self, mesdata):
        '''
        加密过程:
        1、将需要的参数mes取出key排序后取出value拼成字符串signdata
        2、用signdata对商户私钥进行rsa签名，生成签名signn，并转base64格式
        3、将签名signn插入到mesdata的最后生成新的data
        4、用encryptkey16位常量对data进行AES加密后转BASE64,生成机密后的data
        5、用易宝公钥publickey对encryptkey16位常量进行RSA加密BASE64编码，生成加密后的encryptkey
        '''
        signdata = self.sort(mesdata)
        #         print '需要签名的排序后的字符串为:' + signdata
        signn = self.sign(signdata)

        mesdata['sign'] = signn
        #         print mesdata
        encryptkey = '1234567890123456'
        data = self.aes_base64_encrypt(json.dumps(mesdata), encryptkey)

        #         print '加密后的data=' + data
        values = {}
        values['merchantaccount'] = self.account
        values['data'] = data
        values['encryptkey'] = self.rsa_base64_encrypt(encryptkey, self.public_key)
        return values

    '''
    对返回结果进行解密后输出
    '''

    def result_decrypt(self, result):
        '''
        1、返回的结果json传给data和encryptkey两部分，都为加密后的
        2、用商户私钥对encryptkey进行RSA解密，生成解密后的encryptkey。参考方法:rsa_base64_decrypt
        3、用解密后的encryptkey对data进行AES解密。参考方法:base64_aes_decrypt
        '''
        if isinstance(result, (str, unicode)):
            result = json.loads(result)
        kdata = result['data']
        kencryptkey = result['encryptkey']
        #         print '返回的加密后的data=' + kdata
        #         print '返回的加密后的encryptkey=' + kencryptkey
        cryptkey = self.rsa_base64_decrypt(kencryptkey, self.private_key)
        #         print '解密后的encryptkey=' + cryptkey
        rdata = self.base64_aes_decrypt(kdata, cryptkey)
        #         print '解密后的data=' + rdata
        rdata = json.loads(rdata)
        return rdata
