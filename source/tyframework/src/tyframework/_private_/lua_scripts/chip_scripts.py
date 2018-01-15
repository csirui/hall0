# -*- coding=utf-8 -*-
from tyframework._private_.lua_scripts.util_scripts import FUN_INCR_HASH_CHIP_FIELD

###################################################################################################
# 金币变化接口, incr用户的金币数, 当前金币不足时先补为0，然后再操作
# @param 2 delta incr的数量
# @param 3 lowLimit 用户最低金币数，-1表示没有最低限制
# @param 4 highLimit 用户最高金币数，-1表示没有最高限制
# @param 5 mode 0表示如果field+delta<0则不做操作; 1如果field+delta<0则将field值变为0
# @param 6 mkey 需要加减的HASH的主键
# @param 7 filed 需要加减的用户数据的字段名称
# 返回 {实际incr的数量, incr完之后最终的数量, 系统补偿的数量}
###################################################################################################
INCR_CHIP_LUA_SCRIPT = FUN_INCR_HASH_CHIP_FIELD + '''
local delta = ty_tonumber(KEYS[1])
local lowLimit = ty_tonumber(KEYS[2])
local highLimit = ty_tonumber(KEYS[3])
local mode = ty_tonumber(KEYS[4])
local mkey = KEYS[5]
local filed = KEYS[6]
local cur_final_fixed = incr_hash_field(mkey, filed, delta, mode, lowLimit, highLimit)
return {cur_final_fixed[1], cur_final_fixed[2], cur_final_fixed[3]}
'''

###################################################################################################
# 将tablechip的值设置为满足 _min 前提下尽量满足 _max，如果不够则用chip补，如果需要多退则把多余的部分退还到chip
# @param 1 userId 用户ID
# @param 2 gameId 游戏ID
# @param 3 _min 最小取值
# @param 4 _max 最大取值
# @param 5 tablechip所在的HASH键值
# @param 6 tablechip的的HASH字段名称
# 返回{tableDelta, tablechip当前的值, 系统补了多少给tablechip, userchipdelta, userchipfinal, userchipfix}
###################################################################################################
MOVE_CHIP_TO_TABLE_LUA_SCRIPT = FUN_INCR_HASH_CHIP_FIELD + '''
local userId = ty_tonumber(KEYS[1])
local gameId = ty_tonumber(KEYS[2])
local _min = ty_tonumber(KEYS[3])
local _max = ty_tonumber(KEYS[4])
local tkey = KEYS[5]
local tfield = KEYS[6]

-- 修复tchip<0的问题
local tfixed = 0
local tchip = ty_tonumber(redis.call('hget', tkey, tfield))
if tchip < 0 then
    tfixed = -tchip
    tchip = ty_tonumber(redis.call('hincrby', tkey, tfield, tfixed))
end

-- 修复chip<0的问题
local key = 'user:'..userId
local field = 'chip'
local fixed = 0
local chip = ty_tonumber(redis.call('hget', key, field))
if chip < 0 then
    fixed = -chip
    chip = ty_tonumber(redis.call('hincrby', key, field, fixed))
end

-- 解析 -1, -2, -3 flag为对应的 chip 值:
-- -1 chip+tablechip, -2:tablechip, -3:chip, >0: 原样返回
local function parse_flag(_flag_, _chip_, _tablechip_)
    if _flag_ == -1 then
        return _tablechip_ + _chip_
    elseif _flag_ == -2 then
        return _tablechip_
    elseif _flag_ == -3 then
        return _chip_
    else
        return _flag_
    end
end
_min = parse_flag(_min, chip, tchip)
_max = parse_flag(_max, chip, tchip)

local allchip = chip + tchip

--------------------------------------------------------------------------------
-- 检查上、下限，为 target 取 [0, allchip] 之间的值

-- 0. 如果下限 > allchip，令下限=上限=tablechip，确保不做任何真正操作
if _min > allchip then
    _min = tchip
    _max = tchip
end

-- 1. 上限超出 allchip 时，上限取allchip，确保 _max <= allchip
if _max > allchip then
    _max = allchip
end

-- 2. 上限小于下限时，令上限=下限，确保 _min <= _max
if _min > _max then
    _max = _min
end

-- 到此，0 <= _min <= _max <= allchip 成立，取target为最大：
local target = _max

--------------------------------------------------------------------------------

local diff = tchip - target

if diff == 0 then
    return {0, tchip, tfixed, 0, chip, fixed}
end

local chipRet = incr_hash_field(key, field, diff, 0, -1, -1)

-- 多退少补成功
if chipRet[1] == diff then
    -- 多退少补成功，记录tchip日志
    tchip = ty_tonumber(redis.call('hincrby', tkey, tfield, -diff))
else
    diff = 0
end

return {-diff, tchip, tfixed, chipRet[1], chipRet[2], chipRet[3]}
'''
