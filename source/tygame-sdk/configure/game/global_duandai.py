# -*- coding=utf-8 -*-

from pyscript._helper_config_ import *

# 全国的city zipcode定义
# [1, u"全国",
# [230000,u"安徽",
# [100000,u"北京"
# [350000,u"福建"
# [730000,u"甘肃"
# [510000,u"广东"
# [530000,u"广西"
# [550000,u"贵州"
# [570000,u"海南"
# [50000,u"河北"
# [450000,u"河南"
# [150000,u"黑龙江"
# [430000,u"湖北"
# [410000,u"湖南"
# [130000,u"吉林"
# [210000,u"江苏"
# [330000,u"江西"
# [110000,u"辽宁"
# [10000,u"内蒙"
# [750000,u"宁夏"
# [810000,u"青海"
# [250000,u"山东"
# [30000,u"山西"
# [710000,u"陕西"
# [200000,u"上海"
# [610000,u"四川"
# [300000,u"天津"
# [850000,u"西藏"
# [830000,u"新疆"
# [650000,u"云南"
# [310000,u"浙江"
# [400000,u"重庆"

# 此列表中的支付类型需要进行短信支付限额控制
# add_global_item('paytype.msg.limited.list', ['linkyun', 'linkyununion', 'ydmm',
#                                              'huafubao', 'liantong.wo', 'newYinHe',
#                                              '360.ydmm', '360.liantong.wo'])
add_global_item('paytype.msg.limited.list', ['newYinHe', 'ydmm', 'ydjd'])
# 每设备每月的短信支付限额
add_global_item('paytype.msg.limited.month', 500)
# 每设备每天的短信支付限额
add_global_item('paytype.msg.limited.day', 100)
# 同一IP每天的短信支付次数
add_global_item('single_ip_day_count_limit', {
    #paytype -> count
    'ydmm': 5,
    'ydjd': 5,
    'liantong.wo':5,
})

add_global_item('paytype.msg.speed.limited.list', ['ydmm','ydjd'])
add_global_item('paytype.msg.speed.min.interval', 120)
add_global_item('paytype.msg.speed.limited.waived.clientid.list', [
    'Android_3.71_tyOneKey,tyAccount,tyGuest.weakChinaMobile.0-hall17.ydmm.tu',
    'Android_3.71_tyOneKey,tyAccount,tyGuest.weakChinaMobile.0-hall7.ydmm.happy',
    'Android_3.71_tyOneKey,tyAccount,tyGuest.duoku,yisdkpay4.0-hall3.baidunew.tu',
    'Android_3.71_tyOneKey,tyAccount,tyGuest.duoku,yisdkpay4.0-hall3.bdtiebanew.tu',
    'Android_3.71_tyOneKey,tyAccount,tyGuest.duoku,yisdkpay4.0-hall3.duokunew.tu',
    'Android_3.71_tyOneKey,tyAccount,tyGuest.duoku,yisdkpay4.0-hall3.91new.tu',
    'Android_3.71_tyOneKey,tyAccount,tyGuest.weakChinaMobile.0-hall7.ydmm.sc',
    'Android_3.71_tyOneKey,tyAccount,tyGuest.weakChinaMobile.0-hall7.ydmm.dj',
    'Android_3.71_tyOneKey,tyAccount,tyGuest.weakChinaMobile.0-hall7.ydmm.happy',
    'Android_3.71_tyOneKey,tyAccount,tyGuest.weakChinaMobile.0-hall7.ydmm.tu',
    'Android_3.71_YDJDMain.YDJDMain.0-hall7.ydjd.tu',
    'Android_3.713_tyOneKey,tyAccount,tyGuest.weakChinaMobile.0-hall6.tuyoo.laizi',
    'Android_3.373_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall20.kuyu.tu',
    'Android_3.73_360,tyGuest.360,yisdkpay4.0-hall6.360danji.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.duoku,yisdkpay4.0-hall6.91new.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.duoku,yisdkpay4.0-hall6.baidunew.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.duoku,yisdkpay4.0-hall6.bdtiebanew.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.duoku,yisdkpay4.0-hall6.duokunew.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.jinli,yisdkpay4.0-hall6.jinligame.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.Midas,yisdkpay4.0-hall6.qq.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.Midas,yisdkpay4.0-hall6.qqas.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.Midas,yisdkpay4.0-hall6.qqcustomizedas.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.Midas,yisdkpay4.0-hall6.qqcustomizedgc.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.Midas,yisdkpay4.0-hall6.qqexplorer.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.Midas,yisdkpay4.0-hall6.qqgc.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.Midas,yisdkpay4.0-hall6.qqic02.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.Midas,yisdkpay4.0-hall6.qqtmsas.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.Midas,yisdkpay4.0-hall6.qqtmsgc.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.Midas,yisdkpay4.0-hall6.qqvideo.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall6.ali.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall6.coolpad.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall6.haihai.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall6.htc.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall6.jiangyou.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall6.jinli.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall6.kubi.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall6.kunda.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall6.leshiphone.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall6.litianbaoli.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall6.qingmeng.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall6.sougou.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall6.tcl.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall6.wandou.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall6.wifikey.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall6.yiguo.dj',
    'Android_3.73_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall6.vivo.dj',
    'Android_3.712_360.360,yisdkpay4.0-hall7.360.happy',
    'Android_3.712_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall7.qq.happy',
    'Android_3.712_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall7.qqgc.happy',
    'Android_3.712_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall7.qqas.happy',
    'Android_3.712_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall7.qqcustomizedgc.happy',
    'Android_3.712_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall7.qqtmsgc.happy',
    'Android_3.712_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall7.qqtmsas.happy',
    'Android_3.712_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall7.qqexplorer.happy',
    'Android_3.712_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall7.qqic02.happy',
    'Android_3.712_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall7.qqvideo.happy',
    'Android_3.712_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall7.qqcustomizedas.happy',
    'Android_3.762_tyOneKey,tyAccount,tyGuest.yisdkpay4.0-hall6.zhangzhong.dj',
    #象棋
    #'Android_3.731_tyAccount,tyGuest.weakChinaMobile.0-hall25.ydmm.tu',
    #地主
    #'Android_3.762_tyOneKey,tyAccount,tyGuest.weakChinaMobile.0-hall6.ydmm.happy',
    #'Android_3.761_tyOneKey,tyAccount,tyGuest.weakChinaMobile.0-hall6.ydmm.tu',
    #'Android_3.762_tyOneKey,tyAccount,tyGuest.weakChinaMobile.0-hall6.ydmm.laizi',
    #麻将

])


add_global_item('smspay_dialog_text_template', {
    'text1': '立得{prodName}\n点击确定将自动扣除{prodPrice}元话费',
    'text2': '仅需{prodPrice}元即可获得更多体验，让游戏任性起来。\n如有疑问，请致电客服:4008-098-000',
})


#2014/12/29 ydmm单机关停：吉林，河北，湖北，福建，甘肃，新疆，天津，上海
#linkyun可用：吉林，河北，湖北
add_global_item('ydmm_stopped_list', {
        '300007728518' : { # 单机斗地主
            'stopped_provs' : {
                '130000': { #吉林
                    'fallback': 'linkyun',
                    'prices': [1, 2, 5, 8, 10] },
                '50000': { #河北
                    'fallback': 'linkyun',
                    'prices': [1, 2, 3, 5],
                           },
                '430000': { #湖北
                    'fallback': 'linkyun',
                    'prices': [1, 2, 5, 8, 10] },
            },
            'resortto' : {
                "Android_2.88_360": "360",
                "Android_2.89_360": "360",
                "Android_2.9_360": "360",
                "Android_2.91_360": "360",
                "Android_2.92_360": "360",
                "Android_2.88_91": "tuyoo",
                "Android_2.88_baidu": "tuyoo",
                "Android_2.88_duoku": "tuyoo",
                "Android_2.88_jinshan": "tuyoo",
                "Android_2.89_91": "tuyoo",
                "Android_2.89_aidian": "tuyoo",
                "Android_2.89_apphui": "tuyoo",
                "Android_2.89_baidu": "tuyoo",
                "Android_2.89_coolpad": "tuyoo",
                "Android_2.89_duoku": "tuyoo",
                "Android_2.89_wpsj": "tuyoo",
                "Android_2.92_91": "tuyoo",
                "Android_2.92_baidu": "tuyoo",
                "Android_2.92_coolpad": "tuyoo",
                "Android_2.92_duoku": "tuyoo",
                "Android_2.92_meizu": "tuyoo",
                "Android_2.92_qq": "tuyoo",
                "Android_2.92_wandou": "tuyoo",
                "Android_2.9_91": "tuyoo",
                "Android_2.9_baidu": "tuyoo",
            },
                          }
})

add_global_item('linkyun_stopped_provs', {
    '430000' : { 'stopped_port': '1065800810025938', 'new_port': '1065800810026880', },
})

#5938(1/2/3/5):北京，海南，河北，黑龙江，吉林，辽宁，山西，四川
#5938(8/10):北京，河北，黑龙江，吉林，辽宁，山西，四川
#6880(1/2/3/5/8/10):河北，黑龙江，湖北，吉林，山西，四川
#5775(2/4/8):河北，北京，福建，甘肃，海南，河北，黑龙江，湖北，吉林，江苏，山西，上海，四川
add_global_item('linkyun_supported_provs', {
    10 :   '北京',
    03 :   '山西',
    #11 :   '辽宁',
    #05 :   '河北',
    13 :   '吉林',
    15 : '黑龙江',
    #43 :   '湖北',
    #61 :   '四川',
    #57 :   '海南',
    #73 :   '甘肃',
    20 :   '上海',
    35 :   '福建',
    #21 :   '江苏',
    #45 :   '河南',
    #51 :   '广东',
    #53 :   '广西',
})

#北京,福建,江苏,山西,河北,河南,吉林,黑龙江,湖北,广东,江西(只开了10)
add_global_item('huafubao_supported_provs', {
    10 :   '北京',
    35 :   '福建',
    21 :   '江苏',
    03 :   '山西',
    #33 :   '江西',
    05 :   '河北',
    45 :   '河南',
    13 :   '吉林',
    15 : '黑龙江',
    43 :   '湖北',
    51 :   '广东',
})

# temp solution: ydjd is added here for ydmm/ydjd switch.
add_global_item('nonconfigured_duandai_paytypes', [
    'yipay',
    'ydjd',
    #'EFT.api',
    'yisdkpay',
    'linkyun.api',
    'gefu',
])
#add_global_item('nonconfigured_duandai_paytypes', ['yipay', 'EFT.api', 'yisdkpay', 'linkyun.api'])

add_global_item('all_duandai_paytypes', [
    'ydmm',
    'ydjd',
    'liantong.wo',
    'aigame',
    'linkyun',
    'linkyun.api',
    #'EFTChinaUnion.msg',
    #'EFTChinaTelecom.msg',
    #'EFT.api',
    'yipay',
    'gefu',
])

add_global_item('ydjd_percentage_share_with_ydmm', {
    'Android_2.92_360': 3,
    'Android_3.37_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.dj': 3,
    #'Android_3.372_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall7.360.dj': 100,
})

add_global_item('pay_appid_config', {
    'Android_3.37_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.dj': {
        'ydjd': '621216015822',
    },
})
add_global_item('ydjd_paycodes', {
    '6':{
        'TY9999D0000103' : '013',
        'TY9999D0002001' : '014',
        'TY9999D0006001' : '002',
        'TY9999D0008002' : '010',
        'TY9999D0008001' : '011',
        'TY9999R0008001' : '012',
    },
    '7':{
        'TY0007D0008001' : '001',
        'TY0007D0010001' : '002',
        'TY9999R0008001' : '003',
        'TY9999D0008001' : '004',
        'TY9999D0008002' : '005',
    }
})
