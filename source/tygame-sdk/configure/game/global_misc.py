# -*- coding=utf-8 -*-

from pyscript._helper_config_ import add_global_item, add_client_item_old, \
    add_template_item

add_global_item('winpc_guest_forbidden_info', '亲，为了您的账号安全，请登录后畅玩吧~')
add_global_item('winpc_guest_forbidden_tips', '')

add_global_item('user_forbidden_info', '尊敬的用户，您的帐号{userId}已被禁止登录。请联系客服4008-098-000')
add_global_item('user_forbidden_tips', '')
#add_global_item('user_forbidden_tips', '请联系客服4008-098-000')

add_global_item('clientid_forbidden_info', '您使用的版本太低，请尽快升级到最新版本，客服联系电话4008-098-000')
add_global_item('clientid_forbidden_tips', '')

add_global_item('tyId_forbidden_info', '请使用第三方账号登录，客服联系电话4008-098-000')
add_global_item('tyId_forbidden_tips', '')

add_global_item('winpc_360qt_verify_proxy', 'http://qtverify.qipai.360.cn:8000/api.php?head_size=100_100&Q=%s&T=%s')
add_global_item('check_clientid_num_before_login', 0)

# support baifen or mandao
add_global_item('smsdown_selector', 'baifen')

#下行短信内容配置
add_global_item('smsdown_content', {
    'sendcode':'验证码:%d(为保账号安全请勿告知他人，如有疑问请拨打客服电话：4008098000)',
    'sendpwd':'%s(手机登录密码)用于使用手机号码登录你的通行证,请妥善保管。',
    'smstouser':'%s',
})

# 射雕sdk接入的游戏，此配置目的是短验下行短信控制显示射雕信息
add_global_item('shediao_appId', [10003,10029,10032,10043])

# smsup port support baifen or mandao
# mandao:106901336019
# baifen:106901408788
add_global_item('smsup_port', '106901336019')
add_global_item('smsup_content', {
    'bindcode': '%06d（途游通行证关联短信）',
    'bindcode_re': '(\d{6})（途游通行证关联短信）',
})

# Danji product ids
add_global_item('danji_prods', ['TY9999R00020DJ'])

#支付提示内容配置
add_global_item('querystatus_config', {
    'querymaxnums': '60',
    'success':{'info':'支付成功啦！',
               'content':'您于{time}成功购买{prodname}\n',
               'tips':'如有问题，请拨打客服电话：400-8098-000',
              },
    'fail':   {'info':'很抱歉，支付失败了……',
               'content':'{info}\n请您放心我们还未扣取您任何费用!',
               'tips':'如有问题，请拨打客服电话：400-8098-000',
              },
    'bug': {'info':'很抱歉，添加物品失败了……',
            'content':'啊哦~这真是太尴尬了......请您尽快联系我们的客服！我们一定会第一时间为您处理！感谢您对我们工作的支持和理解！',
            'tips':'请拨打客服电话：400-8098-000',
           },
    'timeout':{'info':'支付请求处理超时……',
               'content':'{info}\n您可以关闭该窗口继续等待，一旦添加成功，我们会第一时间通知您!',
               'tips':'如有问题，请拨打客服电话：400-8098-000',
              },
    'process':{'info':'支付请求已提交，系统正在处理中…',
               'content':'{info}',
               'tips':'如有问题，请拨打客服电话：400-8098-000',
              },
    'processinfo':{'ydmm,liantong.wo,aigame,linkyun,yipay,linkyun.ido,linkyun.api,EFTChinaTelecom.msg,EFTChinaUnion.msg':'话费不足、网络故障、卡类限制、号段区域限制、话费支付超过日限额或月限额等可能会导致充值失败',
                '360.ali,tuyou.ali,yee2.card1,yee2.card2':'余额不足，账号输入错误、网络故障等可能会导致充值失败',
                '360.card.dx,360.card.yd,360.card.lt,tuyou.card.dx,tuyou.card.yd,tuyou.card.lt':'充值卡过期、卡号输入错误、网络故障等可能会导致充值失败',
                'thirdpay':'余额不足、账户错误、网络故障等可能会导致充值失败',
                },
     'failinfo':{'ydmm,liantong.wo,aigame,linkyun,yipay,linkyun.ido,linkyun.api,EFTChinaTelecom.msg,EFTChinaUnion.msg':'话费不足、网络故障、卡类限制、号段区域限制、话费支付超过日限额或月限额等可能会导致充值失败',
                '360.ali,tuyou.ali,yee2.card1,yee2.card2':'余额不足，账号输入错误、网络故障等可能会导致充值失败',
                '360.card.dx,360.card.yd,360.card.lt,tuyou.card.dx,tuyou.card.yd,tuyou.card.lt':'充值卡过期、卡号输入错误、网络故障等可能会导致充值失败',
                'thirdpay':'余额不足、账户错误、网络故障等可能会导致充值失败',
                },
     'timeoutinfo':{'ydmm,liantong.wo,aigame,linkyun,yipay,linkyun.ido,linkyun.api,EFTChinaTelecom.msg,EFTChinaUnion.msg':'超时的原因可能包括:网络故障、网络延迟、账户限制、账户余额不足、支付超过限额等。',
                '360.ali,tuyou.ali,yee2.card1,yee2.card2':'超时的原因可能包括:网络故障、网络延迟、账户限制、账户余额不足、支付超过限额等。',
                '360.card.dx,360.card.yd,360.card.lt,tuyou.card.dx,tuyou.card.yd,tuyou.card.lt':'超时的原因可能包括:网络故障、网络延迟、账户限制、账户余额不足、支付超过限额等。',
                'thirdpay':'超时的原因可能包括:网络故障、网络延迟、账户限制、账户余额不足、支付超过限额等。',
                }
})

add_global_item('charge_categories_config', {
    '360.ali,tuyou.ali':'CAT_ALIPAY',
    'yee2.card1':'CAT_DEBIT_CARD',
    'yee2.card2':'CAT_CREDIT_CARD',
    '360.card.dx,360.card.yd,360.card.lt,tuyou.card.dx,tuyou.card.yd,tuyou.card.lt,yee.card,shenzhoufu.card':'CAT_PHONECHARGE_CARD',
    'wxpay':'CAT_WEIXIN',
})

#3.50 hall rev number 4052
add_global_item('min_revision_supporting_type0_smspayinfo', 4052)

add_global_item('qipai_ipauth', 0)
add_global_item('qipai_sign_key', 'xlZGF0YXMiOiBbeyJkYmlkIjogMTEsIC')
add_global_item('qipai_servers_ip', ['211.151.194.124', ])
add_global_item('qipai_gamecode2gameid', {
    'kxddz': 6,
    '22': 8,
})
#ios支付限制参数
add_global_item('ios_limited_config', {
    'ios_pay_total':500,#单日充值额度
    'ios_pay_waived_uids':[84267062,164323361,166779074,96734709,155837599,170362076],#uid白名单
    'pay_limit_msg':'抱歉，您今日充值额度已超过上限，请明日再来充值吧',#限额提示
    'ios_uuid_pay_amount':3000,#uuid单日充值额度
    'ios_uuid_pay_total':100,#单日充值次数
    'ios_uuid_pay_total_open':1,#是否打开充值次数判断
    'ios_uuid_limit_msg':'单日充值次数达到上限',#单日充值次数
    'ios_5mins_pay_total':195,#5分钟内充值金额限制
    'ios_gametimes_limited':3600,#玩家游戏时长限制
    'ios_gametimes_limited_open':0,#是否打开游戏时长判断
})

#同一个deviceid限制第三方账号注册配置
add_global_item('deviceid_sns_config', {
    'new_user_numbers':5,
    'new_limit_msg':'对不起，您的设备注册已达上限',
    'login_user_numbers':10,
    'login_limit_msg':'对不起，您切换账号的数量已达上限',
})

add_global_item('kaiping_configs', {
    # client_id -> client_secret, pay_key, login_key, ty_gameid
    'vdhscvnmqvf': ('3131225641340672', 'mUmpHL5kHyllYrhta85WhYsTRtuKe6Pf', 'lLzMqfQVQ7dFogxG7afojd7tfWyPRo3O', 6),
    'vdhsvngytan': ('3018250369010836', 'ogk210Z173Y4lRg8cKUHup2et4HQ9iqX', 'yluqYs2yTZymyqznj2xDeQfKknDbBl01', 7),
    'vdhsnnsbnci': ('3062077356074294', '81vnNCfDyisyeKfIY1cpPXjsRyFkw3ZJ', 'G4p5Vi2RfsgVabUFkjR10xsrCiiCNSmL', 8),
    'wxztozmsaaj': ('3254520932069741', 'CybDpfBy2s4Eruud8buKcE7WqEsVYDcY', 'zxO6AFz9Hz5EhGrrfuXrxy0QNIVM795R', 6),
    'wxzyugyelws': ('3254521519272346', 'DN8EG2FaFbsckdfR1rrxYVIrfjfkxOil', 'VQoLpzk0eCJZy2rYkPNoeWUziHrbHEG4', 6),
    'wzqocfpkxxo': ('3254522123252199', 'kNCCJxkm8Up06P3x1sslx7SGgNR8I0cQ', 'qmFaHa8MWrpIQ7y0zthbNLM7oSNbor5E', 7),
    'wzqogiyfvor': ('3254522727232057', 'DDWugy04T0FJEHdXpCgob9eRKsZQMVtj', 'vKdCthYCS1a29l7VfAmCD4UKha902fc0', 7),
    'xkmpqnrliww': ('', 'wqWs5OTv7ypu4K0WMMEa3taqDhfCtWN9', 'YWnc21JOVLq99KIudjWztkOe7dZ1c5qo', 3),
    'xqzkdofovaq': ('', 'mSRbkBUQv5dtyRZil6HEG9fPWkPqYW5K', 'AfFwSVGoYxMvW3qJM1YlnhgfpsLd1CzP', 3),
})

