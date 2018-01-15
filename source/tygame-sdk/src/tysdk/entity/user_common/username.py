#! encoding=utf-8
'''
Created on 2014年6月23日

@author: zjgzzz@126.com
'''
import codecs
import random

from tyframework.context import TyContext


class UsernameGenerator(object):
    _instance = None

    def __init__(self, usernames):
        self._usernames = usernames

    @classmethod
    def loadNamesFromFile(cls, path, encoding='utf8'):
        '''从文件中加载关键词库'''
        f = None
        names = []
        try:
            f = codecs.open(path, 'r', encoding)
            keyword = f.readline()
            while keyword:
                keyword = keyword.strip()
                names.append(keyword)
                keyword = f.readline()
        except Exception, _:
            TyContext.ftlog.exception()
        finally:
            if f:
                f.close()
        return names

    @classmethod
    def createInstance(cls):
        assert (cls._instance is None)
        usernames = {}
        malefile = TyContext.TYGlobal.path_webroot() + '/male.txt'
        femalefile = TyContext.TYGlobal.path_webroot() + '/female.txt'
        usernames[0] = cls.loadNamesFromFile(malefile)
        usernames[1] = cls.loadNamesFromFile(femalefile)
        TyContext.ftlog.info('UsernameGenerator.createInstance malefile=', malefile, len(usernames[0]),
                             'femalefile=', femalefile, len(usernames[1]))
        cls._instance = UsernameGenerator(usernames)
        return cls._instance

    @classmethod
    def getInstance(cls):
        return cls._instance

    def generate(self, sex):
        sex = int(sex)
        usernames = self._usernames[sex] if sex in self._usernames else None
        ret = None
        if usernames and len(usernames) > 0:
            i = random.randint(0, len(usernames) - 1)
            ret = usernames[i]
        TyContext.ftlog.debug('UsernameGenerator.generate', sex, '==>', ret)
        return ret

    @classmethod
    def _get_redis_key_by_username(cls, userName):
        rname_prefix = 'username_'
        hash_base = 10000
        hash_value = hash(userName)
        return rname_prefix + str(hash_value % hash_base)

    @classmethod
    def _set_userid_by_username(cls, userName, userId):
        rname = cls._get_redis_key_by_username(userName)
        TyContext.RedisUserKeys.execute('HSET', rname, userName, userId)

    @classmethod
    def _get_userid_by_username(cls, userName):
        rname = cls._get_redis_key_by_username(userName)
        saved_datas = TyContext.RedisUserKeys.execute('HGET', rname, userName)
        return saved_datas

    @classmethod
    def _is_current_uid_need_save(cls, username, userid):
        saved_uid = cls._get_userid_by_username(username)
        if not saved_uid:
            return True
        if int(saved_uid) == int(userid):
            return True
        return False

    @classmethod
    def _get_alpha_with_digits_list(cls):
        dist_seq = []
        upper_alpha = [chr(x) for x in range(65, 91)]
        dist_seq.extend(upper_alpha)
        lower_alpaht = [chr(x) for x in range(97, 123)]
        dist_seq.extend(lower_alpaht)
        digit = [str(x) for x in range(0, 10)]
        dist_seq.extend(digit)
        return dist_seq

    @classmethod
    def _send_user_changename_card(cls, userid):
        '''
        赠送改名用户一张改名卡
        :param userid:
        :return:
        '''
        import time
        params = {
            'time': int(time.time()),
            'userId': userid,
            'kindId': 2001,  # 改名卡
            'count': 1
        }
        # 线上gdss 地址 10.3.0.18
        sendUrl = 'http://10.3.13.253:8040/_gdss/user/item/add?'
        query = '&'.join(k + '=' + str(params[k]) for k in sorted(params.keys()))
        query = query + 'www.tuyoo.com-api-6dfa879490a249be9fbc92e97e4d898d-www.tuyoo.com'
        from hashlib import md5
        m = md5(query)
        params['code'] = m.hexdigest().lower()
        import urllib
        sendUrl = sendUrl + urllib.urlencode(params)
        try:
            response, _ = TyContext.WebPage.webget(sendUrl)
        except Exception as e:
            pass

    @classmethod
    def _generate_unique_rand_user_name(cls, username):
        '''
        :param username:已有用户名
        :return:产生的随机用户名
        '''
        dist_seq = cls._get_alpha_with_digits_list()

        random.shuffle(dist_seq)
        name_suffix = '_' + ''.join(random.sample(dist_seq, 4))
        rand_name = username + name_suffix
        if cls._get_userid_by_username(rand_name):
            return cls._generate_unique_rand_user_name(username)
        else:
            return rand_name

    @classmethod
    def _save_userid_username(cls, username, userid):
        TyContext.RedisUser.execute(userid, 'HSET', 'user:' + str(userid), 'name', username)
        cls._set_userid_by_username(username, userid)

    @classmethod
    def check_and_save_user_name(cls, username, userid):
        '''
        检查 当前用户名
        符合条件的修改掉
        :param username:
        :param userid:
        :return:修改后的用户名
        '''
        if isinstance(username, unicode):
            username = username.encode('utf-8')
        saved_uid = cls._get_userid_by_username(username)
        if saved_uid and int(saved_uid) == int(userid):
            return username
        elif len(username) < 4:
            new_username = cls.generate_unique_new_user_name(userid)
        else:
            new_username = cls._generate_unique_rand_user_name(username)
        cls._save_userid_username(new_username, userid)
        cls._send_user_changename_card(userid)
        return new_username

    @classmethod
    def change_old_user_name(cls, username, userid, mo):
        '''

        :param username:
        :param userid:
        :param mo:
        :return:
        '''
        if isinstance(username, unicode):
            username = username.encode('utf-8')
        saved_uid = cls._get_userid_by_username(username)
        rname = cls._get_redis_key_by_username(username)
        if saved_uid:
            if int(saved_uid) != int(userid):
                mo.setResult('info', '该昵称已被使用，试试后面加个数字吧')
                mo.setResult('code', 1)
                return
        old_uname = TyContext.RedisUser.execute(userid, 'HGET', 'user:' + str(userid), 'name')
        saved_old_uid = cls._get_userid_by_username(old_uname)
        if saved_old_uid and int(saved_old_uid) != int(userid):
            mo.setResult('info', 'userId 对应关系异常', userid, username)
            mo.setResult('code', 2)
            return
        rname = cls._get_redis_key_by_username(old_uname)
        TyContext.RedisUserKeys.execute('HDEL', rname, old_uname)
        # 删除之前用户名的对应关系
        if len(username) < 3:
            mo.setResult('info', '请输入3-14位字符')
            mo.setResult('code', 2)
            return
        if TyContext.KeywordFilter.isContains(username):
            mo.setResult('info', '含非法字符，请修改')
            mo.setResult('code', 3)
            return
        cls._save_userid_username(username, userid)
        mo.setResult('info', '昵称修改成功')
        mo.setResult('code', 0)

    @classmethod
    def generate_unique_new_user_name(self, userId):
        '''
        创建新用户
        :param userId:
        :return:
        '''
        name_prefix = '来宾'
        userId_fixed = int(userId) % 10000
        name_middle = '%04x' % userId_fixed
        dist_seq = []
        upper_alpha = [chr(x) for x in range(65, 91)]
        dist_seq.extend(upper_alpha)
        lower_alpaht = [chr(x) for x in range(97, 123)]
        dist_seq.extend(lower_alpaht)
        random.shuffle(dist_seq)
        name_suffix = ''.join(random.sample(dist_seq, 5))
        new_name = name_prefix + name_middle + name_suffix
        if self._get_userid_by_username(new_name):
            return self.generate_unique_new_user_name(userId)
        else:
            return new_name
