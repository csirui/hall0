# -*- coding=utf-8 -*-
'''
Created on 2014年5月22日

@author: ZQH
'''

from tyframework._private_.bi.activityid import ActivityId
from tyframework._private_.bi.bieventid import BIEventId
from tyframework._private_.bi.bireport import BiReport
from tyframework._private_.bi.biutils import BiUtils
from tyframework._private_.bi.chipmode import ChipNotEnoughOpMode
from tyframework._private_.bi.giftid import GiftId
from tyframework._private_.configure.configure import Configure
from tyframework._private_.configure.tyglobal import TYGlobal
from tyframework._private_.configure.tysync import TySync
from tyframework._private_.dao.authorcode import AuthorCode
from tyframework._private_.dao.day1st import Day1st
from tyframework._private_.dao.paytype import PayType
from tyframework._private_.dao.smspaycheck import SmsPayCheck
from tyframework._private_.dao.userprops import UserProps
from tyframework._private_.dao.usersession import UserSession
from tyframework._private_.dataswap.dataswap2 import MySqlSwap2
from tyframework._private_.dbmysql.db_mysql import DbMySql
from tyframework._private_.dbredis.db_cluster import RedisCluster
from tyframework._private_.dbredis.db_single import RedisSingle
from tyframework._private_.events.tyevent import TYEvent
from tyframework._private_.events.tyeventbus import TYEventBus
from tyframework._private_.events.tyeventhandler import TYEventHandler
from tyframework._private_.logic.clientutils import ClientUtils
from tyframework._private_.logic.online import OnLine
from tyframework._private_.logic.robot import RobotClient
from tyframework._private_.logic.timer import GameTimer
from tyframework._private_.msg.msg import MsgPack
from tyframework._private_.msg.msgline import MsgLine
from tyframework._private_.runmode.http.runhttp import RunHttp
from tyframework._private_.runmode.run import TYRun
from tyframework._private_.runmode.runmode import RunMode
from tyframework._private_.runmode.servercontrol import ServerControl
from tyframework._private_.util.cache import Cache
from tyframework._private_.util.channel import NWChannel
from tyframework._private_.util.city_locator import CityLocator
from tyframework._private_.util.closewebview import CloseWebView
from tyframework._private_.util.constants import Const
from tyframework._private_.util.exception import FreetimeException, \
    GlobalLockerException
from tyframework._private_.util.exception import MySqlSwapException
from tyframework._private_.util.exception import TimeoutException
from tyframework._private_.util.fileutil import fileutil
from tyframework._private_.util.ftlog import ftlog
from tyframework._private_.util.geohash import GeoHash
from tyframework._private_.util.globallocker import GlobaclLocker
from tyframework._private_.util.iccid_loc import IccidLoc
from tyframework._private_.util.ip_loc import IPLoc
from tyframework._private_.util.ip_loc2 import IPLoc2
from tyframework._private_.util.ipaddr import IPAddress, IPNetwork
from tyframework._private_.util.keyword_filter import KeywordFilter
from tyframework._private_.util.libcffi.cffiloader import CffiLoader
from tyframework._private_.util.lockattr import LockAttr
from tyframework._private_.util.locker import Locker
from tyframework._private_.util.osenv import OsEnv
from tyframework._private_.util.phone_loc import PhoneTrie
from tyframework._private_.util.regexp import RegExp
from tyframework._private_.util.smsdown import SmsDownSelector
from tyframework._private_.util.strutil import strutil
from tyframework._private_.util.timestamp import TimeStamp
from tyframework._private_.util.tydeffer import TyDeffer
from tyframework._private_.util.webpage import WebPage
from tyframework.private.interface import GData
from tyframework.private.servers.protocol.tytasklet.helper import TaskletHelper


class TyContext:
    def __init__(self):
        self.ftlog = ftlog  # Singleton
        self.strutil = strutil  # Singleton
        self.fileutil = fileutil  # Singleton
        self.CffiLoader = CffiLoader  # Singleton
        self.TimeoutException = TimeoutException  # Class
        self.MySqlSwapException = MySqlSwapException  # Class
        self.FreetimeException = FreetimeException  # Class
        self.GlobalLockerException = GlobalLockerException  # Class
        self.GeoHash = GeoHash  # Singleton
        self.KeywordFilter = KeywordFilter  # Singleton
        self.TimeStamp = TimeStamp  # Singleton
        self.OsEnv = OsEnv  # Singleton
        self.RegExp = RegExp  # Singleton
        self.WebPage = WebPage  # Singleton
        self.Locker = Locker  # Class
        self.NWChannel = NWChannel  # Class
        self.Cache = Cache  # Singleton
        self.TyDeffer = TyDeffer  # Singleton
        self.CityLocator = CityLocator  # Singleton
        self.TYEvent = TYEvent  # Class
        self.TYEventBus = TYEventBus  # Class
        self.TYEventHandler = TYEventHandler  # Class
        self.ClientUtils = ClientUtils  # Singleton
        self.TYGlobal = TYGlobal  # Singleton
        self.TySync = TySync  # Singleton
        self.MySqlSwap = MySqlSwap2  # Singleton
        self.GameTimer = GameTimer  # Class
        self.RobotClient = RobotClient  # Class

        self.ActivityId = ActivityId  # Singleton
        self.BIEventId = BIEventId  # Singleton
        self.BiReport = BiReport  # Singleton
        self.BiUtils = BiUtils  # Singleton
        self.ChipNotEnoughOpMode = ChipNotEnoughOpMode  # Singleton
        self.GiftId = GiftId  # Singleton

        self.MsgPack = MsgPack  # Class
        self.Cls_MsgPack = MsgPack
        self.MsgLine = MsgLine  # Class

        self.DbMySql = DbMySql
        self.RedisUser = RedisCluster()  # 用户数据库
        self.RedisGame = RedisCluster()  # 游戏数据库
        self.RedisConfig = RedisSingle()  # 配置数据库
        self.RedisMix = RedisSingle()  # 混合数据库
        self.RedisAvatar = RedisSingle()  # 头像数据库
        self.RedisPayData = RedisSingle()  # 支付数据库
        self.RedisUserKeys = RedisSingle()  # 用户ID键值对应数据库
        self.RedisBiCount = RedisSingle()  # BI统计数据库
        self.RedisOnline = RedisCluster()  # 在线状态数据库
        self.RedisOnlineGeo = RedisSingle()  # 在线地理位置数据库
        self.RedisFriendMix = RedisSingle()  # 好友数据库
        self.RedisLocker = RedisSingle()  # 全局资源锁数据库
        self.RedisTableData = RedisCluster()  # 桌子状态数据库
        self.RedisForbidden = RedisSingle()  # 禁止登陆数据库

        self.TYRun = TYRun  # Singleton tasklet管理器
        self.RunHttp = RunHttp  # Singleton Http协议tasklet工具类
        self.IPAddress = IPAddress
        self.IPNetwork = IPNetwork

        self.RunMode = RunMode  # Singleton 运行模式检查器
        self.ServerControl = ServerControl  # Singleton 服务登陆、API转发定义
        self.UserSession = UserSession  # Singleton
        self.SmsPayCheck = SmsPayCheck  # Singleton
        self.PayType = PayType  # Singleton
        self.IccidLoc = IccidLoc  # Singleton
        self.Const = Const
        self.IPLoc = IPLoc
        self.IPLoc2 = IPLoc2
        self.PhoneTrie = PhoneTrie
        self.AuthorCode = AuthorCode  # Singleton
        self.Day1st = Day1st  # Singleton
        self.UserProps = UserProps  # Singleton

        self.OnLine = OnLine  # Class, can be Singleton
        self.Configure = Configure  # Singleton

        self.GData = GData()  # 全局控制数据中心

        self.GlobaclLocker = GlobaclLocker
        self.SmsDown = SmsDownSelector
        self.CloseWebView = CloseWebView

        LockAttr.lock(self)

    def getTasklet(self):
        return TaskletHelper.getTasklet()

    def _init_ctx_(self):
        for pname in dir(self):
            attobj = getattr(self, pname)
            _init_ctx_ = getattr(attobj, '_init_ctx_', None)
            if _init_ctx_ != None and callable(_init_ctx_):
                _init_ctx_()
        self._init_ctx_ = None

    def _init_singleton_(self):
        for pname in dir(self):
            attobj = getattr(self, pname)
            _init_singleton_ = getattr(attobj, '_init_singleton_', None)
            if _init_singleton_ != None and callable(_init_singleton_):
                self.ftlog.debug('_init_singleton_', pname)
                _init_singleton_()
        self._init_singleton_ = None


# self.ftlog.info('========= string code image ========')
#         self.ftlog.info('normal define : 123456->', type('123456'), repr('123456'))
#         self.ftlog.info('unicode define : 123456->', type(u'123456'), repr(u'123456'))
#         self.ftlog.info('normal define chinese: 你好 ->', type('你好'), repr('你好'))
#         self.ftlog.info('unicode define chinese : 你好 ->', type(u'你好'), repr(u'你好'))
#         str1 = self.RedisConfig.execute('get', 'configitems:game:8:sng_matchs_no_reward_desc')
#         self.ftlog.info('data from redis : str1->', type(str1), repr(str1))
#         str2 = self.RedisConfig.execute('get', 'configitems:game:6:ios.five.star.slam')
#         data2 = self.strutil.loads(str2)
#         data2 = data2['desc']
#         self.ftlog.info('data from redis json loads data2->', type(data2), repr(data2))
#         self.ftlog.info('========= string code image ========')

TyContext = TyContext()
