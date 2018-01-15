# -*- coding=utf-8 -*-

from xml.etree import ElementTree


class SmsDownBaiFen(object):
    def __call__(self, *argl, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext
        self.smsurl = u'http://cf.lmobile.cn/submitdata/Service.asmx/g_Submit'

    def __init__(self):
        pass

    def sendSms(self, mobile, content, sdk_type='tuyoo', sms_config={}):
        basecontent = content
        if sms_config:
            smsurl = sms_config.get('smsurl')
            content = basecontent + sms_config.get('smssign')
            querys = {
                'sname': sms_config.get('sname'),
                'spwd': sms_config.get('spwd'),
                'scorpid': '',
                'sprdid': sms_config.get('sprdid'),
                'sdst': str(mobile),
                'smsg': content
            }
        elif sdk_type == 'shediao':
            smsurl = u'http://cf.51welink.com/submitdata/Service.asmx/g_Submit'
            content = content + '【射雕科技】'
            querys = {
                'sname': 'dlquzh00',
                'spwd': '0rg8fEus',
                'scorpid': '',
                'sprdid': '1012818',
                'sdst': str(mobile),
                'smsg': content
            }
        elif sdk_type == 'xingyou':
            smsurl = u'http://cf.lmobile.cn/submitdata/Service.asmx/g_Submit'
            content = content + '【星游网络】'
            querys = {
                'sname': 'dlzxty00',
                'spwd': '18lJsdrv',
                'scorpid': '',
                'sprdid': '1012818',
                'sdst': str(mobile),
                'smsg': content
            }
        # tuyoo
        else:
            smsurl = u'http://cf.lmobile.cn/submitdata/Service.asmx/g_Submit'
            content = content + '【途游游戏】'
            querys = {
                'sname': 'dlzxty00',
                'spwd': '18lJsdrv',
                'scorpid': '',
                'sprdid': '1012818',
                'sdst': str(mobile),
                'smsg': content
            }
        # 不用post会500错误
        response, _ = self.__ctx__.WebPage.webget(smsurl, postdata_=querys)
        xmlroot = ElementTree.fromstring(response)
        state = xmlroot.find('{http://tempuri.org/}State').text
        if int(state) != 0:
            return False
        return True


SmsDownBaiFen = SmsDownBaiFen()


class SmsDownKJCX(object):
    '''
    空间畅想
    '''
    smsurl = 'http://210.51.190.19:8080/eums/send_strong.do'

    def sendSms(self, mobile, content, sdk_type='cty', sms_config={}):

        from datetime import datetime
        pwd = 'kl9f90v5'
        seed = datetime.now().strftime('%Y%m%d%H%M%S')
        if sms_config:
            content = content + sms_config.get('smssign')
            pwd = sms_config.get('spwd')
            querys = {
                'name': sms_config.get('sname'),
                'seed': seed,
                'dest': mobile,
                'content': content,
            }
        else:
            content = content + '【途游游戏】'
            querys = {
                'name': 'tuyouhy',
                'seed': seed,
                'dest': mobile,
                'content': content,
            }
        import types
        content = querys['content']
        if type(content) != types.UnicodeType:
            content = unicode(content, "utf8")
        querys['content'] = content.encode("GBK")
        from hashlib import md5
        m = md5(pwd)
        m = md5(m.hexdigest().lower() + querys['seed'])
        querys['key'] = m.hexdigest().lower()
        from tyframework.context import TyContext
        response, _ = TyContext.WebPage.webget(self.smsurl, postdata_=querys)
        if 'succ' in response:
            return True
        return False


class SmsDownCTY(object):
    def __call__(self, *argl, **argd):
        return self

    '''
    畅天游
    '''
    smsurl = 'http://sms.800617.com:4400/sms/SendSMS.aspx'

    def sendSms(self, mobile, content, sdk_type='cty', sms_config={}):
        if sms_config:
            content = content + sms_config.get('smssign')
            querys = {
                'un': sms_config.get('sname'),
                'pwd': sms_config.get('spwd'),
                'mobile': mobile,
                'msg': content
            }
        else:
            content = content + '【途游游戏】'
            querys = {
                'un': 'ctyswse-45',
                'pwd': '7b93bf',
                'mobile': mobile,
                'msg': content
            }
        from tyframework.context import TyContext
        response, _ = TyContext.WebPage.webget(self.smsurl, postdata_=querys)
        dstr = response.decode('gb2312').encode('utf-8')
        dstr = dstr.replace('gb2312', 'utf-8')
        print dstr
        root = ElementTree.fromstring(dstr)
        if root.find('Result').text == '1':
            return True
        print root.find('Result').text
        return False


class SmsDownManDao(object):
    def __call__(self, *argl, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext
        self.sn = 'SDK-BBX-010-19139'
        pwd = '140408'
        pwd = TyContext.strutil.md5digest(self.sn + pwd)
        self.pwd = pwd.upper()
        self.smsurl = u'http://sdk2.entinfo.cn:8061/mdsmssend.ashx?'

    def __init__(self):
        pass

    def sendSms(self, mobile, content, sdk_type='tuyoo', sms_config={}):
        content = content + '【在线途游】'
        content = unicode(content, 'utf8')
        content = content.encode('utf8')

        querys = {
            'sn': self.sn,
            'pwd': self.pwd,
            'mobile': mobile,
            'content': content,
        }

        surl = self.smsurl + self.__ctx__.strutil.urlencode(querys)

        response, _ = self.__ctx__.WebPage.webget(surl, {})
        response = str(response).strip()
        if response[0] == '-':
            return False
        return True


SmsDownManDao = SmsDownManDao()


class SmsDownSelector(object):
    def __call__(self, *argl, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext
        SmsDownBaiFen._init_ctx_()
        SmsDownManDao._init_ctx_()

    channelConfig = {
        'cty': SmsDownCTY(),
        'kjcx': SmsDownKJCX(),
        'baifen': SmsDownBaiFen,
        'mandao': SmsDownManDao,
    }

    def __init__(self):
        pass

    def sendSms(self, mobile, content, sdk_type='tuyoo', sms_config={}):
        channelList = sms_config.get('channelList', [])
        for it in channelList:
            channelName = it.get('name')
            channel = self.channelConfig.get(channelName)
            if channel:
                if channel.sendSms(mobile, content, sdk_type, it):
                    return True
        if sdk_type == 'cty':
            return SmsDownCTY().sendSms(mobile, content, sdk_type, sms_config)
        if sdk_type == 'kjcx':
            return SmsDownKJCX().sendSms(mobile, content, sdk_type, sms_config)
        channel = self.__ctx__.Configure.get_global_item_str('smsdown_selector', 'mandao')
        if channel == 'baifen':
            return SmsDownBaiFen.sendSms(mobile, content, sdk_type, sms_config)
        else:
            return SmsDownManDao.sendSms(mobile, content, sdk_type, sms_config)


SmsDownSelector = SmsDownSelector()
