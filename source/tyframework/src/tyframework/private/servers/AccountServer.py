# -*- coding=utf-8 -*-
from basic.commonservice import CommonService
from basic.globaldata import GlobalData
from tyframework.protocol.server import AccountUDPSrvProtocol


# Main entry...
def main():
    gdata = GlobalData()
    gs = CommonService()
    gs.startup(gdata, None, AccountUDPSrvProtocol())


# Execute Main ...
if __name__ == '__main__':
    main()
