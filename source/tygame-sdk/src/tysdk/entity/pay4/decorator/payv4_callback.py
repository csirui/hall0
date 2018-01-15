#! encoding=utf-8

__author__ = 'yuejianqiang'

payv4_callback_map = {

}


class payv4_callback:
    def __init__(self, *path):
        self.path = path

    def __call__(self, method):
        method.__callback_path__ = self.path
        return method
