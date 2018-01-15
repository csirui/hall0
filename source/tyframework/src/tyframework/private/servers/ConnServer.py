# -*- coding=utf-8 -*-

from basic.commonservice import CommonService
from basic.globaldata import GlobalData

from tyframework.protocol.server import ConnTCPSrvProtocol
from tyframework.protocol.server import ConnTCPSrvZipProtocol
from tyframework.protocol.server import ConnUDPSrvProtocol


# Main entry...
def main():
    gdata = GlobalData()
    gs = CommonService()
    gs.startup(gdata, ConnTCPSrvProtocol, ConnUDPSrvProtocol(), ConnTCPSrvZipProtocol)


# Execute Main ...
if __name__ == '__main__':
    main()
