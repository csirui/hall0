DATA_TYPE_INT = 3  # 数据类型: 整形数字

from tyframework.context import TyContext

def get_global_item_int(key, defaultVal=0):
    self = TyContext.Configure
    self.__ctx__.ftlog.info('44444444444444444444')
    return self.__get_configure__('configitems:global:' + key, defaultVal, DATA_TYPE_INT)

TyContext.Configure.get_global_item_int = get_global_item_int
