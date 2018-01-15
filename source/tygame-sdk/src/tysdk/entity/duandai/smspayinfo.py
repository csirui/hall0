# -*- coding=utf-8 -*-

from tyframework.context import TyContext


class SmsPayInfo(object):
    '''
    SmsPayInfo defines the smsPayInfo field in chargeData.

    It is to cover all duandai messages variants.
    The getSmsPayInfo method is depricated. Please use build_sms_payinfo method.
    It is a dict, contains these fields:
        messages: list of tuples. each tuple is (addr, text, wait).  addr is the
            port where to send the text.  text is the short msg text, utf8
            encoded. wait is the seconds to wait before sending next message
            in the list. if there is not next message, its value is ignored.
        blockaddr: optional. a list of blocked port of down-path sms messages.
        blocktext: optional. a list of blocked text of down-path sms messages, utf8 format.
        nohint: optional. whether hint the user or not before sending sms. default to 0.
    '''

    @classmethod
    def fill_in_dialog_text(cls, payinfo, prodname, prodprice):
        dialog_text = TyContext.Configure.get_global_item_json(
            'smspay_dialog_text_template')
        payinfo['text1'] = dialog_text['text1'].format(prodName=prodname,
                                                       prodPrice=prodprice)
        payinfo['text2'] = dialog_text['text2'].format(prodName=prodname,
                                                       prodPrice=prodprice)

    @classmethod
    def build_sms_payinfo(cls, messages, blockaddr=None, blocktext=None, nohint=None):
        sms_payinfo = {}
        if nohint:
            sms_payinfo['nohint'] = nohint
        assert isinstance(messages, list)
        for message in messages:
            assert len(message) == 3
            assert isinstance(message[0], basestring)
            assert isinstance(message[1], basestring)
            assert isinstance(message[2], int)
        sms_payinfo['messages'] = messages
        if blockaddr:
            assert isinstance(blockaddr, list)
            for addr in blockaddr:
                assert isinstance(addr, basestring)
            sms_payinfo['blockaddr'] = blockaddr
        if blocktext:
            assert isinstance(blocktext, list)
            for text in blocktext:
                assert isinstance(text, basestring)
            sms_payinfo['blocktext'] = blocktext
        return sms_payinfo

    @classmethod
    def getSmsPayInfo(cls, smsType, smsMsg, smsPort, smsSecondMsg=None,
                      smsVerifyPort=None):
        '''
        smsType: 1 表示一个短信内容发一个号码发一次
        smsType: 2 表示一个短信内容发一个号码发两次
        smsType: 3 表示一个短信内容发两个号码各发一次
        smsType: 4 表示两个短信内容发同一个号码各发一次
        smsType: 5 表示两个短信内容分别发对应的号码各发一次
        '''
        smsPayinfo = {}
        smsPayinfo['type'] = smsType
        smsPayinfo['smsMsg'] = smsMsg
        smsPayinfo['smsPort'] = smsPort
        if smsSecondMsg:
            smsPayinfo['smsSecondMsg'] = smsSecondMsg
        if smsVerifyPort:
            smsPayinfo['smsVerifyPort'] = smsVerifyPort
        return smsPayinfo
