# -*- coding=utf-8 -*-
'''
第三方接入。
第三方的appID从10000开始
第三方的appKey使用此文件产生
'''
from hashlib import md5

def creatAppKey(joinTime, appName, appId, monkey):
    rstr = str(joinTime) + '_' + str(appName) + '_' + str(appId) + '_' + str(monkey)
    m = md5()
    m.update(rstr)
    ret = m.hexdigest()
    return ret

# 德州扑克
joinTime = '2013-08-01 12:01:01'
monkey = 'adshfqh31234lakjf092309'
appName = '德州扑克'
appId = 10001
deliveryUrl = 'http://119.254.84.152/callback/tuyou'
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl

joinTime = '2013-08-01 12:02:02'
monkey = 'lkadfwaeoiewqjsxcv23sadfasd09132'
appName = '爆走貂蝉'
appId = 10002
deliveryUrl = 'http://42.62.53.142:9012/deposit'
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl

joinTime = '2013-08-01 12:03:03'
monkey = 'asdfadsfewq9230-fdsgvaswqer23'
appName = '一剑灭天'
appId = 10003
deliveryUrl = 'http://42.62.53.142:9012/deposit'
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl


joinTime = '2013-09-01 12:03:03'
monkey = 'adfadjfhkjhqweur23lddva230-fdsgvaswqer23'
appName = '天天西游'
appId = 10004
deliveryUrl = 'http://42.62.53.142:9012/deposit'
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl

joinTime = '2013-09-01 12:03:03'
monkey = 'adlkfajsflkjahdsf234123-fdsgvaswqer23'
appName = '神曲'
appId = 10005
deliveryUrl = 'http://42.62.53.142:9012/deposit'
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl

joinTime = '2013-09-01 12:03:03'
monkey = 'adlkfajsflkjahdsf234123-983saahsfddsa'
appName = '三国志Q传'
appId = 10006
deliveryUrl = 'http://42.62.53.142:9012/deposit'
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl

joinTime = '2013-10-22 12:03:03'
monkey = 'adasdfasdq34513532432ahdsf234123-983saahsfddsa'
appName = '途游十三张'
appId = 10007
deliveryUrl = 'http://42.62.53.142:9012/deposit'
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl

joinTime = '2013-11-18 12:03:03'
monkey = 'asasdfasfa432ahdsf2a34w123-34rfcv32'
appName = '精灵联盟'
appId = 10008
deliveryUrl = 'http://42.62.53.142:9012/deposit'
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl


joinTime = '2014-02-12 12:03:03'
monkey = 'aswsxvdasdfasfa432ahdsf2a34w123-34rfcv32'
appName = '飘飘欲仙'
appId = 10009
deliveryUrl = 'http://42.62.59.61/ms/tuyoo/pay.jsp'
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl


joinTime = '2014-02-20 12:03:03'
monkey = 'aswsxvdasdfasfa432ahdsf2a34w123-34rfcv32'
appName = '勇士联盟'
appId = 10010
deliveryUrl = ''
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl


joinTime = '2014-02-24 12:03:03'
monkey = 'aswsxvdasdfasfa432ahdsf2a34w123-34rfcv32'
appName = '战神黎明'
appId = 10011
deliveryUrl = ''
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl


joinTime = '2014-03-03 12:03:03'
monkey = 'aswsxvdasdfasfa432ahdsf2a34w123-34rfcv32'
appName = '刀塔传奇'
appId = 10012
deliveryUrl = ''
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl

joinTime = '2014-04-02 12:03:03'
monkey = 'aswsxvdasdfasfa432ahdsf2a34w123-34rfcv32'
appName = '新神曲'
appId = 10013
deliveryUrl = ''
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl


joinTime = '2014-04-22 12:03:03'
monkey = 'aswsxvdasdfasfa432ahdsf2a34w123-34rfcv32'
appName = '妖精的尾巴'
appId = 10014
deliveryUrl = ''
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl

joinTime = '2014-04-24 11:03:03'
monkey = 'aswsxvdasdfasfa432ahdsf2a34w123-34rfcv32'
appName = '媚三国'
appId = 10015
deliveryUrl = ''
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl

joinTime = '2014-06-18 15:03:03'
monkey = 'aswsxvdasdfasfa432ahdsf2a34w123-34rfcv32'
appName = '水果连萌'
appId = 10016
deliveryUrl = ''
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl

joinTime = '2014-06-21 15:53:03'
monkey = 'aswsxvdasdfasfa432ahdsf2a34w123-34rfcv32'
appName = '战神黎明Android'
appId = 10018
deliveryUrl = ''
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl

#已经生成
#appName = '噼啪三张牌Android'
#appId = 10019

joinTime = '2014-10-08 15:53:03'
monkey = 'aswsxvdasdfasfa432ahdsf2a34w123-34rfcv32'
appName = '噼啪三张牌IOS'
appId = 10020
deliveryUrl = ''
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl

joinTime = '2014-10-08 11:43:03'
monkey = 'aswsqtrzxvclae2302340lsfg0ajq34rl%@)(v32'
appName = '全民三国'
appId = 10021
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey

joinTime = '2015-01-07 19:43:33'
monkey = 'aswsqtrzxvclae2302340ldfg-ajk34rlm0)-v)2'
appName = '第五元素'
appId = 10022
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey


joinTime = '2015-01-13 22:43:33'
monkey = 'afd(&($%()sadouasdlfafjdI&*(&(4rlm0)-v)2'
appName = '天将雄师OL'
appId = 10023
appKey = creatAppKey(joinTime, appName, appId, monkey)
print 'name=', appName, 'appId=', appId, 'appKey=', appKey

joinTime = '2015-06-15 20:43:33'
monkey = 'sldfasdwerq0sdvnxcqrtq0934q)*(&%0w3rnl)2'
appName = '这不是刀塔'
appId = 10024
appKey = creatAppKey(joinTime, appName, appId, monkey)
print 'name=', appName, 'appId=', appId, 'appKey=', appKey

joinTime = '2015-07-06 09:56:35'
monkey = 'asdfdsdddsfdsfdsfdsfa&*fdsafdre()s@saf#'
appName = '远古纷争'
appId = 10025
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey

joinTime = '2015-07-24 18:17:22'
monkey = 'adlkfajsflkjahdsf2341dfdfdf23-fdsgvaswqer23'
appName = 'Yo怪兽'
appId = 10026
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl


joinTime = '2015-09-09 17:03:28'
monkey = 'adlkfajsflkjahdsf2341dfadsdfasdfdfdfdf23-fdsgvaswqer23'
appName = '天天赢三张'
appId = 10027
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl

joinTime = '2015-09-23 17:03:28'
monkey = 'adlkfajsflkjahdsf2341dfdssdfdfdf23-fdsgvaswqer23'
appName = '长留修仙传'
appId = 10028
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl
joinTime = '2015-09-23 14:44:28'
monkey = 'adlkfajsflkjahdsf2sdsjljoi341dfdssdfdfdf23-fdsgvaswqer23'
appName = '战神之光'
appId = 10029
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl

joinTime = '2015-09-23 14:51:28'
monkey = 'adlkfajsflkjahdsf2sdssqqjoi341dfdssdfdfdf23-fdsgvaswq'
appName = '灵域修真'
appId = 10030
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl

joinTime = '2015-10-26 14:51:28'
monkey = 'adlkfajsflkjahdsf2sdssqqjoi341dfdssdfdfdf23-fdsgvaswq'
appName = '圣杯传奇'
appId = 10031
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl

joinTime = '2015-10-30 14:51:28'
monkey = 'adlkfajsflkjahdsf2sdssqqjoi341dfdssdfdfdf23-fdsgvaswq'
appName = 'Yo怪兽射雕'
appId = 10032
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl

joinTime = '2015-11-07 14:51:28'
monkey = 'adlkfajsflkjahdsf2sdssqqjoi341dfdssdfdfdf23-fdsgvaswq'
appName = '海外噼啪三张牌'
appId = 10033
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl

joinTime = '2015-11-21 14:51:28'
monkey = 'adlkfajsflkjahdsf2sdssqqjoi341dfdssdfdfdf23-fdsgvaswq'
appName = '蜀山剑仙'
appId = 10034
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl

joinTime = '2015-11-23 14:51:28'
monkey = 'adlkfajsflkjahdsf2sdssqqjoi341dfdssdfdfdf23-fdsgvaswq'
appName = '任性超神'
appId = 10035
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl

joinTime = '2015-12-28 14:51:28'
monkey = 'adlkfajsflkjahdsf2sdssqqjoi341dfdssdfdfdf23-fdsgvaswq'
appName = '天天赢三张'
appId = 10036
appKey = creatAppKey(joinTime, appName, appId, monkey)

print 'name=', appName, 'appId=', appId, 'appKey=', appKey, 'deliveryUrl=', deliveryUrl

#360PC棋牌的应用，appid从1000/2000开始
#1001, '开心斗地主',
#1010, '捕鱼',
#1011, '经典斗地主',
#1012, '开心象棋',
#1013, '三消',
#1015, '开心升级',
#1016, '欢乐麻将',
#2000, '血战麻将',
#2001, '疯狂牛仔',
joinTime = '2015-02-11 12:43:33'
monkey = 'afd(&($%()sad0q2jadfva80Q4325=354-0)-v)2'
appName = '360 app 1001'
appId = 1001
appKey = creatAppKey(joinTime, appName, appId, monkey)
print 'name=', appName, 'appId=', appId, 'appKey=', appKey

joinTime = '2015-02-11 12:43:33'
monkey = 'afd(&($%()sad0q2jadfva80Q4325=354-0)-v)2'
appName = '360 app 1010'
appId = 1010
appKey = creatAppKey(joinTime, appName, appId, monkey)
print 'name=', appName, 'appId=', appId, 'appKey=', appKey

joinTime = '2015-02-11 12:43:33'
monkey = 'afd(&($%()sad0q2jadfva80Q4325=354-0)-v)2'
appName = '360 app 1011'
appId = 1011
appKey = creatAppKey(joinTime, appName, appId, monkey)
print 'name=', appName, 'appId=', appId, 'appKey=', appKey

joinTime = '2015-02-11 12:43:33'
monkey = 'afd(&($%()sad0q2jadfva80Q4325=354-0)-v)2'
appName = '360 app 1012'
appId = 1012
appKey = creatAppKey(joinTime, appName, appId, monkey)
print 'name=', appName, 'appId=', appId, 'appKey=', appKey

joinTime = '2015-02-11 12:43:33'
monkey = 'afd(&($%()sad0q2jadfva80Q4325=354-0)-v)2'
appName = '360 app 1013'
appId = 1013
appKey = creatAppKey(joinTime, appName, appId, monkey)
print 'name=', appName, 'appId=', appId, 'appKey=', appKey

joinTime = '2015-02-11 12:43:33'
monkey = 'afd(&($%()sad0q2jadfva80Q4325=354-0)-v)2'
appName = '360 app 1015'
appId = 1015
appKey = creatAppKey(joinTime, appName, appId, monkey)
print 'name=', appName, 'appId=', appId, 'appKey=', appKey

joinTime = '2015-02-11 12:43:33'
monkey = 'afd(&($%()sad0q2jadfva80Q4325=354-0)-v)2'
appName = '360 app 1016'
appId = 1016
appKey = creatAppKey(joinTime, appName, appId, monkey)
print 'name=', appName, 'appId=', appId, 'appKey=', appKey

joinTime = '2015-02-11 12:43:33'
monkey = 'afd(&($%()sad0q2jadfva80Q4325=354-0)-v)2'
appName = '360 app 2000'
appId = 2000
appKey = creatAppKey(joinTime, appName, appId, monkey)
print 'name=', appName, 'appId=', appId, 'appKey=', appKey

joinTime = '2015-02-11 12:43:33'
monkey = 'afd(&($%()sad0q2jadfva80Q4325=354-0)-v)2'
appName = '360 app 2001'
appId = 2001
appKey = creatAppKey(joinTime, appName, appId, monkey)
print 'name=', appName, 'appId=', appId, 'appKey=', appKey


