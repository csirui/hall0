# -*- coding=utf-8 -*-
'''
Created on 2014年5月6日

@author: zjgzzz@126.com

全量更新的配置ID clients.full.upgrade.map
增量更新的配置ID clients.inc.upgrade.map
差分更新的配置ID clients.diff.upgrade.map

'''
import json
import os
import time

from tyframework.context import TyContext


class Version(object):
    def __init__(self, id, md5, size, path, des, force, autoDownloadCondition):
        self._id = id
        self._md5 = md5
        self._size = size
        self._path = path
        self._des = des
        self._force = force
        self._autoDownloadCondition = autoDownloadCondition

    def generateToSave(self):
        return {'id': self._id,
                'md5': self._md5,
                'size': self._size,
                'path': self._path,
                'force': self._force,
                'des': self._des,
                'autoDownloadCondition': self._autoDownloadCondition
                }

    def generateToManager(self):
        return self.generateToSave()

    @classmethod
    def generateFrom(cls, data):
        assert (isinstance(data, dict))
        if 'id' not in data: return None
        if 'md5' not in data: return None
        if 'path' not in data: return None
        if 'size' not in data: return None
        if 'force' not in data: return None
        if 'des' not in data: return None

        return cls(data['id'], data['md5'], data['size'], data['path'], data['des'], data['force'],
                   4 if "autoDownloadCondition" not in data else data["autoDownloadCondition"])

    def setMd5(self, md5):
        self._md5 = md5

    def setSize(self, size):
        self._size = size

    def setPath(self, path):
        self._path = path

    def setDes(self, des):
        self._des = des

    def setForce(self, force):
        self._force = force

    def setAutoDownloadCondition(self, autoDownloadCondition):
        self._autoDownloadCondition = autoDownloadCondition


class VersionManager(object):
    def __init__(self, gameid_, file_):
        self.__idtoversion = {}
        self.__recordid = 1
        self._file = file_
        self._gameid = gameid_

    def generateId(self):
        self.__recordid += 1
        return self.__recordid

    def generateToSave(self):
        data = []
        for value in self.__idtoversion.values():
            data.append(value.generateToSave())
        return data

    def generateToManager(self):
        return self.generateToSave()

    def generateFrom(self, data):
        assert (isinstance(data, (list, tuple)))
        self.__idtoversion = {}
        for info in data:
            ver = Version.generateFrom(info)
            if ver:
                self.__idtoversion[ver._id] = ver
                if ver._id > self.__recordid:
                    self.__recordid = ver._id
            else:
                return False
        return True

    def addVersion(self, version):
        assert (isinstance(version, Version))
        if version._id not in self.__idtoversion:
            self.__idtoversion[version._id] = version
            return True
        return False

    def findVersion(self, id):
        if id in self.__idtoversion:
            return self.__idtoversion[id]
        return None

    def remVersin(self, id):
        if id in self.__idtoversion:
            del self.__idtoversion[id]

    def save(self):
        save_data = self.generateToSave()
        return SaveLoadHelper.save(self._file, json.dumps(save_data))

    def load(self):
        load_data = SaveLoadHelper.load(self._file)
        try:
            load_data = json.loads(load_data)
        except:
            load_data = []
        return self.generateFrom(load_data)


class ClientVersions(object):
    def __init__(self, clientid):
        assert (clientid)
        self.__client = clientid
        self.__versions = []

    @property
    def clientId(self):
        return self.__client

    def generateToManager(self):
        versions = []
        for ver in self.__versions:
            versions.append(ver.generateToManager())
        return versions

    def generateToSave(self):
        versions = []
        for ver in self.__versions:
            versions.append(ver._id)
        return versions

    def addVersion(self, version):
        assert (isinstance(version, Version))
        for oldver in self.__versions:
            if oldver._id == version._id:
                return False
        self.__versions.append(version)

    def remVersionById(self, id):
        for index in xrange(len(self.__versions)):
            if self.__versions[index]._id == id:
                del self.versions[index]

    def remVersionByUpver(self, updateversion):
        assert (updateversion > 0)
        if updateversion <= len(self.__versions):
            del self.__versions[updateversion - 1]

    def makeVersionChain(self, updateversion):
        if updateversion >= len(self.__versions):
            return []
        verchain = []
        for index in xrange(updateversion - 1, len(self.__versions)):
            verchain.append([index, self.__versions[index]._force])
        return verchain

    def makeNeedUpdateVersion(self, updateversion):
        TyContext.ftlog.debug('makeNeedUpdateVersion', updateversion, len(self.__versions), self.__versions)

        if len(self.__versions) <= 0 or updateversion >= self.__versions[-1]._id:
            return None

        force = '0'
        for i in range(len(self.__versions) - 1, -1, -1):
            version = self.__versions[i]
            if version._id <= updateversion:
                break
            if version._force == '1':
                force = '1'
                break
        version = self.__versions[-1]
        return Version(version._id, version._md5, version._size, version._path,
                       version._des, force, version._autoDownloadCondition)


class CliToVersManager(object):
    def __init__(self, file_, export_, gameid_):
        self.__clitovers = {}
        self._file = file_
        self._export = export_
        self._gameid = gameid_

    def generateToSave(self):
        out_dic = {}
        for key, value in self.__clitovers.items():
            out_dic[key] = value.generateToSave()
        return out_dic

    def generateToManager(self):
        out_dic = {}
        for key, value in self.__clitovers.items():
            out_dic[key] = value.generateToManager()
        return out_dic

    def generateFrom(self, data):
        assert (isinstance(data, dict))
        self.__clitovers = {}
        for key, value in data.items():
            cliv = ClientVersions(key)
            self.__clitovers[key] = cliv
            for id in value:
                vermnr = GameIncUpdateConfiger.instance().find_vers_mnr(self._gameid)
                if vermnr:
                    ver = vermnr.findVersion(id)
                    if ver:
                        cliv.addVersion(ver)

    def addClientId(self, clientid):
        clivers = ClientVersions(clientid)
        return self.addClientVersion(clivers)

    def addClientVersion(self, clientversions):
        assert (isinstance(clientversions, ClientVersions))
        clientid = clientversions.clientId
        if clientid in self.__clitovers:
            return False
        else:
            self.__clitovers[clientid] = clientversions
            return True

    def findClientVersion(self, clientid):
        if clientid in self.__clitovers:
            return self.__clitovers[clientid]

    def remClientVersion(self, clientid):
        if clientid in self.__clitovers:
            del self.__clitovers[clientid]

    def remVersion(self, id):
        for key, value in self.__clitovers.items():
            value.remVersionById(id)

    def load(self):
        try:
            load_data = json.loads(SaveLoadHelper.load(self._file))
        except:
            load_data = {}

        return self.generateFrom(load_data)

    def save(self):
        save_data = self.generateToSave()
        SaveLoadHelper.save(self._file, json.dumps(save_data))

    def export(self):
        if os.path.isfile(self._export):
            curtime = time.strftime('%y%m%d%H%M%S')
            os.rename(self._export, self._export + '.' + curtime + '.bak')

        save_data = self.generateToManager()
        SaveLoadHelper.save(self._export, json.dumps(save_data))


# 提供配置的代码
class GameIncUpdateConfiger(object):
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance == None:
            cls._instance = cls()
            cls._instance.initialize()
        return cls._instance

    def __init__(self):
        self._gidtocliver = {}
        self._gidtovers = {}

    def initialize(self):
        # 初始化版本管理
        self._gidtovers = {
            6: VersionManager(6, '../datas/versions6.json'),
            #                              6: VersionManager(6, 'versions.json'),
        }
        for k, v in self._gidtovers.items():
            v.load()

        # 初始化clientId对应版本
        self._gidtocliver = {
            6: CliToVersManager('../datas/clientversions6.json',
                                '../datas/export6.json', 6),
        }
        for k, v in self._gidtocliver.items():
            v.load()

    def find_vers_mnr(self, gameid):
        if gameid in self._gidtovers:
            return self._gidtovers[gameid]
        return None

    def find_clivers_mnr(self, gameid):
        if gameid in self._gidtocliver:
            return self._gidtocliver[gameid]
        return None

    # 提供服务的代码


class CliToVersService(object):
    def __init__(self, gameId):
        # self.__clitovers = {}
        self.__gameId = gameId

    '''
    def load(self):
        try:
            load_data = TyContext.Configure.get_game_item_json(self.__gameId, 'clients.inc.upgrade.map', {})
            TyContext.ftlog.info('CliToVersService->load gameId=', self.__gameId, load_data)
            self.__clitovers = self._generateFrom(load_data)
            TyContext.ftlog.info('CliToVersService->generateFrom gameId=', self.__gameId, load_data, self.__clitovers)
        except:
            TyContext.ftlog.exception()
            return False
    '''

    def _generateFrom(self, data):
        assert (isinstance(data, dict))
        clitovers = {}
        for key, value in data.items():
            cliv = ClientVersions(key)
            clitovers[key] = cliv
            for verdata in value:
                ver = Version.generateFrom(verdata)
                if ver:
                    cliv.addVersion(ver)
                else:
                    raise TyContext.FreetimeException(-1, 'Bad version data:' + str(data))
        return clitovers

    def getNeedUpdateVersion(self, clientid, updatever):
        try:
            load_data = TyContext.Configure.get_game_item_json(self.__gameId, 'clients.inc.upgrade.map', {})
            TyContext.ftlog.info('CliToVersService->load gameId=', self.__gameId, load_data)
            clitovers = self._generateFrom(load_data)
            TyContext.ftlog.info('CliToVersService->generateFrom gameId=', self.__gameId, load_data, clitovers)
        except:
            TyContext.ftlog.exception()
            return None
        if clientid in clitovers:
            clv = clitovers[clientid]
            return clv.makeNeedUpdateVersion(updatever)
        return None


class SaveLoadHelper(object):
    @classmethod
    def load(cls, file):
        file = os.path.abspath(file)
        if not os.path.isfile(file): return None
        size = os.path.getsize(file)
        load_data = '{}'
        if size > 0:
            try:
                fp = open(file, 'rb')
                load_data = fp.read(size)
                fp.close()
            except:
                TyContext.ftlog.exception()
                load_data = '{}'
        TyContext.ftlog.debug('SaveLoadHelper->load', file, load_data)
        return load_data

    @classmethod
    def save(cls, file, data):
        if data == None: return False
        try:
            cls.checkPath(file)
            fp = open(file, 'wb+')
            fp.write(data)
            fp.flush()
            fp.close()
            return True
        except:
            pass
        return False

    @classmethod
    def checkPath(cls, file):
        file = os.path.abspath(file)
        splites = file.split('/')
        dict = os.getcwd()
        if len(splites) > 1:
            file_l = len(splites[-1])
            dict = file[0: 0 - file_l]
        if not os.path.exists(dict):
            os.makedirs(dict)
        return


class GameIncUpdate(object):
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance == None:
            cls._instance = cls()
            cls._instance.initialize()
        return cls._instance

    def __init__(self):
        self.__gid2mnr = {}

    def initialize(self):
        # 读配置
        self.__gid2mnr = {
            6: CliToVersService(6),
            10: CliToVersService(10),
            7: CliToVersService(7),
            9999: CliToVersService(9999),
        }

        # 初始化
        # self.load()

    def getNeedUpdateVersion(self, gid, clientid, updatever):
        if gid in self.__gid2mnr:
            return self.__gid2mnr[gid].getNeedUpdateVersion(clientid, updatever)
        return None

    def load(self):
        for k, v in self.__gid2mnr.items():
            v.load()
            TyContext.ftlog.debug('GameIncUpdate load', k)


# 全量更新
class GameFullUpdate(object):
    '''
    Download APK to insall
    '''

    @classmethod
    def getFullUpdateInfo(cls, gameId, clientId):
        configData = TyContext.Configure.get_game_item_json(gameId, 'clients.full.upgrade.map', {})
        if clientId in configData:
            return configData[clientId]
        else:
            return None


# 差分更新
class GameDiffUpdate(object):
    '''
    Download diff file
    Patch with old apk file already installed in phone, generate new apk file
    Different with full update and inc update, md5 is new apk file's hash, not update file's[diff file] hash
    If match, new apk file can be trusted
    '''

    @classmethod
    def getDiffUpdateInfo(cls, gameId, clientId):
        configData = TyContext.Configure.get_game_item_json(gameId, 'clients.diff.upgrade.map', {})
        if clientId in configData:
            return configData[clientId]
        else:
            return None


if __name__ == '__main__':
    vm = VersionManager(6, 'versions6.json')
    print vm.load()
    print vm.generateToSave()
    print vm.save()

    svc = CliToVersService(6)
    print svc.load()

    clvm = CliToVersManager('clientversions6.json', 'export6.json', 6)
    print clvm.load()
    print clvm.save()
    print clvm.export()

    pass
