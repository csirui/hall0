# -*- coding=utf-8 -*-

# Author:        zipxing@hotmail.com
# Company:       YouXia.Inc
# Created:       2012年04月06日 星期五 16时55分58秒
# FileName:      http91.py
# Class:         Http91Tasklet

# from trunk svn 7501 2014-10-04 10:58

import base64
import json
import re
import urllib
import urlparse
from xml.etree import ElementTree

from tyframework.context import TyContext
from tyframework.orderids import orderid
from tysdk.entity.pay.rsacrypto import rsa_decrypto_with_publickey, iTools_pubkey_str
from tysdk.entity.pay.rsacrypto_yee2 import get_yee_verify
from tysdk.entity.pay.shortidmapping import ShortOrderIdMap
from tysdk.entity.paythird.paymidashi import TuYouPayMiDaShi
from tysdk.utils.pyDes201.pyDes import triple_des, ECB, PAD_NORMAL


class HttpGateWay(object):
    HTMLPATHS = None

    CALLBACKS = {
        # 用户操作相关
        # mandao sms up callback
        '/open/v1/user/smsCallback': {'online': 1, 'type': 100},
        # baifen sms up callback
        '/open/v1/user/smsCallback/baifen': {'online': 1, 'type': 101},
        # 支付操作相关
        '/v1/pay/360/callback': {'online': 1, 'type': 1, 'paramKey': 'mer_trade_code'},
        '/v1/pay/360/msg/callback': {'online': 1, 'type': 1, 'paramKey': 'platformOrderId'},
        '/v1/pay/360pay/callback': {'online': 1, 'type': 1, 'paramKey': 'app_order_id'},
        '/v1/pay/aibei/callback': {'online': 0, 'type': 4, 'paramKey': 'transdata', 'jsonPath': 'exorderno'},
        '/v1/pay/aigame/callback': {'online': 0, 'type': 1, 'paramKey': 'gameUserId'},
        '/v1/pay/aigame/msg/callback': {'online': 0, 'type': 1, 'paramKey': 'cpparam'},
        '/v1/pay/aiyouxi/callback1': {'online': 1, 'type': 1, 'paramKey': ['cpparam', 'cp_order_id']},
        '/v1/pay/aiyouxi/callback2': {'online': 1, 'type': 1, 'paramKey': 'gameUserId'},
        '/v1/pay/aiyouxi/callback/dizhu/cunzhang': {'online': 1, 'type': 1, 'paramKey': ['cpparam', 'cp_order_id']},
        '/v1/pay/aiyouxi/callback/dizhu/kugou': {'online': 1, 'type': 1, 'paramKey': ['cpparam', 'cp_order_id']},
        '/v1/pay/aiyouxi/callback/dizhu/happy': {'online': 1, 'type': 1, 'paramKey': ['cpparam', 'cp_order_id']},
        '/v1/pay/aiyouxi/callback/dizhu/tyhall': {'online': 1, 'type': 1, 'paramKey': ['cpparam', 'cp_order_id']},
        '/v1/pay/aiyouxi/callback/dizhu/huabei': {'online': 1, 'type': 1, 'paramKey': 'cp_order_id'},
        '/v1/pay/aiyouxi/callback/dizhustar/zszh/wf': {'online': 1, 'type': 1, 'paramKey': ['cpparam', 'cp_order_id']},
        '/v1/pay/aiyouxi/callback/dizhustar/zszh/pt': {'online': 1, 'type': 1, 'paramKey': ['cpparam', 'cp_order_id']},
        '/v1/pay/aiyouxi/callback/dizhu/happy/dj': {'online': 1, 'type': 1, 'paramKey': ['cpparam', 'cp_order_id']},
        '/v1/pay/aigame/all/callback': {'online': 1, 'type': 1, 'paramKey': ['cpparam', 'cp_order_id']},
        '/v1/pay/alipay/callback': {'online': 1, 'type': 2, 'paramKey': 'notify_data', 'xmlPath': 'out_trade_no'},
        '/v1/pay/alinewpay/callback': {'online': 1, 'type': 1, 'paramKey': 'out_trade_no'},
        '/v1/pay/wxpay/callback': {'online': 1, 'type': 3, 'paramKey': '', 'xmlPath': 'out_trade_no', },
        '/v1/pay/baidu/callback': {'online': 0, 'type': 4, 'paramKey': 'transdata', 'jsonPath': 'exorderno'},
        '/v1/pay/caifutong/callback': {'online': 0, 'type': 9},
        '/v1/pay/caifutong/notify': {'online': 0, 'type': 1, 'paramKey': 'sp_billno'},
        '/v1/pay/card/callback': {'online': 1, 'type': 1, 'paramKey': 'privateField'},
        '/v1/pay/yipay/callback': {'online': 1, 'type': 1, 'paramKey': 'app_orderid'},
        '/v1/pay/yipaysdk/callback': {'online': 1, 'type': 1, 'paramKey': 'app_orderid'},
        '/v1/pay/muzhiwan/callback': {'online': 1, 'type': 1, 'paramKey': 'app_orderid'},
        '/v1/pay/jinri/callback': {'online': 1, 'type': 1, 'paramKey': 'app_orderid'},
        '/v1/pay/changtianyou/callback': {'online': 1, 'type': 1, 'paramKey': 'OrderID'},
        '/v1/pay/duoku/msg/callback': {'online': 1, 'type': 1, 'paramKey': 'cpdefinepart'},
        '/v1/pay/vivo/callback': {'online': 1, 'type': 1, 'paramKey': 'storeOrder'},
        '/v1/pay/huafubao/callback': {'online': 1, 'type': 1, 'paramKey': 'orderId'},
        '/v1/pay/huafubao/getorder': {'online': 1, 'type': 6, 'paramKey': 'goodsInf', 'splitStr': '#', 'splitKey': 2},
        '/v1/pay/ios/callback': {'online': 1, 'type': 5, 'paramKey': 'iosOrderId'},
        '/v1/pay/jingdong/callback': {'online': 0, 'type': 4, 'paramKey': 'data', 'base64Json': True,
                                      'jsonPath': 'orderId'},
        # '/v1/pay/jingdong/getorder'
        # '/v1/pay/jingdong/getrole'
        '/v1/pay/momo/callback': {'online': 1, 'type': 1, 'paramKey': 'app_trade_no'},
        '/v1/pay/laohu/callback': {'online': 1, 'type': 1, 'paramKey': 'platformOrderId'},
        '/v1/pay/lenovodj/callback': {'online': 1, 'type': 4, 'paramKey': 'transdata', 'jsonPath': 'cpprivate'},
        '/v1/pay/lenovo/callback': {'online': 1, 'type': 4, 'paramKey': 'transdata', 'jsonPath': 'exorderno'},
        '/v1/pay/liantong/callback': {'online': 1, 'type': 3, 'paramKey': '', 'xmlPath': 'orderid'},
        '/v1/pay/linkyun/callback': {'online': 1, 'type': 1, 'paramKey': 'goodsInf', 'substrHead': 2},
        '/v1/pay/linkyun/confirm': {'online': 1, 'type': 1, 'paramKey': 'goodsInf', 'substrHead': 2},
        '/v1/pay/linkyun/union/callback': {'online': 1, 'type': 1, 'paramKey': 'orderid', 'substrHead': 2},
        '/v1/pay/linkyun/union/confirm': {'online': 1, 'type': 1, 'paramKey': 'orderid', 'substrHead': 2},
        '/v1/pay/linkyun/ltsdk/callback': {'online': 1, 'type': 1, 'paramKey': 'outTradeNo'},
        '/v1/pay/linkyun/dx/callback': {'online': 1, 'type': 1, 'paramKey': 'passwd', 'substrHead': -6},
        '/v1/pay/linkyun/api/callback': {'online': 1, 'type': 1, 'paramKey': 'cpparam', 'substrHead': 2},
        '/v1/pay/mh/callback': {'online': 0, 'type': 1, 'paramKey': 'OrderId', 'substrHead': 2},
        '/v1/pay/oppo/callback': {'online': 1, 'type': 1, 'paramKey': 'partnerOrder'},
        '/v1/pay/mo9/callback': {'online': 1, 'type': 1, 'paramKey': 'invoice'},
        '/v1/pay/youku/callback': {'online': 1, 'type': 1, 'paramKey': 'apporderID'},
        '/v1/pay/qtld/callback': {'online': 1, 'type': 1, 'paramKey': 'extra'},
        '/v1/pay/114/callback': {'online': 1, 'type': 1, 'paramKey': 'cpOrderId'},
        '/v1/pay/linkyun/ido/callback': {'online': 1, 'type': 1, 'paramKey': 'order_code'},
        '/v1/pay/doumeng/callback': {'online': 1, 'type': 1, 'paramKey': 'privstr'},
        '/v1/pay/zhangyue/callback': {'online': 1, 'type': 4, 'paramKey': 'transData', 'jsonPath': 'merOrderId'},
        '/v1/pay/shediao/caifutong/callback': {'online': 0, 'type': 9},
        '/v1/pay/shediao/caifutong/notify': {'online': 0, 'type': 1, 'paramKey': 'sp_billno'},
        '/v1/pay/shediao/alipay/callback': {'online': 1, 'type': 1, 'paramKey': 'out_trade_no'},
        '/v1/pay/shediao/card/callback': {'online': 1, 'type': 1, 'paramKey': 'privateField'},
        '/v1/pay/shediaoyee/callback': {'online': 1, 'type': 1, 'paramKey': 'p2_Order'},
        '/v1/pay/tianyi/msg/callback': {'online': 0, 'type': 1, 'paramKey': 'txId'},
        '/v1/pay/wandoujia/callback': {'online': 1, 'type': 4, 'paramKey': 'content', 'jsonPath': 'out_trade_no'},
        '/v1/pay/xiaomi/callback': {'online': 1, 'type': 1, 'paramKey': 'cpOrderId'},
        '/v1/pay/xiaomidanji/callback': {'online': 1, 'type': 1, 'paramKey': 'cpOrderId'},
        '/v1/pay/yd/callback': {'online': 0, 'type': 3, 'paramKey': '', 'xmlPath': 'cpParam'},
        '/v1/pay/ydgs/callback': {'online': 0, 'type': 3, 'paramKey': '', 'xmlPath': 'cpParam'},
        '/v1/pay/ydmm/callback': {'online': 1, 'type': 3, 'paramKey': '',
                                  'xmlPath': '{http://www.monternet.com/dsmp/schemas/}ExData'},
        '/v1/pay/ydjd/callback': {'online': 1, 'type': 3, 'paramKey': '', 'xmlPath': 'cpparam', 'substrHead': 2},
        '/v1/pay/yee/callback': {'online': 1, 'type': 1, 'paramKey': 'p2_Order'},
        '/v1/pay/yidongmm/msg/callback': {'online': 1, 'type': 1, 'paramKey': 'platformOrderId'},
        '/v1/pay/yidongmmtuyou/msg/callback': {'online': 0, 'type': 1, 'paramKey': 'platformOrderId'},
        '/v1/pay/yingyonghui/msg/callback': {'online': 0, 'type': 1, 'paramKey': 'platformOrderId'},
        '/v1/pay/liantongw/callback': {'online': 1, 'type': 3, 'paramKey': '', 'xmlPath': 'orderid', 'substrHead': 10},
        '/v1/pay/yee2/callback10': {'online': 1, 'type': 99},  # 测试
        '/v1/pay/yee2/callback11': {'online': 1, 'type': 99},
        '/v1/pay/yee2/callback20': {'online': 1, 'type': 99},  # 途游
        '/v1/pay/yee2/callback21': {'online': 1, 'type': 99},
        '/v1/pay/yee2/callback30': {'online': 1, 'type': 99},  # 射雕
        '/v1/pay/yee2/callback31': {'online': 1, 'type': 99},
        '/v1/pay/360sns/callback': {'online': 1, 'type': 1, 'paramKey': 'app_order_id'},
        '/v1/pay/360ydmm/callback': {'online': 1, 'type': 3, 'paramKey': '',
                                     'xmlPath': '{http://www.monternet.com/dsmp/schemas/}ExData'},
        '/v1/pay/360liantongwo/callback': {'online': 1, 'type': 3, 'paramKey': '', 'xmlPath': 'orderid',
                                           'substrHead': 10},
        '/v1/pay/xinyinhe/callback': {'online': 1, 'type': 1, 'paramKey': 'orderno'},
        '/v1/pay/zhangqu/callback': {'online': 1, 'type': 1, 'paramKey': 'p', 'substrHead': -6},
        '/v1/pay/uucun/callback': {'online': 1, 'type': 1, 'paramKey': 'platformOrderId'},
        '/v1/pay/huawei/callback': {'online': 1, 'type': 1, 'paramKey': 'requestId'},
        '/v1/pay/tencent/callback': {'online': 1, 'type': 7, 'paramKey': 'appmeta', 'splitStr': '*', 'splitKey': 0},
        '/v1/pay/pps/callback': {'online': 1, 'type': 6, 'paramKey': 'userData', 'splitStr': ',', 'splitKey': 0},
        '/v1/pay/zhuowang/callback': {'online': 1, 'type': 6, 'paramKey': 'cmd', 'splitStr': ',', 'splitKey': -1},
        '/v1/pay/rdo/callback': {'online': 1, 'type': 1, 'paramKey': 'orderNo', 'substrHead': 6},
        '/v1/pay/langtian/callback': {'online': 1, 'type': 6, 'paramKey': 'msg', 'splitStr': '#', 'splitKey': -1},
        '/v1/pay/uc/callback': {'online': 1, 'type': 8, 'paramKey': 'data', 'jsonPath': 'cpOrderId'},
        '/v1/pay/ucdj/callback': {'online': 1, 'type': 8, 'paramKey': 'data', 'jsonPath': 'orderId'},
        '/v1/pay/9xiu/callback': {'online': 1, 'type': 1, 'paramKey': 'orderPlatformId'},
        '/v1/pay/shuzitianyu/callback': {'online': 1, 'type': 1, 'paramKey': 'linkid', 'substrHead': 7},
        '/v1/pay/szty/h5/callback': {'online': 1, 'type': 1, 'paramKey': 'orderid'},
        '/v1/pay/palm/callback': {'online': 1, 'type': 1, 'paramKey': 'merOrderNo'},
        '/v1/pay/palm/closeview/callback': {'online': 1, 'type': 99},
        '/v1/pay/yygame/callback': {'online': 1, 'type': 1, 'paramKey': 'cparam'},
        '/v1/pay/meizu/callback': {'online': 1, 'type': 1, 'paramKey': 'cp_order_id'},
        '/v1/pay/jinritoutiao/callback': {'online': 1, 'type': 1, 'paramKey': 'out_trade_no'},
        '/v1/pay/gefu/callback': {'online': 1, 'type': 1, 'paramKey': 'orderno'},
        '/v1/pay/gefusdk/callback': {'online': 1, 'type': 1, 'paramKey': 'orderno'},
        '/v1/pay/googleiab/callback': {'online': 1, 'type': 1, 'paramKey': 'platformOrderId'},
        '/v1/pay/maopao/callback': {'online': 1, 'type': 1, 'paramKey': 'orderId'},
        '/v1/pay/daodao/callback': {'online': 1, 'type': 1, 'paramKey': 'cpparam'},
        '/v1/pay/aidongman/callback': {'online': 1, 'type': 2, 'paramKey': 'requestData', 'xmlPath': 'Extension',
                                       'substrHead': 23},
        '/v1/pay/gefubigsdk/callback': {'online': 1, 'type': 8, 'paramKey': 'transdata', 'jsonPath': 'cporderid'},
        '/v1/pay/jinli/callback': {'online': 1, 'type': 1, 'paramKey': 'out_order_no'},
        '/v1/pay/xyzs/callback': {'online': 1, 'type': 1, 'paramKey': 'extra'},
        '/v1/pay/xyzsdj/callback': {'online': 1, 'type': 1, 'paramKey': 'extra'},
        '/v1/pay/ppzhushou/callback': {'online': 1, 'type': 8, 'paramKey': 'data', 'jsonPath': 'orderId'},
        '/v1/pay/mingtiandongli/callback': {'online': 1, 'type': 1, 'paramKey': 'cpparams'},
        '/v1/pay/aisi/callback': {'online': 1, 'type': 1, 'paramKey': 'billno'},
        '/v1/pay/haimawan/callback': {'online': 1, 'type': 1, 'paramKey': 'out_trade_no'},
        '/v1/pay/itools/callback': {'online': 1, 'type': 10, 'paramKey': 'order_id_com'},
        '/v1/pay/kuaiyongpingguo/callback': {'online': 1, 'type': 1, 'paramKey': 'dealseq'},
        '/v1/pay/anzhi/callback': {'online': 1, 'type': 11, 'paramKey': 'cpInfo'},
        '/v1/pay/tongbutui/callback': {'online': 1, 'type': 1, 'paramKey': 'trade_no'},
        '/v1/pay/vipchinamobile/callback': {'online': 1, 'type': 12, 'paramKey': ['usernumber', 'msg'],
                                            'kind': 'chinaMobile'},
        '/v1/pay/vipchinaunion/callback': {'online': 1, 'type': 12, 'paramKey': ['mobile', 'smscontext']},
        '/v1/pay/viptelecom/callback1': {'online': 1, 'type': 12, 'paramKey': ['mobile', 'mo']},
        '/v1/pay/viptelecom/callback2': {'online': 1, 'type': 12, 'paramKey': ['mobile', 'reason'],
                                         'kind': 'chinaTelecom'},
        '/v1/pay/vipmobiletoorder/callback': {'online': 1, 'type': 12, 'paramKey': ['mobile', 'mo']},
        '/v1/pay/midashi/callback': {'online': 1, 'type': 13, 'paramKey': 'payitem'},
        '/v1/pay/iappay/callback': {'online': 1, 'type': 4, 'paramKey': 'transdata', 'jsonPath': 'cporderid'},
        '/v1/pay/iiapple/callback': {'online': 1, 'type': 1, 'paramKey': 'gameExtend'},
        '/v1/pay/now/callback': {'online': 1, 'type': 14, 'paramKey': 'mhtOrderNo'},
        '/v1/pay/unionpay/callback': {'online': 1, 'type': 1, 'paramKey': 'orderId'},
        '/v1/pay/mumayi/callback': {'online': 1, 'type': 8, 'paramKey': 'orderID'},
        '/v1/pay/pengyouwan/callback': {'online': 1, 'type': 8, 'paramKey': 'cp_orderid'},
        '/v1/pay/4399/callback': {'online': 1, 'type': 1, 'paramKey': 'mark'},
        '/v1/pay/zhuoyi/callback': {'online': 1, 'type': 1, 'paramKey': 'Extra'},
        '/v1/pay/sougou/callback': {'online': 1, 'type': 14, 'paramKey': 'appdata'},
        '/v1/pay/coolpad/callback': {'online': 1, 'type': 4, 'paramKey': 'transdata', 'jsonPath': 'cporderid'},
        '/v1/pay/jolo/callback': {'online': 1, 'type': 9, 'paramKey': 'game_order_id'},
        '/v1/pay/papa/callback': {'online': 1, 'type': 1, 'paramKey': 'app_order_id'},
        '/v1/pay/kuaiwan/callback': {'online': 1, 'type': 8, 'paramKey': 'orderId'},
        '/v1/pay/changba/callback': {'online': 1, 'type': 4, 'paramKey': 'transdata', 'jsonPath': 'cporderid'},
        '/v1/pay/lizi/callback': {'online': 1, 'type': 1, 'paramKey': 'extend'},
        '/v1/pay/nubia/callback': {'online': 1, 'type': 1, 'paramKey': 'order_no'},
        '/v1/pay/letv/callback': {'online': 1, 'type': 1, 'paramKey': 'cooperator_order_no'},
        '/v1/pay/yiwan/callback': {'online': 1, 'type': 1, 'paramKey': 'custominfo'},
        '/v1/pay/ysdk/callback': {'online': 1, 'type': 1, 'paramKey': 'orderId'},
        '/v1/pay/jusdk/callback': {'online': 1, 'type': 1, 'paramKey': 'dealseq'},
        '/v1/pay/bdgame/callback': {'online': 1, 'type': 1, 'paramKey': 'CooperatorOrderSerial'},
        '/v1/pay/wandoujiadanji/callback': {'online': 1, 'type': 4, 'paramKey': 'content', 'jsonPath': 'out_trade_no'},
        '/v1/pay/vivounion/callback': {'online': 1, 'type': 1, 'paramKey': 'cpOrderNumber'},
        '/v1/pay/wyxt/callback': {'online': 1, 'type': 1, 'paramKey': 'orderid'},
        '/v1/pay/more/callback': {'online': 1, 'type': 8, 'paramKey': 'orderinfo', 'jsonPath': 'cporderid'},
        '/v1/pay/168x/callback': {'online': 1, 'type': 1, 'paramKey': 'game_orderno'},
        '/v1/pay/16game/callback': {'online': 1, 'type': 1, 'paramKey': 'orderId'},
        '/v1/pay/alinewpay/app/callback': {'online': 1, 'type': 1, 'paramKey': 'out_trade_no'},
        '/v1/pay/liebao/callback': {'online': 1, 'type': 1, 'paramKey': 'cp_order_id'},
    }

    @classmethod
    def getHtmlPaths(cls):
        if not cls.HTMLPATHS:
            cls.HTMLPATHS = {}
            for rpath in cls.CALLBACKS:
                TyContext.ftlog.info('gate path ->', rpath)
                cls.HTMLPATHS[rpath] = cls._do_gateway
            cls.HTMLPATHS['/v1/pay/jingdong/getorder'] = cls._jingdong_getorder
            cls.HTMLPATHS['/v1/pay/jingdong/getrole'] = cls._jingdong_getrole
        return cls.HTMLPATHS

    @classmethod
    def _jingdong_getorder(cls, path):
        # base64.b64encode('{"orderStatus": "0"}') == eyJvcmRlclN0YXR1cyI6ICIwIn0=
        return '{"retCode": "100","retMessage": "success","data": "eyJvcmRlclN0YXR1cyI6ICIwIn0="}'

    @classmethod
    def _jingdong_getrole(cls, path):
        try:
            jsondata = TyContext.RunHttp.getRequestParam('data', '')
            jsondata = base64.decodestring(jsondata)
            jsondata = json.loads(jsondata)
            userId = int(jsondata['userId'])
            data_base64 = base64.b64encode('{"roleInfos": [{"roleId": "' + str(userId) + '","roleName": ""}]}')
            return '{"retCode": "100","retMessage": "success","data": "' + data_base64 + '"}'
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doJingDongGetRole->ERROR, param error !! jsondata=', jsondata)
            return '{"retCode": "103","retMessage": "param error","data": ""}'

    @classmethod
    def _do_gateway(cls, rpath):
        config = cls.CALLBACKS[rpath]
        calltypes = config['type']
        postData = ''
        queryDatas = None
        TyContext.ftlog.debug("_do_gateway", "rpath=%s" % rpath)
        TyContext.ftlog.debug("_do_gateway", "param=%s" % TyContext.RunHttp.convertArgsToDict())
        TyContext.ftlog.debug("_do_gateway", "post=%s" % TyContext.RunHttp.get_body_content())
        if calltypes == 1:
            '''
            在tasklet.args当中直接可以取得orderPlatformOrderId
            '''
            if isinstance(config['paramKey'], list):
                for paramKeys in config['paramKey']:
                    orderPlatformId = TyContext.RunHttp.getRequestParam(paramKeys, '')
                    if orderPlatformId != '':
                        break
            else:
                orderPlatformId = TyContext.RunHttp.getRequestParam(config['paramKey'], '')

            if 'post_body' in config:
                postData = TyContext.RunHttp.get_body_content()
                queryDatas = TyContext.RunHttp.convertArgsToDict()

        elif calltypes == 2:
            '''
            取得tasklet.args当中的某个参数里面的值后进行XML解析后，可以取得orderPlatformOrderId
            '''
            xmldata = TyContext.RunHttp.getRequestParam(config['paramKey'], '')
            xmlroot = ElementTree.fromstring(xmldata)
            orderPlatformId = xmlroot.find(config['xmlPath']).text

        elif calltypes == 3:
            '''
            信息在POST的BODY当中，其格式为XML，解析后可以取得orderPlatformOrderId
            '''
            postData = TyContext.RunHttp.get_body_content()
            TyContext.ftlog.debug('postdata=[', postData, ']')
            xmlroot = ElementTree.fromstring(postData)
            orderPlatformId = xmlroot.find(config['xmlPath']).text
            queryDatas = TyContext.RunHttp.convertArgsToDict()

        elif calltypes == 4:
            '''
            取得tasklet.args当中的某个参数里面的值后进行JSON解析后，可以取得orderPlatformOrderId
            '''
            jsondata = TyContext.RunHttp.getRequestParam(config['paramKey'], '')
            if 'base64Json' in config and config['base64Json'] == True:
                jsondata = base64.decodestring(jsondata)
            jsondata = json.loads(jsondata)
            orderPlatformId = jsondata[config['jsonPath']]

        elif calltypes == 5:
            '''
            IOS特殊的回调
            此处取得的是游戏内的“购买道具”的ID,即游戏的orderId
            '''
            orderPlatformId = TyContext.RunHttp.getRequestParam(config['paramKey'], '')

        elif calltypes == 6:
            '''
            取得tasklet.args当中的某个参数里面的值后进行split分隔后，可以取得orderPlatformOrderId
            '''
            dataStr = TyContext.RunHttp.getRequestParam(config['paramKey'], '')
            orderPlatformId = dataStr.split(config['splitStr'])[config['splitKey']]

        elif calltypes == 7:
            '''
            信息在POST的BODY当中，其格式为XML，解析后可以取得orderPlatformOrderId
            '''
            try:
                dataStr = ''
                postData = TyContext.RunHttp.get_body_content()
                # TyContext.ftlog.info('zhuowangMdo postData=', postData)
                postData = postData.replace('encoding="gbk"', 'encoding="utf-8"')
                postData = unicode(postData, encoding='gbk').encode('utf-8')
                # TyContext.ftlog.info('zhuowangMdo encode->postData=', postData)
                xmlroot = ElementTree.fromstring(postData)
                # TyContext.ftlog.info('zhuowangMdo xmlroot=', xmlroot)
                parmMap = xmlroot.getiterator("paramMap")[0]
                for x in parmMap:
                    k, v = x.getchildren()
                    if k.text == 'command':
                        dataStr = v.text
                        # TyContext.ftlog.info('zhuowangMdo dataStr=', dataStr)
                if dataStr != '':
                    orderPlatformId = dataStr.split(config['splitStr'])[config['splitKey']]
                    # TyContext.ftlog.info('zhuowangMdo orderPlatformId=', orderPlatformId)
            except:
                TyContext.ftlog.exception()
        elif calltypes == 8:
            '''
            信息在POST的BODY当中，其格式为JSON，解析后拿到里面的一个JSON数据可以取得orderPlatformOrderId
            '''
            try:
                postData = TyContext.RunHttp.get_body_content()
                if rpath.find('gefubigsdk') != -1:
                    postData = urllib.unquote(postData)
                    TyContext.ftlog.info("postData", postData)
                    response = urlparse.parse_qs(postData)
                    rparams = eval(response[config['paramKey']][0])
                    orderPlatformId = rparams[config['jsonPath']]
                    TyContext.ftlog.info("response", response, 'rparams', rparams, 'paramKey', config['paramKey'],
                                         'jsonPath', config['jsonPath'], 'orderPlatformId', orderPlatformId)

                else:
                    jsondata = json.loads(postData)
                    paramKey = config['paramKey']
                    jsonPath = config.get('jsonPath', '')
                    jsondata = jsondata[paramKey]
                    if jsonPath:
                        orderPlatformId = jsondata[jsonPath]
                    else:
                        orderPlatformId = jsondata
            except:
                TyContext.ftlog.exception()
        elif calltypes == 9:
            '''
            信息在POST的BODY当中，其格式为order="%7B%22result_code%22%3A1%2C%22gmt_create%22%3A%222014-04-15+11%3A07%3A42%22%2C%22real_amount%22%3A100%2C%22result_msg%22%3A%22%E6%94%AF%E4%BB%98%E6%88%90%E5%8A%9F%22%2C%22game_code%22%3A%222792557105408%22%2C%22game_order_id%22%3A%22201404155250421048987403109%22%2C%22jolo_order_id%22%3A%22ZF-277fa462fe674a398790d267c2e367c2%22%2C%22gmt_payment%22%3A%222014-04-15+11%3A08%3A05%22%7D"&sign="VmjAUCko66btW15Sq15B2r1oF9NGwE9If%2F07vu8QaWRI7wZcKI%2FY3ifYeziJGr%2F69xXV0eIeHH3QOvH26A6zayaSB1cj0lb2sZ6xDWvVn0Kz26rscnA7Z3NGMoEQgheYaKiNxI%2BI9q7lwodvaPG0on%2BFWXZ2N8CzAxjSGtP3VdA%3D"&sign_type="RSA"
            '''
            try:
                postData = TyContext.RunHttp.get_body_content()
                TyContext.ftlog.info("postData", postData)
                response = urlparse.parse_qs(postData)
                order = response['order'][0].strip('"')
                jsonData = json.loads(order)
                paramKey = config['paramKey']
                orderPlatformId = jsonData[paramKey]
            except:
                TyContext.ftlog.exception()
        elif calltypes == 10:
            '''
            iTools回掉的特殊处理，信息在POST的BODY中，其格式为notiry_data=xxx&sign=xxx的形式，但xxx是经过rsa密钥加密并进行base64编码过的数据，
            需要先进行base64解码并用rsa公钥解密方能获取其中的数据
            '''
            postData = TyContext.RunHttp.get_body_content()
            TyContext.ftlog.debug('postData: ', postData)
            paramslist = postData.split('&')
            params = {}
            for k in paramslist:
                paramdata = k.split('=')
                params[paramdata[0]] = paramdata[1]
            TyContext.ftlog.debug('postParams: ', params)

            for k in params.keys():
                params[k] = urllib.unquote(params[k])
            TyContext.ftlog.debug('postParams_urldecode: ', params)

            pristr = params['notify_data']
            sign = params['sign']
            data = rsa_decrypto_with_publickey(pristr, iTools_pubkey_str, 1)
            TyContext.ftlog.debug('iTools callback data: ', data)
            jsondata = json.loads(data)
            orderPlatformId = jsondata[config['paramKey']]
            TyContext.ftlog.debug('relocation callback data: ', postData)
        elif calltypes == 11:
            '''
            安智回掉的特殊处理，信息在POST的BODY中，其格式为body=XXXXXX的形式，其中XXXXXX为经过3des加密并进行base64编码过的内容，其中IV和padding均为空值,
            需要先进行base64解码并用3des解密方能获取其中的数据，数据的格式为json，cpInfo字段为所要的内容，内容为途游订单号。
            '''
            postData = TyContext.RunHttp.get_body_content()
            TyContext.ftlog.debug('Original postData is:', postData)

            urlParam = TyContext.RunHttp.convertArgsToDict()
            TyContext.ftlog.debug('Url params is:', urlParam)

            if 'appId' in urlParam:
                appId = urlParam['appId']
            else:
                TyContext.ftlog.error('ERROR There doesn\'t has appId in request url.')
                return 'success'

            paramdata = postData.split('=')
            rparam = {paramdata[0]: paramdata[1]}
            TyContext.ftlog.debug('Parame list(Before urldecode) is: ', rparam)

            for k in rparam.keys():
                rparam[k] = urllib.unquote(rparam[k])
            TyContext.ftlog.debug('Parame list(After urldecode) is: ', rparam)

            if 'data' in rparam:
                data = rparam['data']
            else:
                TyContext.ftlog.error('ERROR There doesn\'t has data in post data.')
                return 'failed'

            anzhiconfig = TyContext.Configure.get_global_item_json('anzhi_config', {})
            if anzhiconfig:
                for item in anzhiconfig:
                    if 0 == cmp(item['appId'], appId):
                        encryptKey = item['appsecret']
                        break
                else:
                    TyContext.ftlog.error('ERROR Cann\'t find appsecert, appId is: ', appId)
                    return 'success'
            else:
                TyContext.ftlog.error('ERROR cann\'t find anzhi_config.')
                return 'success'

            try:
                # 先用base64解码，再采用3des解密
                tripelDes = triple_des(encryptKey.encode('ascii'), mode=ECB, padmode=PAD_NORMAL)
                data = tripelDes.decrypt(base64.b64decode(data))
                data = "".join([data.rsplit("}", 1)[0], "}"])
                TyContext.ftlog.debug('Data is: ', data)
                params = json.loads(data)
                orderPlatformId = params[config['paramKey']]  # 途游订单号
            except Exception as e:
                TyContext.ftlog.error('ERROR: ', e)
                return 'success'
            postData = postData + '&appId=' + appId
        elif calltypes == 12:
            '''
            会员包月回掉，订单号在字符串中ty后面，以ty分割字符串，然后去后面的那个字符串即可
            '''
            urlParam = TyContext.RunHttp.convertArgsToDict()
            TyContext.ftlog.debug('Url params is:', urlParam)
            command = urlParam.get('command', '')
            if 0 == cmp(command, 'report'):
                return 'ok'
            paramList = config['paramKey']
            mobile = urlParam[paramList[0]]
            smsContent = urlParam[paramList[1]]
            orderPlatformId = cls.getplatformOrderId(smsContent, mobile)
            if not orderPlatformId:
                if 'kind' in config:
                    phoneType = config['kind']
                    TyContext.ftlog.error(
                        'Httpgateway ERROR: There\'s a none recode monthly callback, mobile:[%s], phoneType:[%s].' % (
                        mobile, phoneType))
                else:
                    TyContext.ftlog.error(
                        'Httpgateway ERROR: There should have a short orderId in smsContent, mobile:[%s].' % mobile)
                return 'fail'
        elif calltypes == 13:
            '''
            米大师回掉，订单号是参数中某字段的一部分
            '''
            try:
                urlParam = TyContext.RunHttp.convertArgsToDict()
                TyContext.ftlog.debug('Url params is:', urlParam)
                payitem = urlParam[config['paramKey']]
                appmeta = payitem.split('*')[0]
                orderPlatformId = appmeta
            except Exception, e:
                TyContext.ftlog.error('Httpgateway ERROR:', e)
                return TuYouPayMiDaShi.getReturnContent(4, config['paramKey'])

            if not TuYouPayMiDaShi.verifySign(urlParam):
                return TuYouPayMiDaShi.getReturnContent(4, 'sign error.')
        elif calltypes == 14:
            """
            参数在POST的BODY中，格式key=value&key=value
            """
            postData = TyContext.RunHttp.get_body_content()
            TyContext.ftlog.debug('postData: ', postData)
            paramslist = postData.split('&')
            params = {}
            for k in paramslist:
                paramdata = k.split('=')
                params[paramdata[0]] = paramdata[1]
            TyContext.ftlog.debug('postParams: ', params)
            for k in params.keys():
                params[k] = urllib.unquote(params[k])
            TyContext.ftlog.debug('postParams_urldecode: ', params)
            orderPlatformId = params[config['paramKey']]
            TyContext.ftlog.debug('relocation callback data: ', postData)
        elif calltypes == 99:
            '''
            易宝银行卡回调特殊处理
            '''
            orderPlatformId = TyContext.RunHttp.getRequestParam('orderid', '')
            if not orderPlatformId:
                orderPlatformId, postData = cls._get_yee2_orderid(rpath, config)
            if orderPlatformId == None:
                return '{"errorcode ":200024}'
        elif calltypes == 100:
            # mandao短信回调特殊处理
            orderPlatformId = cls._get_mandao_sms_orderid(rpath)
            if len(orderPlatformId) == 0:  # TODO 如果单号取得失败，直接返回数据，0 OK ？
                return '0'
        elif calltypes == 101:
            # baifen短信回调特殊处理
            orderPlatformId = cls._get_baifen_sms_orderid(rpath)
            if len(orderPlatformId) == 0:  # TODO 如果单号取得失败，直接返回数据，0 OK ？
                return '0'
        else:
            '''
            财付通：返回一个充值结果的网页
            '''
            raise Exception('not implement !!')

        if 'substrHead' in config:
            substrHead = int(config['substrHead'])
            if '/v1/pay/liantongw/callback' == rpath and orderPlatformId.startswith('0000000FC'):
                orderPlatformId = orderPlatformId[len('0000000FC') - 2:]
            elif '/v1/pay/ydjd/callback' == rpath and orderPlatformId.startswith('FC'):
                pass
            else:
                orderPlatformId = orderPlatformId[substrHead:]
        # 移动基地,移动妹妹,联通沃商店,电信爱游戏,以FC开头的订单,全部透传至优易付服务器.
        TyContext.ftlog.debug('TyContext.RunHttp->rpath ', rpath, 'orderPlatformId', orderPlatformId)
        yipay_passthrough_config = TyContext.Configure.get_global_item_json('yipay_passthrough_address', {})
        if orderPlatformId.startswith('FC') and rpath in yipay_passthrough_config:
            # YDMM 检查订单号是否全为0, 直接返回失败
            if rpath == '/v1/pay/ydmm/callback' and postData and postData.find(
                    '<OrderID>00000000000000000000</OrderID>') >= 0:
                return '''<?xml version="1.0" encoding="UTF-8"?><SyncAppOrderResp><MsgType>SyncAppOrderResp</MsgType><Version>1.0.0</Version><hRet>0</hRet></SyncAppOrderResp>'''
            redirectUrl = yipay_passthrough_config[rpath]
            TyContext.ftlog.debug('TyContext.RunHttp->redirectUrl', redirectUrl)
            if len(postData) == 0:
                datas = TyContext.RunHttp.convertArgsToDict()
            else:
                datas = postData
            headers = {'Content-type': 'text/xml'}
            response, fullUrl = TyContext.WebPage.webget(redirectUrl, datas, None, postdata_=postData, headers_=headers)
            TyContext.ftlog.info('__do_gateway__->passthrough->orderPlatformId', orderPlatformId, 'response=[',
                                 response, '] fullUrl=[', fullUrl, ']')
            return response
        if len(orderPlatformId) == 6:
            # 这是一个短ID，需要换为长ID
            longid = ShortOrderIdMap.get_long_order_id(orderPlatformId)
            TyContext.ftlog.info('_do_gateway->replace short order id with long id. sort=[', orderPlatformId,
                                 '] long=[', longid, ']')
            if longid == None:
                orderPlatformId = ''
            else:
                orderPlatformId = str(longid)

        # 临时处理单机商城bug，把订单号替换成正式订单号
        if orderPlatformId[0:1] == 'f' and orderPlatformId[4:5] == 'R':
            orderPlatformId = orderPlatformId[0:4] + '0' + orderPlatformId[5:]

        #         apiVer = orderPlatformId[0:1]
        apiVer, _ = orderid.get_order_id_info(orderPlatformId)
        if not TyContext.ServerControl.is_valid_orderid_str(orderPlatformId) \
                or orderPlatformId.find('GO') == 0:
            TyContext.ftlog.error('ERROR !! _do_gateway rpath', rpath,
                                  'orderPlatformId', orderPlatformId, 'is not a valid platform orderid !')
            #             appId = 0
            #             srvTag = ''
            if 'ios/callback' in rpath:
                apiVer = 'c'
            else:
                apiVer = -1
                return 'invalid orderid'

                # apiVer = orderPlatformId[0:1]
            #         appId = TyContext.strutil.toint10(orderPlatformId[1:4])
            #         srvTag = TyContext.strutil.toint10(orderPlatformId[4:5])
        TyContext.ftlog.info('_do_gateway->orderPlatformId=', orderPlatformId,
                             'apiVer=', apiVer)

        temp_apiVer = apiVer.lower()
        if temp_apiVer == 'a' or temp_apiVer == 'b':
            # a V1版本充值的事务
            # b V1版本消费的事务
            replacepath = rpath.replace('/v1/', '/open/va/', 1)
        elif temp_apiVer == 'c' or temp_apiVer == 'd':
            # c V3版本充值的事务
            # d V3版本消费的事务
            replacepath = rpath.replace('/v1/', '/open/vc/', 1)
        elif temp_apiVer == 'e':
            replacepath = rpath.replace('/v1/', '/open/ve/', 1)
        elif temp_apiVer == '0':
            # 0 V1版本短信上行调用
            replacepath = rpath.replace('/v1/', '/va/', 1)
        elif temp_apiVer == 's':
            # s V3版本短信上行调用
            replacepath = rpath.replace('/v1/', '/vc/', 1)
        elif temp_apiVer == 'y':
            # y 畅天游回调
            replacepath = rpath.replace('/v1/', '/open/va/', 1)
        else:
            # 其他
            replacepath = rpath.replace('/v1/', '/open/va/', 1)
            TyContext.ftlog.error('_do_gateway->can not be here, version error !')
        #         control = None
        #         if appId > 0 :
        #             TyContext.RunMode.get_server_link(orderPlatformId)
        #             control = TyContext.ServerControl.findServerControlByTag(appId, srvTag)
        #         if control :
        #             if 'http.sdk' in control :
        #                 redirectUrl = control['http.sdk']
        #             else:
        #                 redirectUrl = control['http']
        #         else:
        #             redirectUrl = TyContext.TYGlobal.http_game()
        #             TyContext.ftlog.error('_do_gateway->can not find server define for appid', appId, 'use localhost!')
        redirectUrl = orderid.getOrderIdHttpCallBack(orderPlatformId)
        redirectUrl = redirectUrl + replacepath
        TyContext.ftlog.info('_do_gateway->orderPlatformId=', orderPlatformId, 'redirectUrl=[', redirectUrl, ']')
        if len(postData) == 0:
            datas = TyContext.RunHttp.convertArgsToDict()
        else:
            if queryDatas:
                datas = queryDatas
            else:
                datas = {}
        if 'authInfo' in datas:
            datas['authInfo'] = datas['authInfo'].replace(' ', '')
        if 'maopao' in rpath:
            datas['orig_uri'] = TyContext.RunHttp.get_request().uri
        # ios的receipt通过postdata进行请求
        if 'receipt' in datas and datas['receipt'] != '':
            if postData:
                postData += '&' + urllib.urlencode({'receipt': datas['receipt']})
            else:
                postData = urllib.urlencode({'receipt': datas['receipt']})

            del datas['receipt']
        response, fullUrl = TyContext.WebPage.webget(redirectUrl, datas, None, postdata_=postData)
        TyContext.ftlog.info('_do_gateway->orderPlatformId=', orderPlatformId, 'response=[', response, '] fullUrl=[',
                             fullUrl, ']')
        return response

    @classmethod
    def _get_mandao_sms_orderid(cls, rpath):
        args = TyContext.RunHttp.getRequestParam('args', None)
        try:
            datas = args.split(',')
            content = urllib.unquote(datas[3])
            content = content.decode('gbk').encode('utf8')
            return cls._get_sms_orderid(content)
        except Exception, e:
            TyContext.ftlog.error('_get_mandao_sms_orderid->ERROR, get bindOrderId error!!'
                                  ' exception', e, 'args=', args)
            return ''

    @classmethod
    def _get_baifen_sms_orderid(cls, rpath):
        content = TyContext.RunHttp.getRequestParam('Up_UserMsg', None)
        return cls._get_sms_orderid(content)

    @classmethod
    def _get_sms_orderid(cls, smscontent):
        ''' caller should make sure smscontent is utf8 encoding '''

        TyContext.ftlog.info('_get_sms_orderid smscontent', smscontent)
        try:
            template = TyContext.Configure.get_global_item_json(
                'smsup_content', decodeutf8=True)
            smsre = template['bindcode_re']
            bindOrderId = re.match(smsre, smscontent).group(1)
            if bindOrderId:
                TyContext.ftlog.info('_get_sms_orderid new format bindOrderId',
                                     bindOrderId)
                return bindOrderId

        except Exception as e:
            pass
            # TyContext.ftlog.error(
            #    '_get_sms_orderid error parsing new format bindOrderId: smscontent',
            #    smscontent, 'exception', e, )

        try:
            # contentData = base64.decodestring(smscontent.replace('%3d', '='))
            contentData = base64.decodestring(smscontent)
            params = contentData.split('|')
            if len(params) > 2:
                bindOrderId = params[0]
            else:
                # bindOrderId = '000600smsv1dummy'
                bindOrderId = ''
            return bindOrderId
        except Exception, e:
            TyContext.ftlog.error('_get_sms_orderid->ERROR, get bindOrderId error!!'
                                  ' exception', e, 'smscontent=', smscontent)
            return ''

    @classmethod
    def _get_yee2_orderid(cls, rpath, config):
        orderid = None
        postData = None
        account = None
        key = rpath.split('/')[-1][:-1]
        account = TyContext.Configure.get_global_item_json('yee2_rpath2account')[key]
        TyContext.ftlog.debug('_get_yee2_orderidaccount=', account, 'data=[', postData, ']')
        encryptkey = TyContext.RunHttp.getRequestParam('encryptkey')
        data = TyContext.RunHttp.getRequestParam('data')
        if not encryptkey or not data:
            TyContext.ftlog.error('_get_yee2_orderid->ERROR, encryptkey(%s) '
                                  'or data(%s) missing!! ' % (encryptkey, data))
            return None, None
        postData = {'encryptkey': encryptkey, 'data': data}

        try:
            yee = get_yee_verify(account)
            rdata = yee.result_decrypt(postData)
        except Exception as e:
            TyContext.ftlog.error('_get_yee2_orderid->ERROR Exception', e,
                                  'account', account, 'postData', postData)
            return None, None

        if rdata and 'orderid' in rdata:
            orderid = rdata['orderid'].split('-')[0]
        return orderid, ''

    # modified as calltypes == 12
    @classmethod
    def getplatformOrderId(cls, smsContent, mobile):
        if '_' in smsContent or 'ty' in smsContent:
            # 联通和电信用户订阅时，由客户端发送的短信息，含有_订单号；移动用户订阅时，由客户端发短信，第三方回掉，含有ty订单号
            if '_' in smsContent:
                shortOrderId = smsContent.split('_')[1]
            else:
                shortOrderId = smsContent.split('ty')[1]
            if cls.isShortOrderIdSame(mobile, shortOrderId):
                params = cls.getUserInfoParam(mobile)
                platformOrderId = params['platformOrderId']
                TyContext.ftlog.info('Old ShortOrderId! ShortOrderId : [%s], platformOrderId :[%s], mobile :[%s]' % (
                shortOrderId, platformOrderId, mobile))
            else:
                platformOrderId = ShortOrderIdMap.get_long_order_id(shortOrderId)
            TyContext.ftlog.debug('ShortOrderId : [%s], platformOrderId :[%s]' % (shortOrderId, platformOrderId))
        else:
            # 用户退订时，由用户自己发送的短信息，不含uid
            params = cls.getUserInfoParam(mobile)
            if not params:
                return None
            platformOrderId = params['platformOrderId']
            TyContext.ftlog.debug('platformOrderId :', platformOrderId)
            if not platformOrderId:
                return None
        return platformOrderId

    @classmethod
    def getUserInfoParam(cls, mobile):
        redisKey = 'vipuser:' + mobile
        paramsStr = TyContext.RedisPayData.execute('GET', redisKey)
        if not paramsStr:
            return None
        try:
            params = json.loads(paramsStr)
        except Exception, e:
            TyContext.ftlog.error('TuYouPayHuiYuanBaoYue->getUserInfo ERROR: ', e)
            return None
        return params

    @classmethod
    def isShortOrderIdSame(cls, mobile, shortOrderId):
        params = cls.getUserInfoParam(mobile)
        if not params:
            return False
        oldShortOrderId = params['shortOrderId']
        if 0 == cmp(shortOrderId, oldShortOrderId):
            return True
        else:
            return False
