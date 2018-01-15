from twisted.internet import reactor

from tyframework.protocol.client import InternalUDPClientProtocol


class RobotClient():
    @classmethod
    def creatRobotClient(self, gdata, ip, port):
        from tyframework.context import TyContext
        rkey = str(ip) + ':' + str(port)
        if rkey in gdata.robotclientmap:
            robotClient = gdata.robotclientmap[rkey]
            TyContext.ftlog.info('ROBOT Server create client->', ip, port, robotClient)
        else:
            robotClient = InternalUDPClientProtocol(ip, port)
            robotClient.gdata = gdata
            gdata.robotclientmap[rkey] = robotClient
            reactor.listenUDP(0, robotClient, maxPacketSize=65536)
            TyContext.ftlog.info('ROBOT Server create client->', ip, port, robotClient)
        return robotClient
