# -*- coding=utf-8 -*-

from tyframework._private_.dao.userprops_.checkhalldata import CheckHallData
from tyframework._private_.dao.userprops_.gamedata import GameData
from tyframework._private_.dao.userprops_.playerdata import PlayerData
from tyframework._private_.dao.userprops_.tabledata import TableData
from tyframework._private_.dao.userprops_.userchip import UserChip
from tyframework._private_.dao.userprops_.userdata import UserData
from tyframework._private_.dao.userprops_.useritem import UserItem
from tyframework._private_.dao.userprops_.usermedal import UserMedal
from tyframework._private_.dao.userprops_.uservip import UserVip


class UserProps(UserData, GameData, UserChip,
                UserItem, UserVip, CheckHallData,
                TableData, PlayerData, UserMedal):
    def __init__(self):
        pass

    def __call__(self, *args, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def _init_singleton_(self):
        UserData._init_singleton_(self)
        GameData._init_singleton_(self)
        UserChip._init_singleton_(self)
        UserItem._init_singleton_(self)
        UserMedal._init_singleton_(self)
        UserVip._init_singleton_(self)
        CheckHallData._init_singleton_(self)
        TableData._init_singleton_(self)
        PlayerData._init_singleton_(self)
        self.incr_chip2 = self.incr_chip
        self.incr_chip2_limit = self.incr_chip_limit


UserProps = UserProps()
