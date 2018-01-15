__author__ = 'tuyou'

snsv4_login_map = {

}


class snsv4_login(object):
    def __init__(self, *sdk):
        self.sdks = sdk

    def __call__(self, method):
        method.__sdks__ = self.sdks
        return method
