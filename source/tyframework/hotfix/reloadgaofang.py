# -*- coding=utf-8 -*-
from tyframework.context import TyContext

TyContext.Configure.reload_cache_keys(['poker:map.gaofangip', 'poker:map.gaofangip.2'])
TyContext.ftlog.info('gaofang reload ! poker:map.gaofangip', 
                     TyContext.Configure._get_configure_('poker:map.gaofangip', None, 2))
TyContext.ftlog.info('gaofang reload ! poker:map.gaofangip.2', 
                     TyContext.Configure._get_configure_('poker:map.gaofangip.2', None, 2))
