# -*- coding=utf-8 -*-
from tyframework._private_.lua_scripts.util_scripts import LUA_FUN_TY_TOBMBER

###################################################################################################
# 加减一个道具的数量
# 参数1 : gameId
# 参数2 : userId
# 参数3 : itemId
# 参数4 : count 加减的数量
# 参数5 : ts 时间戳
# 参数6 : 道具的状态
# 返回:  (rem, istate) 
#        rem 道具的剩余的数量
#        istate 道具的状态
###################################################################################################
INCR_ITEM_LUA_SCRIPT = LUA_FUN_TY_TOBMBER + '''
local gameId = ty_tonumber(KEYS[1])
local userId = ty_tonumber(KEYS[2])
local itemId = ty_tonumber(KEYS[3])
local count = ty_tonumber(KEYS[4])
local ts = ty_tonumber(KEYS[5])
local istate = ty_tonumber(KEYS[6])
local itemKey = 'item:'..gameId..':'..userId
local itemData = redis.call('hget', itemKey, itemId)
local ofid = 0
local ostart = 0
local ocount = 0
local ostate = 0
if itemData then
    ofid, ostart, ocount, ostate = struct.unpack('iiiB', itemData)
    ocount = ty_tonumber(ocount)
end
local rem = ocount + count
if rem == 0 then
    redis.call('hdel', itemKey, itemId)
else
    local newItemData = struct.pack('iiiB', ofid, ts, rem, istate)
    redis.call('hset', itemKey, itemId, newItemData)
end
return {rem, istate}
'''

###################################################################################################
# 更新一个以时间(单位:天)为基础的道具信息(例如: 记牌器)
# 参数1 : gameId
# 参数2 : userId
# 参数3 : itemId
# 参数4 : nowtime 当前的时间戳
# 参数5 : timeZone 当前时间的TIME ZONE
# 返回:  (dcount, ncount, ostate, flg) 
#        dcount 消耗的道具数量
#        ncount 当前剩余的数量
#        ostate 道具的状态
#        flg  1 -- 还有剩余, 2 -- 剩余0, 3 -- 没有该道具信息
###################################################################################################
UPDATE_TIME_ITEM_LUA_SCRIPT = LUA_FUN_TY_TOBMBER + '''
local function get_int_part(x)
    x = ty_tonumber(x)
    if x <= 0 then
       return math.ceil(x);
    end
    if math.ceil(x) == x then
       x = math.ceil(x);
    else
       x = math.ceil(x) - 1;
    end
    return x;
end

local function get_diff_days(big_time, small_time, time_zone_offset)
    big_time = big_time + time_zone_offset
    small_time = small_time + time_zone_offset
    local big_pass_day = get_int_part(big_time/86400)
    local small_pass_day = get_int_part(small_time/86400)
    return big_pass_day - small_pass_day
end

local gameId = get_int_part(KEYS[1])
local userId = get_int_part(KEYS[2])
local itemId = get_int_part(KEYS[3])
local nowtime = get_int_part(KEYS[4])
local timeZoneOffset = get_int_part(KEYS[5])

local itemKey = 'item:'..gameId..':'..userId
local itemData = redis.call('hget', itemKey, itemId)
local dcount = 0
if itemData then
    local ofid, otime, ocount, ostate = struct.unpack('iiiB', itemData)
    ocount = get_int_part(ocount)
    otime = get_int_part(otime)
    dcount = get_diff_days(nowtime, otime, timeZoneOffset)
    local ncount = ocount - dcount
    if dcount < 0 then
        dcount = 0
        ncount = 0
    end
    if ncount >= 0 then
        if ocount ~= ncount then
            itemData = struct.pack('iiiB', ofid, nowtime, ncount, ostate)
            redis.call('hset', itemKey, itemId, itemData)
        end
        return {dcount, ncount, ostate, 1}
    else
        redis.call('hdel', itemKey, itemId)
        return {dcount, ncount, 0, 2}
    end
end
return {dcount, -1, 0, 3}
'''
