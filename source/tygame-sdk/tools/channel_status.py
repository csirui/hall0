# -*- coding=utf-8 -*-

'''
usage:
http://125.39.218.101:6002/mgt/execfile?f=/home/dingf/tysdk/source/tygame-sdk/tools/channel_status.py&p=chinaMobile,北京,Android_3.501_tuyoo.weakChinaMobile,YDJD.0-hall6.wifikey.dj
'''

from tyframework.context import TyContext
from tysdk.entity.duandai.channels import Channels
from tysdk.entity.duandai.channels import prov2zc_dict as d

p = exec_params
result = exec_result

params = p.split(',')
operator = params[0]
province = d[unicode(params[1])]
clientid = ','.join(params[2:])

#result['clientid'] = clientid
#result['province'] = province
#result['operator'] = operator
price = '6'
result['all'] = Channels._duandai_channels
all = Channels._duandai_channels[operator][price][province]

channels = TyContext.Configure.get_global_item_json('channels', clientid=clientid)
try:
    channels = channels[operator]
except:
    channels = Channels()._get_default_channels(clientid, operator)
result['rule'] = channels

cid_channels = list()
for c in channels:
    cid_channels.append(c['channel'])
final = [a for a in all if a in cid_channels]

result['channels'] = final
