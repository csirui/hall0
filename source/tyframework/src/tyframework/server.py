# -*- coding=utf-8 -*-

def main():
    from tyframework._private_.util.initreactor import initepollreactor
    initepollreactor()

    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')

    from tyframework.context import TyContext
    TyContext._init_ctx_()

    procid = sys.argv[1]
    TyContext.ftlog.info('service __main__', procid)
    TyContext.TYGlobal.init_static_data()
    TyContext.TYGlobal.dump_static_info()

    ptype = TyContext.TYGlobal.run_process_type()
    pid = TyContext.TYGlobal.run_process_id()

    pyclass = None
    if ptype.find('robo') >= 0:
        if pid == 0:
            pyclass = 'robots.RobotServerNew'
        else:
            pyclass = 'robots2.RobotServer2New'
    elif ptype.find('http') >= 0:
        pyclass = 'private.servers.HttpServer'
    elif ptype.find('conn') >= 0:
        pyclass = 'private.servers.ConnServer'
    elif ptype.find('enti') >= 0:
        pyclass = 'private.servers.EntityServer'
    elif ptype.find('acco') >= 0:
        pyclass = 'private.servers.AccountServer'
    elif ptype.find('quic') >= 0:
        pyclass = 'private.servers.QuickStartServer'
    elif ptype.find('hear') >= 0:
        pyclass = 'private.servers.HeartBeatServer'
    elif ptype.find('game') >= 0:
        pyclass = 'private.servers.GameServer'

    srvmain = None
    exec 'from %s import main as srvmain' % (pyclass)
    TyContext.ftlog.info('srvmain start')
    srvmain()


if __name__ == '__main__':
    main()
