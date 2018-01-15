#! encoding=utf-8

__author__ = 'yuejianqiang'

payv4_order_map = {

}


class payv4_order:
    def __init__(self, *charge_type):
        self.charge_type = charge_type

    def __call__(self, method):
        method.__charge_type__ = self.charge_type
        return method
