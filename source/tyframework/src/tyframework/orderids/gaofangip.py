# -*- coding=utf-8 -*-
import random


def getGaoFangIp(clientId, ip, port):
    try:
        from tyframework.context import TyContext
        _, cver, _ = TyContext.strutil.parse_client_id(clientId)
        gaofangConfs = TyContext.Configure._get_configure_('poker:map.gaofangip', None, 2)
        TyContext.ftlog.debug('convert ip to gaofangConfs->', cver, gaofangConfs)
        if gaofangConfs:
            policy = gaofangConfs['policy']
            if policy == 'tuyou':
                ip = gaofangConfs[policy].get(ip, ip)

            elif policy == 'aligaofang':
                original = gaofangConfs['original']
                group = original[ip + ':' + str(port)]
                groupIps = gaofangConfs[policy][group]
                if groupIps:
                    ip = random.choice(groupIps)
            if cver >= 3.78:
                TyContext.ftlog.debug('convert ip to namesapce->', ip)
                ip = gaofangConfs['namespace'][ip]
                TyContext.ftlog.debug('convert ip to namesapce->', ip)
    except:
        TyContext.ftlog.error()
    return ip, port


def getGaoFangIp2(userId, clientId):
    from tyframework.context import TyContext
    ip, port = '', 0
    # TyContext.ftlog.info('getGaoFangIp2->', userId, clientId)
    try:
        gaofangConfs = TyContext.Configure._get_configure_('poker:map.gaofangip.2', {}, 2)
        policy = gaofangConfs.get('policy')
        if policy == 'defence2':
            _, intClientId = TyContext.BiUtils.getClientIdNum(clientId, None, 0, userId, check_msg=0)
            clientIds = gaofangConfs['clientIds']
            areaId = clientIds.get(intClientId)
            if not areaId:
                areaId = clientIds.get(str(intClientId))
                if not areaId:
                    areaId = clientIds.get('default')
                    if not areaId:
                        areaId = gaofangConfs['areas'].keys()[0]
                    TyContext.ftlog.warn('ERROR, getGaoFangIp2 not found area id of ',
                                         intClientId, clientId, 'use default !')
                clientIds[intClientId] = areaId
            entrys = gaofangConfs['areas'][areaId]
            ipPorts = random.choice(entrys)  # 切换不同的端口接入
            ipPort = ipPorts[userId % len(ipPorts)]  # 使用相对固定的IP地址接入
            ip, port = ipPort[0], ipPort[1]

            # TyContext.ftlog.info('getGaoFangIp2->', ip, port, userId, clientId)
    except:
        TyContext.ftlog.exception()
    return ip, port
