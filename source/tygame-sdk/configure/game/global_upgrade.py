# -*- coding=utf-8 -*-
from pyscript._helper_config_ import *

'''
INC update id : clients.inc.upgrade.map
FULL update id: clients.full.upgrade.map
DIFF update id: clients.diff.upgrade.map
'''

# 增量更新
add_game_item_old(9999, 'clients.inc.upgrade.map', {                                                                                                                                                       
  "Android_3.33_360.360.0-hall6.360.laizi360": [
    {
      "force": "0",
      "des": "1、减少耗电量\n2、加快游戏启动速度\n3、解决部分玩家不能比赛的问题\n\n更新文件大小: 162K",
      "path": "http://ddz.dl.tuyoo.com/update/update_package_v3.zip",
      "md5": "ZZZZZZZZZZZZZZZZZZZZZZZZZZ",
      "id": 1,
      "size": "169KB",
      "autoDownloadCondition": 7,
    }
  ],
  "Android_3.33_360.360.0-hall6.360.tu360": [
    {
      "force": "0",
      "des": "1、减少耗电量\n2、加快游戏启动速度\n3、解决部分玩家不能比赛的问题\n\n更新文件大小: 162K",
      "path": "http://ddz.dl.tuyoo.com/update/update_package_v3.zip",
      "md5": "ZZZZZZZZZZZZZZZZZZZZZZZZZZ",
      "id": 1,
      "size": "169KB",
      "autoDownloadCondition": 7,
    }
    ],
  "IOS_3.76_tyGuest,tyAccount,weixin.appStore.0-hall6.tuyoo.huanle": [
    {
      "force": "0",
      "des": " 人生如戏\n 全靠演技",
      "path": "http://ddz.dl.tuyoo.com/cdn37/hall/update/hall_3.76_test_01.zip",
      "md5": "966e26ceab6cd78dc2229667febba86d",
      "id": 1,
      "size": "888KB",
      "autoDownloadCondition": 0,
    }
  ]
})

# 全量更新
# http://125.39.218.101/open/v3/getUpdateInfo2?gameId=9999&clientId=Android_3.50_360.360.0-hall6.360.day&hallVersion=6&updateVersion=0&nicaiCode=863567814
# autoDownloadCondition 自动下载条件
# updateAt 更新时游戏在哪个界面
#   background - 更新时在后台，点击确定后，开始下载APK，同时游戏进入下一个场景
#   其他值，停留在更新界面下载
# 下载完成后开始APK安装
# alphaVersion 没有该设置则支持所有额包
#   有则支持此版本号的包
# v3.501版本全量非强制非自动提示更新，上线前合并代码需确认
add_game_item_old(9999, 'clients.full.upgrade.map', {
  # 1
  "Android_3.501_360.360,weakChinaMobile,woStore,aigame,YDJD.0-hall6.360.dj": [
    {
      "force": "0",
      "des": "1、优化游戏性能及体验\n\n2、修复支付宝支付bug\n\n更新文件大小: 19M",
      "path": "http://ddz.dl.tuyoo.com/apk/501shengji.apk",
      "md5": "2ec74a0a52deb1a8c52adce41b9b94a6",
      "id": 1,
      "size": "19200KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  # 2
  "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.qq.dj": [
    {
      "force": "0",
      "des": "1、优化游戏性能及体验\n\n2、修复支付宝支付bug\n\n更新文件大小: 19M",
      "path": "http://ddz.dl.tuyoo.com/apk/501shengji.apk",
      "md5": "2ec74a0a52deb1a8c52adce41b9b94a6",
      "id": 1,
      "size": "19200KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  # 3
  "Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.coolpad.dj": [
    {
      "force": "0",
      "des": "1、优化游戏性能及体验\n\n2、修复支付宝支付bug\n\n更新文件大小: 19M",
      "path": "http://ddz.dl.tuyoo.com/apk/501shengji.apk",
      "md5": "2ec74a0a52deb1a8c52adce41b9b94a6",
      "id": 1,
      "size": "19200KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  # 4
  "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.wifikey.dj": [
    {
      "force": "0",
      "des": "1、优化游戏性能及体验\n\n2、修复支付宝支付bug\n\n更新文件大小: 19M",
      "path": "http://ddz.dl.tuyoo.com/apk/501shengji.apk",
      "md5": "2ec74a0a52deb1a8c52adce41b9b94a6",
      "id": 1,
      "size": "19200KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  # 5
  "Android_3.501_tuyoo.lenovo,weakChinaMobile,woStore,aigame,YDJD.0-hall6.lenovo.dj": [
    {
      "force": "0",
      "des": "1、优化游戏性能及体验\n\n2、修复支付宝支付bug\n\n更新文件大小: 19M",
      "path": "http://ddz.dl.tuyoo.com/apk/501shengji.apk",
      "md5": "2ec74a0a52deb1a8c52adce41b9b94a6",
      "id": 1,
      "size": "19200KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  # 6
  "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.ali.dj": [
    {
      "force": "0",
      "des": "1、优化游戏性能及体验\n\n2、修复支付宝支付bug\n\n更新文件大小: 19M",
      "path": "http://ddz.dl.tuyoo.com/apk/501shengji.apk",
      "md5": "2ec74a0a52deb1a8c52adce41b9b94a6",
      "id": 1,
      "size": "19200KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  # 7
  "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.wandou.dj": [
    {
      "force": "0",
      "des": "1、优化游戏性能及体验\n\n2、修复支付宝支付bug\n\n更新文件大小: 19M",
      "path": "http://ddz.dl.tuyoo.com/apk/501shengji.apk",
      "md5": "2ec74a0a52deb1a8c52adce41b9b94a6",
      "id": 1,
      "size": "19200KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  # 8
  "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.tianyu.dj": [
    {
      "force": "0",
      "des": "1、优化游戏性能及体验\n\n2、修复支付宝支付bug\n\n更新文件大小: 19M",
      "path": "http://ddz.dl.tuyoo.com/apk/501shengji.apk",
      "md5": "2ec74a0a52deb1a8c52adce41b9b94a6",
      "id": 1,
      "size": "19200KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  # 9
  "Android_3.501_tuyoo.weakChinaMobile,woStore,aigame,YDJD.0-hall6.jinli.dj": [
    {
      "force": "0",
      "des": "1、优化游戏性能及体验\n\n2、修复支付宝支付bug\n\n更新文件大小: 19M",
      "path": "http://ddz.dl.tuyoo.com/apk/501shengji.apk",
      "md5": "2ec74a0a52deb1a8c52adce41b9b94a6",
      "id": 1,
      "size": "19200KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  # 10
  "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.sougou.dj": [
    {
      "force": "0",
      "des": "1、优化游戏性能及体验\n\n2、修复支付宝支付bug\n\n更新文件大小: 19M",
      "path": "http://ddz.dl.tuyoo.com/apk/501shengji.apk",
      "md5": "2ec74a0a52deb1a8c52adce41b9b94a6",
      "id": 1,
      "size": "19200KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  # 11
  "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.tuyoo.dj": [
    {
      "force": "0",
      "des": "1、优化游戏性能及体验\n\n2、修复支付宝支付bug\n\n更新文件大小: 19M",
      "path": "http://ddz.dl.tuyoo.com/apk/501shengji.apk",
      "md5": "2ec74a0a52deb1a8c52adce41b9b94a6",
      "id": 1,
      "size": "19200KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  # 12
  "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.kunda.dj": [
    {
      "force": "0",
      "des": "1、优化游戏性能及体验\n\n2、修复支付宝支付bug\n\n更新文件大小: 19M",
      "path": "http://ddz.dl.tuyoo.com/apk/501shengji.apk",
      "md5": "2ec74a0a52deb1a8c52adce41b9b94a6",
      "id": 1,
      "size": "19200KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  # 13
  "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.litianbaoli.dj": [
    {
      "force": "0",
      "des": "1、优化游戏性能及体验\n\n2、修复支付宝支付bug\n\n更新文件大小: 19M",
      "path": "http://ddz.dl.tuyoo.com/apk/501shengji.apk",
      "md5": "2ec74a0a52deb1a8c52adce41b9b94a6",
      "id": 1,
      "size": "19200KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  # 14
  "Android_3.501_tuyoo.woStore,aigame,YDJD.0-hall6.leshiphone.dj": [
    {
      "force": "0",
      "des": "1、优化游戏性能及体验\n\n2、修复支付宝支付bug\n\n更新文件大小: 19M",
      "path": "http://ddz.dl.tuyoo.com/apk/501shengji.apk",
      "md5": "2ec74a0a52deb1a8c52adce41b9b94a6",
      "id": 1,
      "size": "19200KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  # 15
  "Android_3.501_tuyoo.duoku,weakChinaMobile,YDJD.0-hall6.91new.dj": [
    {
      "force": "0",
      "des": "1、优化游戏性能及体验\n\n2、修复支付宝支付bug\n\n更新文件大小: 19M",
      "path": "http://ddz.dl.tuyoo.com/apk/501shengji.apk",
      "md5": "2ec74a0a52deb1a8c52adce41b9b94a6",
      "id": 1,
      "size": "19200KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  # 16
  "Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.duokunew.dj": [
    {
      "force": "0",
      "des": "1、优化游戏性能及体验\n\n2、修复支付宝支付bug\n\n更新文件大小: 19M",
      "path": "http://ddz.dl.tuyoo.com/apk/501shengji.apk",
      "md5": "2ec74a0a52deb1a8c52adce41b9b94a6",
      "id": 1,
      "size": "19200KB",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
   # 17
  "Android_3.72_tyGuest.ucdanji.0-hall8.uc.day": [
    {
      "force": "0",
      "des": "1、全新装扮，炫到无敌\n\n2、升级免费赢奖\n\n更新文件大小: 50M",
      "path": "http://ddz.dl.tuyoo.com/apk/Game-texas-3.72-tyGuest.ucdanji.0-hall8.uc.day.301.apk",
      "md5": "680bef2d44ea66c41afcd6dfcd5dfd23",
      "id": 1,
      "size": "50M",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
   # 18
  "Android_3.60_360.360.0-hall8.360.day": [
    {
      "force": "0",
      #"des": "1、全新装扮，炫到无敌\n\n2、升级免费赢奖\n\n更新文件大小: 50M",
      "des": "全新3.75版德州，增加牌局回顾、德州月卡等多种功能，升级可获取更多奖励",
      "path": "http://apk.dl.tuyoo.com/down/dezhou/Game-texas-3.75-360.360.0-hall8.360.day.41.apk",
      "md5": "d2750ba866e3f3f260555feb1ba0d862",
      "id": 1,
      "size": "50M",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.60_360.360.0-hall8.360.tu": [
    {
      "force": "0",
      #"des": "1、全新装扮，炫到无敌\n\n2、升级免费赢奖\n\n更新文件大小: 50M",
      "des": "全新3.75版德州，增加牌局回顾、德州月卡等多种功能，升级可获取更多奖励",
      "path": "http://apk.dl.tuyoo.com/down/dezhou/Game-texas-3.75-360.360.0-hall8.360.tu.44.apk",
      "md5": "d52381a59eb9fcbdb792b200ff8d9d85",
      "id": 1,
      "size": "50M",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.60_360.360.0-hall8.360.fk": [
    {
      "force": "0",
      #"des": "1、全新装扮，炫到无敌\n\n2、升级免费赢奖\n\n更新文件大小: 50M",
      "des": "全新3.75版德州，增加牌局回顾、德州月卡等多种功能，升级可获取更多奖励",
      "path": "http://apk.dl.tuyoo.com/down/dezhou/Game-texas-3.75-360.360.0-hall8.360.fk.40.apk",
      "md5": "53ec02fa17693cb47e4c466e72b6bb1b",
      "id": 1,
      "size": "50M",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.60_tuyoo.tuyoo.0-hall8.qq.tu": [
    {
      "force": "0",
      #"des": "1、全新装扮，炫到无敌\n\n2、升级免费赢奖\n\n更新文件大小: 50M",
      "des": "全新3.75版德州，增加牌局回顾、德州月卡等多种功能，升级可获取更多奖励",
      "path": "http://apk.dl.tuyoo.com/down/dezhou/Game-texas-3.75-tyOneKey,tyAccount,tyGuest.tuyoo.0-hall8.qq.tu.45.apk",
      "md5": "6bd2e8fdac19804b70f26c1891f09453",
      "id": 1,
      "size": "50M",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.60_360.360.0-hall8.360.win": [
    {
      "force": "0",
      #"des": "1、全新装扮，炫到无敌\n\n2、升级免费赢奖\n\n更新文件大小: 50M",
      "des": "全新3.75版德州，增加牌局回顾、德州月卡等多种功能，升级可获取更多奖励",
      "path": "http://apk.dl.tuyoo.com/down/dezhou/Game-texas-3.75-360.360.0-hall8.360.win.75.apk",
      "md5": "dfd909d2d0079590b39cff6cdb0a16f0",
      "id": 1,
      "size": "50M",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
  "Android_3.60_tuyoo.tuyoo.0-hall8.tuyoo.tu": [
    {
      "force": "0",
      #"des": "1、全新装扮，炫到无敌\n\n2、升级免费赢奖\n\n更新文件大小: 50M",
      "des": "全新3.75版德州，增加牌局回顾、德州月卡等多种功能，升级可获取更多奖励",
      "path": "http://apk.dl.tuyoo.com/down/dezhou/Game-texas-3.75-tyOneKey,tyAccount,tyGuest.tuyoo.0-hall8.tuyoo.tu.46.apk",
      "md5": "be743d98a9c0d21d2f242450f6a1b57f",
      "id": 1,
      "size": "50M",
      "autoDownloadCondition": 0,
      "updateAt": "front",
    }
  ],
}

)


# # DIFF更新，MD5为PATCH之后的APK的MD5
# # test case
# # http://125.39.218.101/open/v3/getUpdateInfo2?gameId=9999&clientId=Android_3.502_360.360.0-hall6.360.day&hallVersion=6&updateVersion=0&nicaiCode=863567814
# add_game_item_old(9999, 'clients.diff.upgrade.map', {                                                                                                                                                       
#   "Android_3.502_360.360.0-hall6.360.day": [
#     {
#       "force": "0",
#       "des": "1、测试差分更新\n\n更新文件大小: 0.2M",
#       "path": "http://ddz.dl.tuyoo.com/update/update_package_v3.patch",
#       "md5": "ZZZZZZZZZZZZZZZZZZZZZZZZZZ",
#       "id": 1,
#       "size": "169KB",
#       "autoDownloadCondition": 7,
#       "updateAt": "background",
#     }
#   ]
# })
