# -*- coding=utf-8 -*-

###################################################################################################
# 将一个值转换为数字,如果无法转换,返回0
###################################################################################################
LUA_FUN_TY_TOBMBER = '''
local function ty_tonumber(val)
    val = tonumber(val)
    if val == nil then
        return 0
    end
    return val
end
'''

###################################################################################################
# function incr_hash_field(key, field, delta, mode, lowLimit, highLimit)
#    将hash为key的field的值INCR delta个数量，如果field当前值为负数则由系统修复到0然后再执行incr操作
#    @param key 要incr的key
#    @param field 要incr的field
#    @param delta 要incr的数量
#    @param mode 0表示如果field+delta<0则不做操作; 1如果field+delta<0则将field值变为0
#    @param lowLimit 用户最低金币数，-1表示没有最低限制
#    @param highLimit 用户最高金币数，-1表示没有最高限制
#    返回{实际incr数量, incr后的最终数量, 系统修复的数量}

###################################################################################################
FUN_INCR_HASH_CHIP_FIELD = LUA_FUN_TY_TOBMBER + '''
local function incr_hash_field(key, field, delta, mode, lowLimit, highLimit)
    local cur = ty_tonumber(redis.call('hget', key, field))
    local final = cur
    local fixed = 0
    if cur < 0 then
        fixed = -cur
        final = ty_tonumber(redis.call('hincrby', key, field, fixed))
        cur = final
    end
    if lowLimit ~= -1 and cur < lowLimit then
        return {0, final, fixed}
    end
    if highLimit ~= -1 and cur > highLimit then
        return {0, final, fixed}
    end
    if delta >= 0 or cur + delta >= 0 then
        final = ty_tonumber(redis.call('hincrby', key, field, delta))
        return {delta, final, fixed}
    end
    if mode == 0 or cur == 0 then
        return {0, cur, fixed}
    end
    final = ty_tonumber(redis.call('hincrby', key, field, -cur))
    return {-cur, final, fixed}
end
'''
