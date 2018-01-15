# -*- coding=utf-8 -*-

# usage:
# $ python -m unittest -f test.tu360api.testapi.TestAPI

import unittest
from httplib import HTTPConnection
from urllib import urlencode
import hashlib
import hmac
import json
import uuid


appid = 1001
appkey = '4c18985e946fdc7faf97764751f449cd'
server = '42.62.53.180'
gettyid_uri = '/open/v3/user/gettyid'
gid2qid_uri = '/open/v3/user/gid2qid'
revokeqid_uri = '/open/v3/user/revokeqid'
get_chip_url = '/open/v3/pay/getchip'
incr_chip_url = '/open/v3/pay/incrchip'
exchange_bean_url = '/open/v3/pay/exchangebean'


def calc_sign(params):
    sign_str = '&'.join(['%s=%s' % (k, params[k]) for k in sorted(params.keys())])
    return hmac.new(appkey, sign_str, hashlib.sha1).hexdigest()


def check_sign(params):
    sign = params['sign']
    del params['sign']
    expected = calc_sign(params)
    if sign != expected:
        return False
    return True


class TestAPI(unittest.TestCase):

    def setUp(self):
        self._c = HTTPConnection(server)

    def tearDown(self):
        self._c.close()

    def test_revoke_qid__sign_error(self):
        params = {}
        params['snsid'] = '360:12345678'
        params['appid'] = 1001
        params['sign'] = 'this_is_wrong_sign'
        url = revokeqid_uri + '?' + urlencode(params)
        self._c.request('GET', url)
        response = self._c.getresponse()
        data = response.read()
        #print data
        ret = json.loads(data)
        self.assertTrue(check_sign(ret))
        self.assertNotEqual(ret['code'], 0)
        self.assertEqual(ret['msg'], 'sign error')

    def test_revoke_qid__wrong_snsid(self):
        params = {}
        params['snsid'] = 'wrong:12345678'
        params['appid'] = 1001
        params['sign'] = calc_sign(params)
        url = revokeqid_uri + '?' + urlencode(params)
        self._c.request('GET', url)
        response = self._c.getresponse()
        data = response.read()
        ret = json.loads(data)
        self.assertTrue(check_sign(ret))
        self.assertNotEqual(ret['code'], 0)
        self.assertEqual(ret['msg'], 'wrong snsid')

    def test_revoke_qid__not_registered(self):
        params = {}
        params['snsid'] = '360:not_exist_qid'
        params['appid'] = 1001
        params['sign'] = calc_sign(params)
        url = revokeqid_uri + '?' + urlencode(params)
        self._c.request('GET', url)
        response = self._c.getresponse()
        data = response.read()
        #print data
        ret = json.loads(data)
        self.assertTrue(check_sign(ret))
        self.assertNotEqual(ret['code'], 0)

    def __create_tyid_by_getchip(self):
        params = {}
        params['snsid'] = '360:12345678'
        params['appid'] = 1001
        params['sign'] = calc_sign(params)
        url = get_chip_url + '?' + urlencode(params)
        self._c.request('GET', url)
        response = self._c.getresponse()
        self._c = HTTPConnection(server)

    def test_revoke_qid__success(self):
        self.__create_tyid_by_getchip()

        params = {}
        params['snsid'] = '360:12345678'
        params['appid'] = 1001
        params['sign'] = calc_sign(params)
        url = revokeqid_uri + '?' + urlencode(params)
        self._c.request('GET', url)
        response = self._c.getresponse()
        data = response.read()
        #print data
        ret = json.loads(data)
        self.assertTrue(check_sign(ret))
        self.assertEqual(ret['code'], 0)
        self.assertEqual(ret['snsid'], params['snsid'])

    def __revoke_qid(self):
        params = {}
        params['snsid'] = '360:12345678'
        params['appid'] = 1001
        params['sign'] = calc_sign(params)
        url = revokeqid_uri + '?' + urlencode(params)
        self._c.request('GET', url)
        response = self._c.getresponse()
        data = response.read()
        self._c = HTTPConnection(server)

    def test_get_chip__new_tyid(self):
        self.__revoke_qid()

        params = {}
        params['snsid'] = '360:12345678'
        params['appid'] = 1001
        params['sign'] = calc_sign(params)
        url = get_chip_url + '?' + urlencode(params)
        self._c.request('GET', url)
        response = self._c.getresponse()
        data = response.read()
        ret = json.loads(data)
        self.assertTrue(check_sign(ret))
        self.assertEqual(ret['code'], 0)
        self.assertEqual(ret['curr_chip'], 0)

    def __new_tyid_w_100_chip(self):
        self.__revoke_qid()

        params = {}
        params['snsid'] = '360:12345678'
        params['appid'] = 1001
        params['count'] = 100
        self._last_txnid = str(uuid.uuid4())
        params['transactionid'] = self._last_txnid
        params['sign'] = calc_sign(params)
        url = incr_chip_url + '?' + urlencode(params)
        self._c.request('GET', url)
        response = self._c.getresponse()
        data = response.read()
        ret = json.loads(data)
        self.assertTrue(check_sign(ret))
        self.assertEqual(ret['code'], 0)
        self.assertEqual(ret['add_chip'], params['count'])
        self.assertEqual(ret['final_chip'], params['count'])
        self.assertEqual(ret['transactionid'], params['transactionid'])
        self._c = HTTPConnection(server)
        return ret['userid']

    def test_incr_chip(self):
        self.__revoke_qid()

        #incr with tyid creation
        params = {}
        params['snsid'] = '360:12345678'
        params['appid'] = 1001
        params['count'] = 100
        self._last_txnid = str(uuid.uuid4())
        params['transactionid'] = self._last_txnid
        params['sign'] = calc_sign(params)
        url = incr_chip_url + '?' + urlencode(params)
        self._c.request('GET', url)
        response = self._c.getresponse()
        data = response.read()
        ret = json.loads(data)
        self.assertTrue(check_sign(ret))
        self.assertEqual(ret['code'], 0)
        self.assertEqual(ret['add_chip'], params['count'])
        self.assertEqual(ret['final_chip'], params['count'])
        self.assertEqual(ret['transactionid'], params['transactionid'])

        #decr succ
        params = {}
        params['snsid'] = '360:12345678'
        params['appid'] = 1001
        params['count'] = -60
        self._last_txnid = str(uuid.uuid4())
        params['transactionid'] = self._last_txnid
        params['sign'] = calc_sign(params)
        url = incr_chip_url + '?' + urlencode(params)
        self._c.request('GET', url)
        response = self._c.getresponse()
        data = response.read()
        ret = json.loads(data)
        self.assertTrue(check_sign(ret))
        self.assertEqual(ret['code'], 0)
        self.assertEqual(ret['add_chip'], -60)
        self.assertEqual(ret['final_chip'], 40)
        self.assertEqual(ret['transactionid'], params['transactionid'])

        #decr fail
        params = {}
        params['snsid'] = '360:12345678'
        params['appid'] = 1001
        params['count'] = -60
        self._last_txnid = str(uuid.uuid4())
        params['transactionid'] = self._last_txnid
        params['sign'] = calc_sign(params)
        url = incr_chip_url + '?' + urlencode(params)
        self._c.request('GET', url)
        response = self._c.getresponse()
        data = response.read()
        ret = json.loads(data)
        self.assertTrue(check_sign(ret))
        self.assertEqual(ret['code'], 2)
        self.assertEqual(ret['add_chip'], 0)
        self.assertEqual(ret['final_chip'], 40)
        self.assertEqual(ret['transactionid'], params['transactionid'])

        #incr: dup txnid
        params = {}
        params['snsid'] = '360:12345678'
        params['appid'] = 1001
        params['count'] = 100
        params['transactionid'] = self._last_txnid
        params['sign'] = calc_sign(params)
        url = incr_chip_url + '?' + urlencode(params)
        self._c.request('GET', url)
        response = self._c.getresponse()
        data = response.read()
        ret = json.loads(data)
        self.assertTrue(check_sign(ret))
        self.assertNotEqual(ret['code'], 0)
        self.assertEqual(ret['msg'], 'transactionid missing or already used')
        self.assertEqual(ret['transactionid'], params['transactionid'])

    def test_get_chip__old_tyid(self):
        userid = self.__new_tyid_w_100_chip()

        params = {}
        params['snsid'] = '360:12345678'
        params['appid'] = 1001
        params['sign'] = calc_sign(params)
        url = get_chip_url + '?' + urlencode(params)
        self._c.request('GET', url)
        response = self._c.getresponse()
        data = response.read()
        ret = json.loads(data)
        self.assertTrue(check_sign(ret))
        self.assertEqual(ret['code'], 0)
        self.assertEqual(ret['curr_chip'], 100)
        self.assertEqual(ret['userid'], userid)

    def test_exchange_bean__err_for_nothing(self):
        params = {}
        params['snsid'] = '360:12345678'
        params['appid'] = 1001
        params['for'] = 'nothing'
        params['count'] = 100
        params['eventId'] = 201
        self._last_txnid = str(uuid.uuid4())
        params['transactionid'] = self._last_txnid
        params['sign'] = calc_sign(params)
        url = exchange_bean_url + '?' + urlencode(params)
        self._c.request('GET', url)
        response = self._c.getresponse()
        data = response.read()
        ret = json.loads(data)
        self.assertTrue(check_sign(ret))
        self.assertNotEqual(ret['code'], 0)
        self.assertEqual(ret['transactionid'], params['transactionid'])
        self.assertEqual(ret['msg'], 'for parameter value error')

    def test_exchange_bean__succ_for_diamond(self):
        self.__revoke_qid()

        params = {}
        params['snsid'] = '360:12345678'
        params['appid'] = 1001
        params['for'] = 'diamond'
        params['count'] = 100
        params['eventId'] = 201
        self._last_txnid = str(uuid.uuid4())
        params['transactionid'] = self._last_txnid
        params['sign'] = calc_sign(params)
        url = exchange_bean_url + '?' + urlencode(params)
        self._c.request('GET', url)
        response = self._c.getresponse()
        data = response.read()
        ret = json.loads(data)
        self.assertTrue(check_sign(ret))
        self.assertEqual(ret['code'], 0)
        self.assertEqual(ret['add_diamond'], 10)
        self.assertEqual(ret['final_diamond'], 10)
        self.assertEqual(ret['transactionid'], params['transactionid'])

    def test_exchange_bean__succ_for_chip(self):
        self.__revoke_qid()

        params = {}
        params['snsid'] = '360:12345678'
        params['appid'] = 1001
        params['for'] = 'chip'
        params['count'] = 100
        params['eventId'] = 201
        self._last_txnid = str(uuid.uuid4())
        params['transactionid'] = self._last_txnid
        params['sign'] = calc_sign(params)
        url = exchange_bean_url + '?' + urlencode(params)
        self._c.request('GET', url)
        response = self._c.getresponse()
        data = response.read()
        ret = json.loads(data)
        self.assertTrue(check_sign(ret))
        self.assertEqual(ret['code'], 0)
        self.assertEqual(ret['add_chip'], 10000)
        self.assertEqual(ret['final_chip'], 10000)
        self.assertEqual(ret['transactionid'], params['transactionid'])

    def test_gid2qid(self):
        #fail with guestid_not_registered
        params = {}
        params['snsid'] = '360:12345678'
        params['guestid'] = '360:not_existed_qid'
        params['appid'] = 1001
        params['sign'] = calc_sign(params)
        url = gid2qid_uri + '?' + urlencode(params)
        self._c.request('GET', url)
        response = self._c.getresponse()
        data = response.read()
        ret = json.loads(data)
        self.assertTrue(check_sign(ret))
        self.assertNotEqual(ret['code'], 0)
        self.assertEqual(ret['msg'], 'guestid not registered')

        userid = self.__new_tyid_w_100_chip()

        params = {}
        params['snsid'] = '360:ZZ12345678'
        params['guestid'] = '360:12345678'
        params['appid'] = 1001
        params['sign'] = calc_sign(params)
        url = gid2qid_uri + '?' + urlencode(params)
        self._c.request('GET', url)
        response = self._c.getresponse()
        data = response.read()
        ret = json.loads(data)
        self.assertTrue(check_sign(ret))
        self.assertEqual(ret['code'], 0)
        self.assertEqual(ret['userid'], userid)

        params = {}
        params['snsid'] = '360:ZZ12345678'
        params['appid'] = 1001
        params['sign'] = calc_sign(params)
        url = get_chip_url + '?' + urlencode(params)
        self._c.request('GET', url)
        response = self._c.getresponse()
        data = response.read()
        ret = json.loads(data)
        self.assertTrue(check_sign(ret))
        self.assertEqual(ret['code'], 0)
        self.assertEqual(ret['userid'], userid)
        self.assertEqual(ret['curr_chip'], 100)


class SequentialTestLoader(unittest.TestLoader):

    def __init__(self, testcls):
        self._testcls = testcls

    def sortTestMethodsUsing(self, a, b):
        #ln = lambda f: getattr(self._testcls, f).im_func.func_code.co_firstlineno
        #lncmp = lambda _, a, b: cmp(ln(a), ln(b))
        ln_a = getattr(self._testcls, a).im_func.func_code.co_firstlineno
        ln_b = getattr(self._testcls, b).im_func.func_code.co_firstlineno
        #print a, ln_a, b, ln_b
        return cmp(ln_a, ln_b)


def main():
    #use sequential loader and fail fast, to make sure some testcases passed
    #before other cases
    loader = SequentialTestLoader(TestAPI)
    unittest.main(testLoader=loader, failfast=True)
    #unittest.main(testLoader=loader, verbosity=2, failfast=True)

if __name__ == '__main__':
    main()

