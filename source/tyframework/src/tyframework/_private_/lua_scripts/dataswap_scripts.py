# -*- coding=utf-8 -*-

###################################################################################################
# 检查用户数据是否存在, 并更新aliveTime
# @param 1 userId 用户的ID
# @param 2 aliveTime 当前的时间戳字符串
# @param 3 datajstr JSON格式的用户数据
# 返回 如果存在那么更新aliveTime,返回1, 否则返回0
###################################################################################################
CHECK_USER_DATA_LUA_SCRIPT = '''
local userId = KEYS[1]
local aliveTime = KEYS[2]
local userkey = "user:" .. userId
local createTime = redis.call("hget", userkey, "createTime")
if (createTime == nil or createTime == false) then
    return 0
end
if (string.len(""..createTime) < 20) then -- 2015-04-15 00:00:00.000
    return 0
end
redis.call("hset", userkey, "aliveTime", aliveTime)
return 1
'''

###################################################################################################
# 冷数据转热数据的脚本
# @param 1 userId 用户的ID
# @param 2 aliveTime 当前的时间戳字符串
# @param 3 datajstr JSON格式的用户数据
# 返回 1 执行成功, 其他值失败 以及chip, diamond, coin, coupon
###################################################################################################
DATA_SWAP_LUA_SCRIPT = '''
local userId = KEYS[1]
local aliveTime = KEYS[2]
local datajstr = KEYS[3]

local base64decode = function(data)
    local b="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    data = string.gsub(data, "[^"..b.."=]", "")
    return (data:gsub(".", function(x)
        if (x == "=") then return "" end
        local r,f="",(b:find(x)-1)
        for i=6,1,-1 do r=r..(f%2^i-f%2^(i-1)>0 and "1" or "0") end
        return r;
    end):gsub("%d%d%d?%d?%d?%d?%d?%d?", function(x)
        if (#x ~= 8) then return "" end
        local c=0
        for i=1,8 do c=c+(x:sub(i,i)=="1" and 2^(8-i) or 0) end
        return string.char(c)
    end))
end

local decodedatas1 = function(line)
    local step = (#line - 2) / 2
    for x = 1, step, 1 do
        local i = x * 2 + 2
        line[i] = base64decode(line[i])
    end
end

local decodedatas2 = function(line)
    local step = (#line - 2)
    for x = 1, step, 1 do
        local i = x + 2
        line[i] = base64decode(line[i])
    end
end

local datas = cjson.decode(datajstr)
local rkey = nil
local rdata = nil
local rcmds = {"lpush", "sadd", "zadd", "hmset", "set"}
for rkey, rdata in pairs(datas) do
    local isb64 = rdata[1]
    local rcmdtype = rdata[2] -- 1 lpush 2 sadd 3 zadd 4 hmset 5 string 
    if (isb64 == 1) then
        if rcmdtype == 2 or rcmdtype == 1 or rcmdtype == 5 then
            decodedatas2(rdata)
        elseif (rcmdtype == 4 or rcmdtype == 3) then
            decodedatas1(rdata)
        else
            return {-1, 0, 0, 0, 0}
        end
    end
    table.remove(rdata, 1)
    table.remove(rdata, 1)
    if (#rdata > 0 ) then
        if (string.find(rkey, '%%s')) then
            rkey = string.format(rkey, userId)
        else
            rkey = rkey .. userId
        end
        redis.call(rcmds[rcmdtype], rkey, unpack(rdata))
    end
end
redis.call("hset", "user:" .. userId, "aliveTime", aliveTime)
local chips = redis.call("hmget", "user:" .. userId, "chip", "diamond", "coin", "coupon")
return {1, chips[1], chips[2], chips[3], chips[4]}
'''
