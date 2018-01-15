# -*- coding: utf-8 -*-

class TimeoutException(Exception):
    pass


class MySqlSwapException(Exception):
    def __init__(self, uid=0):
        self.userid = uid


class FreetimeException(Exception):
    def __init__(self, errorCode, message):
        self.__errorCode = errorCode
        self.__message = message

    @property
    def errorCode(self):
        return self.__errorCode

    @property
    def message(self):
        return self.__message


class TableChipException(FreetimeException):
    pass


class GlobalLockerException(FreetimeException):
    pass
