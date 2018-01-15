# -*- coding=utf-8 -*-
'''
Created on 2014年5月6日

@author: zjgzzz@126.com
'''

from tyframework.context import TyContext
from tysdk.entity.upgradev3.versionmanagerv3 import Version, GameIncUpdate, GameIncUpdateConfiger, GameFullUpdate, \
    GameDiffUpdate


class HttpUpgradev3(object):
    JSONPATHS = None

    @classmethod
    def getJsonPaths(cls):
        if not cls.JSONPATHS:
            cls.JSONPATHS = {
                '/open/v3/upgrade/getUpdateInfo': cls.doGetUpdateInfo,
                '/test/open/v3/upgrade/uploadPhoto': cls.doGetUpdateInfoTest,

                '/open/v3/upgrade/getVersionInfos': cls.doGetVersionInfos,
                '/open/v3/upgrade/addVersion': cls.doAddVersion,
                '/open/v3/upgrade/modVersion': cls.doModVersion,
                '/open/v3/upgrade/delVersion': cls.doDelVersion,

                '/open/v3/upgrade/addClientId': cls.doAddClientId,
                '/open/v3/upgrade/getClientIdVersions': cls.doGetClientIdVersions,
                '/open/v3/upgrade/exportClientIdVersions': cls.doExportClientIdVersions,
                '/open/v3/upgrade/addClientIdVersion': cls.doAddClientIdVersion,
                '/open/v3/upgrade/delClientIdVersion': cls.doDelClientIdVersion,

                '/open/v3/getUpdateInfo': cls.doGetUpdataInfo,
                '/open/v3/getUpdateInfo2': cls.doGetUpdataInfo2,
                '/open/v3/getupdateinfo': cls.doGetUpdataInfo,
                '/open/v3/reload': cls.doReload,
                '/open/v3/nicai': cls.doNicai,
            }
        return cls.JSONPATHS

    @classmethod
    def doGetUpdateInfo(cls, rpath):
        pass

    @classmethod
    def doGetUpdateInfoTest(cls, rpath):
        pass

    @classmethod
    def doGetVersionInfos(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        gameId = TyContext.RunHttp.getRequestParamInt('gameId')
        vermnr = GameIncUpdateConfiger.instance().find_vers_mnr(gameId)
        if vermnr == None:
            mo.setError('info', 'error gameId')
        else:
            mo.setResult('versions', vermnr.generateToManager())
        mo = mo.packJson()
        return mo

    @classmethod
    def doAddVersion(cls, rpath):
        gameId = TyContext.RunHttp.getRequestParamInt('gameId')
        md5 = TyContext.RunHttp.getRequestParam('md5')
        size = TyContext.RunHttp.getRequestParam('size')
        path = TyContext.RunHttp.getRequestParam('path')
        des = TyContext.RunHttp.getRequestParam('des')
        force = TyContext.RunHttp.getRequestParam('force')

        mo = TyContext.Cls_MsgPack()
        if not (md5 and size and path and des and force):
            mo.setResult('code', 1)
            mo.setResult('info', 'args error')
            return mo

        vermnr = GameIncUpdateConfiger.instance().find_vers_mnr(gameId)
        if vermnr == None:
            mo.setResult('code', 2)
            mo.setResult('info', 'error gameId')
            return mo

        id = vermnr.generateId()
        ver = Version(id, md5, size, path, des, force)

        if vermnr.addVersion(ver):
            mo.setResult('version', ver.generateToManager())
            vermnr.save()
        else:
            mo.setResult('code', 3)
            mo.setResult('info', 'add error')
        return mo

    @classmethod
    def doModVersion(cls, rpath):
        gameId = TyContext.RunHttp.getRequestParamInt('gameId')
        id = TyContext.RunHttp.getRequestParamInt('id')
        mo = TyContext.Cls_MsgPack()

        vermnr = GameIncUpdateConfiger.instance().find_vers_mnr(gameId)
        if vermnr == None:
            mo.setResult('code', 1)
            mo.setResult('info', 'error gameId')
            return mo

        ver = None
        if id:
            ver = vermnr.findVersion(id)

        if ver:
            md5 = TyContext.RunHttp.getRequestParam('md5')
            if md5:
                ver.setMd5(md5)

            size = TyContext.RunHttp.getRequestParam('size')
            if size:
                ver.setSize(size)

            path = TyContext.RunHttp.getRequestParam('path')
            if path:
                ver.setPath(path)

            des = TyContext.RunHttp.getRequestParam('des')
            if des:
                ver.setDes(des)

            force = TyContext.RunHttp.getRequestParam('force')
            if force:
                ver.setForce(force)

            mo.setResult('version', ver.generateToManager())
            vermnr.save()

        else:
            mo.setResult('code', 2)
            mo.setResult('info', 'id error')

        return mo

    @classmethod
    def doDelVersion(cls, rpath):
        gameId = TyContext.RunHttp.getRequestParamInt('gameId')
        id = TyContext.RunHttp.getRequestParamInt('id')
        mo = TyContext.Cls_MsgPack()
        vermnr = GameIncUpdateConfiger.instance().find_vers_mnr(gameId)
        clivermnr = GameIncUpdateConfiger.instance().find_clivers_mnr(gameId)
        if vermnr == None or clivermnr == None:
            mo.setResult('code', 1)
            mo.setResult('info', 'error gameId')
            return mo
        if id:
            clivermnr.remVersion(id)
            vermnr.remVersin(id)
            clivermnr.save()
            vermnr.save()
            mo.setResult('success', 1)
        else:
            mo.setResult('code', 2)
            mo.setResult('info', 'args error')

        return mo

    @classmethod
    def doAddClientId(cls, rpath):
        gameId = TyContext.RunHttp.getRequestParamInt('gameId')
        clientid = TyContext.RunHttp.getRequestParam('clientId')

        mo = TyContext.Cls_MsgPack()
        clivermnr = GameIncUpdateConfiger.instance().find_clivers_mnr(gameId)
        if clivermnr == None:
            mo.setResult('code', 1)
            mo.setResult('info', 'error gameId')
            return mo
        if clientid:
            if clivermnr.addClientId(clientid):
                cliver = clivermnr.findClientVersion(clientid)
                mo.setResult('clientVersions', cliver.generateToManager())
                clivermnr.save()
            else:
                mo.setResult('code', 2)
                mo.setResult('info', 'clientid exist')
        else:
            mo.setResult('code', 3)
            mo.setResult('info', 'args error')

        return mo

    @classmethod
    def doDelClientIdVersion(cls, rpath):
        gameId = TyContext.RunHttp.getRequestParamInt('gameId')
        clientid = TyContext.RunHttp.getRequestParam('clientId')
        versionid = TyContext.RunHttp.getRequestParamInt('versionId')
        mo = TyContext.Cls_MsgPack()
        clivermnr = GameIncUpdateConfiger.instance().find_clivers_mnr(gameId)
        if clivermnr == None:
            mo.setResult('code', 1)
            mo.setResult('info', 'error gameId')
            return mo
        if clientid and versionid:
            clv = clivermnr.findClientVersion(clientid)
            if clv:
                clv.remVersionById(versionid)
                mo.setResult('clientVersions', clv.generateToManager())
                clivermnr.save()
                return mo

        mo.setResult('code', 2)
        mo.setResult('info', 'args error')
        return mo

    @classmethod
    def doAddClientIdVersion(cls, rpath):
        gameId = TyContext.RunHttp.getRequestParamInt('gameId')
        clientid = TyContext.RunHttp.getRequestParam('clientId')
        versionid = TyContext.RunHttp.getRequestParamInt('versionId')
        mo = TyContext.Cls_MsgPack()
        vermnr = GameIncUpdateConfiger.instance().find_vers_mnr(gameId)
        clivermnr = GameIncUpdateConfiger.instance().find_clivers_mnr(gameId)
        if vermnr == None or clivermnr == None:
            mo.setResult('code', 1)
            mo.setResult('info', 'error gameId')
            return mo

        if clientid and versionid:
            clv = clivermnr.findClientVersion(clientid)
            vsn = vermnr.findVersion(versionid)
            if clv and vsn:
                clv.addVersion(vsn)
                mo.setResult('clientVersions', clv.generateToManager())
                clivermnr.save()
                return mo

        mo.setResult('code', 2)
        mo.setResult('info', 'args error')
        return mo

    @classmethod
    def doGetClientIdVersions(cls, rpath):
        gameId = TyContext.RunHttp.getRequestParamInt('gameId')
        mo = TyContext.Cls_MsgPack()
        clivermnr = GameIncUpdateConfiger.instance().find_clivers_mnr(gameId)
        if clivermnr == None:
            mo.setResult('code', 1)
            mo.setResult('info', 'error gameId')
            return mo

        mo.setResult('allClientVersions', clivermnr.generateToManager())
        return mo

    @classmethod
    def doExportClientIdVersions(cls, rpath):
        gameId = TyContext.RunHttp.getRequestParamInt('gameId')
        mo = TyContext.Cls_MsgPack()
        clivermnr = GameIncUpdateConfiger.instance().find_clivers_mnr(gameId)
        if clivermnr == None:
            mo.setResult('code', 1)
            mo.setResult('info', 'error gameId')
            return mo

        clivermnr.export()
        mo.setResult('success', 1)
        return mo

    @classmethod
    def doGetUpdataInfo(cls, rpath):
        gameid = TyContext.RunHttp.getRequestParamInt('gameId')
        clientid = TyContext.RunHttp.getRequestParam('clientId')
        upversion = TyContext.RunHttp.getRequestParamInt('updateVersion')

        mo = TyContext.Cls_MsgPack()
        mo.setCmd('getUpdateInfo')

        if gameid == 0 or clientid == None:
            mo.setError(2, '参数错误')
            return mo

        TyContext.ftlog.debug('doGetUpdataInfo', gameid, clientid, upversion)
        verinfo = GameIncUpdate.instance().getNeedUpdateVersion(gameid, clientid, upversion)
        if verinfo:
            mo.setResult('gameId', gameid)
            mo.setResult('clientId', clientid)
            mo.setResult('updateVersion', verinfo._id)
            if verinfo._force == '1':
                mo.setResult('updateType', 'force')
            else:
                mo.setResult('updateType', 'optional')
            mo.setResult('updateSize', verinfo._size)
            mo.setResult('updateUrl', verinfo._path)
            mo.setResult('updateDes', verinfo._des)
            mo.setResult('jsMD5', verinfo._md5)
        else:
            mo.setError(1, '无可用更新')
        return mo

    @classmethod
    def __getUpdateWeight(cls, updateType, updateStyle):
        '''
        0 - optional
        1 - force
        '''
        weights = {}
        weights['inc'] = {}
        weights['inc']['0'] = 1
        weights['inc']['1'] = 10
        weights['apk'] = {}
        weights['apk']['0'] = 5
        weights['apk']['1'] = 14
        weights['diff'] = {}
        weights['diff']['0'] = 3
        weights['diff']['1'] = 12

        if updateType not in weights:
            return 0

        if updateStyle not in weights[updateType]:
            return 0

        return weights[updateType][updateStyle]

    @classmethod
    def doGetUpdataInfo2(cls, rpath):
        gameId = TyContext.RunHttp.getRequestParamInt('gameId')
        clientId = TyContext.RunHttp.getRequestParam('clientId')
        updateVersion = TyContext.RunHttp.getRequestParamInt('updateVersion')
        nicaiCode = TyContext.RunHttp.getRequestParam('nicaiCode', '0')
        alphaVersion = TyContext.RunHttp.getRequestParam('alphaVersion', 0)

        TyContext.ftlog.debug('doGetUpdataInfo2', gameId, clientId, updateVersion, nicaiCode, alphaVersion)

        mo = TyContext.Cls_MsgPack()
        mo.setCmd('getUpdateInfo2')

        if gameId == 0 or clientId == None:
            mo.setError(2, '参数错误')
            return mo

        nicaiCodeEncoded = TyContext.strutil.tydes_encode(nicaiCode)
        mo.setResult('nicaiCode', nicaiCodeEncoded)
        mo.setResult('gameId', gameId)
        mo.setResult('clientId', clientId)

        # 获取增量更新信息
        incUpdateInfo = GameIncUpdate.instance().getNeedUpdateVersion(gameId, clientId, updateVersion)
        incUpdateWeight = 0
        if incUpdateInfo:
            TyContext.ftlog.debug('incUpdateInfo', incUpdateInfo)
            incUpdateWeight = cls.__getUpdateWeight('inc', incUpdateInfo._force)

        # 获取全量更新信息
        fullUpdateWeight = 0
        fullUpdateInfoArr = GameFullUpdate.getFullUpdateInfo(gameId, clientId)
        fullUpdateInfo = {}
        if fullUpdateInfoArr != None and isinstance(fullUpdateInfoArr, list):
            # alphaVersion表示要升级的alpha包的版本号
            alphaKey = 'alphaVersion'
            # 先选择合适的alpha更新版本
            for fu in fullUpdateInfoArr:
                if alphaKey in fu:
                    TyContext.ftlog.debug('alphaVersion', fu[alphaKey])
                    if (fu[alphaKey] != 0) and (fu[alphaKey] != int(alphaVersion)):
                        fullUpdateInfo = fu
                else:
                    fullUpdateInfo = fu

            TyContext.ftlog.debug('fullUpdateInfo', fullUpdateInfo)
            if 'force' in fullUpdateInfo:
                fullUpdateWeight = cls.__getUpdateWeight('apk', fullUpdateInfo['force'])

        # 获取差分更新信息
        diffUpdateInfo = {}
        diffUpdateWeight = 0
        diffUpdateInfoArr = GameDiffUpdate.getDiffUpdateInfo(gameId, clientId)
        if diffUpdateInfoArr != None and isinstance(diffUpdateInfoArr, list):
            alphaKey = 'alphaVersion'
            # 先选择合适的alpha更新版本
            for du in diffUpdateInfoArr:
                if alphaKey in du:
                    TyContext.ftlog.debug('alphaVersion', fu[alphaKey])
                    if (du[alphaKey] != 0) and (du[alphaKey] > int(alphaVersion)):
                        diffUpdateInfo = du
                else:
                    diffUpdateInfo = du

            TyContext.ftlog.debug('diffUpdateInfo', diffUpdateInfo)
            if 'force' in diffUpdateInfo:
                diffUpdateWeight = cls.__getUpdateWeight('diff', diffUpdateInfo['force'])

        # 根据权重计算当前发送哪个更新
        TyContext.ftlog.debug('incUpdateWeight:', incUpdateWeight, ' and fullUpdateWeight:', fullUpdateWeight,
                              ' and diffUpdateWeight:', diffUpdateWeight)

        if ((incUpdateWeight > fullUpdateWeight) and (incUpdateWeight > diffUpdateWeight)):
            resUpdate = {}
            resUpdate['updateVersion'] = incUpdateInfo._id
            if incUpdateInfo._force == '1':
                resUpdate['updateType'] = 'force'
            else:
                resUpdate['updateType'] = 'optional'
            resUpdate['updateSize'] = incUpdateInfo._size
            resUpdate['updateUrl'] = incUpdateInfo._path
            resUpdate['updateDes'] = incUpdateInfo._des
            resUpdate['MD5'] = incUpdateInfo._md5
            resUpdate['fileType'] = 'zip'
            resUpdate['autoDownload'] = incUpdateInfo._autoDownloadCondition
            mo.setResult('resUpdate', resUpdate)
        elif ((fullUpdateWeight > incUpdateWeight) and (fullUpdateWeight > diffUpdateWeight)):
            apkUpdate = {}
            if fullUpdateInfo['force'] == '1':
                apkUpdate['updateType'] = 'force'
            else:
                apkUpdate['updateType'] = 'optional'
            apkUpdate['updateSize'] = fullUpdateInfo['size']
            apkUpdate['updateUrl'] = fullUpdateInfo['path']
            apkUpdate['updateDes'] = fullUpdateInfo['des']
            apkUpdate['MD5'] = fullUpdateInfo['md5']
            apkUpdate['fileType'] = 'apk'
            apkUpdate['autoDownload'] = fullUpdateInfo['autoDownloadCondition']
            if 'updateAt' in fullUpdateInfo:
                apkUpdate['updateAt'] = fullUpdateInfo['updateAt']
            mo.setResult('apkUpdate', apkUpdate)
        elif ((diffUpdateWeight > incUpdateWeight) and (diffUpdateWeight > fullUpdateWeight)):
            diffUpdate = {}
            if diffUpdateInfo['force'] == '1':
                diffUpdate['updateType'] = 'force'
            else:
                diffUpdate['updateType'] = 'optional'
            diffUpdate['updateSize'] = diffUpdateInfo['size']
            diffUpdate['updateUrl'] = diffUpdateInfo['path']
            diffUpdate['updateDes'] = diffUpdateInfo['des']
            diffUpdate['MD5'] = diffUpdateInfo['md5']
            diffUpdate['fileType'] = 'diff'
            diffUpdate['autoDownload'] = diffUpdateInfo['autoDownloadCondition']
            if 'updateAt' in diffUpdateInfo:
                diffUpdate['updateAt'] = diffUpdateInfo['updateAt']
            mo.setResult('diffUpdate', diffUpdate)

        return mo

    @classmethod
    def doReload(cls, rpath):

        GameIncUpdate.instance().load()

        mo = TyContext.Cls_MsgPack()
        mo.setCmd('reload')

        return mo

    @classmethod
    def doNicai(cls, rpath):
        code = TyContext.RunHttp.getRequestParam('code', '0')
        rcode = TyContext.strutil.tydes_encode(code)
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('nicai')
        mo.setResult('code', rcode)
        return mo
