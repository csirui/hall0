#! encoding=utf-8

__author__ = 'yuejianqiang'

payv4_filter_map = {

}


class payv4_filter:
    def __init__(self, *filter_type):
        self.filter_type = filter_type

    def __call__(self, method):
        method.__filter_type__ = self.filter_type
        return method
