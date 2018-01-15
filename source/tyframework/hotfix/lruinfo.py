# DATA_TYPE_INT = 3  # 数据类型: 整形数字

from tyframework.context import TyContext

# cachemgr = TyContext.Configure.__get_configure__
# TyContext.ftlog.info('Configure.__get_configure__->hits=', 
#                      cachemgr.hits, 'misses->', cachemgr.misses,
#                      'cachemgr.cache=', len(cachemgr.cache),
# #                      'cachemgr.queue=', len(cachemgr.queue),
# #                      'cachemgr.refcount=', len(cachemgr.refcount),
#                      )
# exec_result['hits'] = cachemgr.hits
# exec_result['misses'] = cachemgr.misses
# exec_result['cache'] = len(cachemgr.cache)
# # exec_result['queue'] = len(cachemgr.queue)
# # exec_result['refcount'] = len(cachemgr.refcount)

'''
# 热更新替换一个TyContext的全局属性
from tyframework.context import TyContext
oldobj = TyContext.Configure

from tyframework._private_.configure.configuredict import ConfigureDict
ConfigureDict._init_ctx_()
object.__setattr__(TyContext, 'Configure', ConfigureDict)
del oldobj

hcount = TyContext.Configure.get_global_item_int('heart.beta.user.count', 6)
exec_result['hcount'] = hcount
exec_result['Configure'] = repr(TyContext.Configure)
'''
