# -*- coding=utf-8 -*-

class DaoConst(object):
    ATT_CHIP = 'chip'
    ATT_COIN = 'coin'
    ATT_DIAMOND = 'diamond'
    ATT_COUPON = 'coupon'
    ATT_TABLE_CHIP = 'tablechip'
    ATT_EXP = 'exp'
    ATT_CHARM = 'charm'
    ATT_NAME = 'name'
    ATT_TRUN_NAME = 'truename'
    ATT_TABLE_ID = 'tableId'
    ATT_SEAT_ID = 'seatId'
    ATT_CLIENT_ID = 'clientId'
    ATT_APP_ID = 'appId'

    HKEY_USERDATA = 'user:'
    HKEY_GAMEDATA = 'gamedata:'
    HKEY_PLAYERDATA = 'playerdata:'
    HKEY_TABLECHIP = 'tablechip:'
    HKEY_TABLEDATA = 'tabledata:'

    FILTER_KEYWORD_FIELDS = set([ATT_NAME, ATT_TRUN_NAME])
    FILTER_MUST_FUNC_FIELDS = set([ATT_CHIP, ATT_DIAMOND, ATT_COIN, ATT_COUPON, ATT_EXP, ATT_CHARM])

    OLD_COUPON_ITEMID = '50'
    VIP_ITEMID = '88'
