# -*- coding=utf-8 -*-

_IDX_URL = 0

def report_bi_http_(user_id, rec_type, data):
    from tyframework.context import TyContext
    httpconf = TyContext.Configure.get_global_item_json('servers.bi.http', {}, None, True)
    if not httpconf :
        return
    lsurls = httpconf.get('servers')
    if not lsurls or not isinstance(lsurls, list):
        return
    groupinfos = httpconf.get('groupinfos')
    if not groupinfos :
        return
    groupinfo = groupinfos.get(rec_type)
    if not groupinfo :
        return
    pkey = str(TyContext.TYGlobal.run_process_type()) + str(TyContext.TYGlobal.run_process_id())
    sids = httpconf.get('sids', [])
    if not TyContext.strutil.reg_matchlist(sids, pkey) :
        return
    log_type = groupinfo.get('log_type')
    group = groupinfo.get('name')
    gcount = groupinfo.get('count')
    if log_type and group and gcount and isinstance(gcount, int) and gcount > 0 :
        if data.find('msg:') == 0 :
            data = data[12:]
        group = group + str(user_id % gcount)
        header = {"log-type": log_type, "log-group": group}
        global _IDX_URL
        lsurl = lsurls[_IDX_URL % len(lsurls)]
        _IDX_URL = _IDX_URL + 1
        if log_type == 'chip' :
            data = data + '\x00\x00\x00\x00'

        timeout = httpconf.get('log_server_time_out', 0.5)
        retryMax = httpconf.get('log_server_retry_count', 6)
        _retry_report_http(lsurl, 'POST', header, data, timeout, {'try' : 0, 'max' : retryMax})


def _retry_report_http(targetUrl, method, header, body, connect_timeout, retrydata):
    from twisted.web import client
    from tyframework.context import TyContext
    TyContext.ftlog.debug('_retry_report_http', targetUrl, connect_timeout, retrydata)

    def _succ_code_inner(response_, *args, **argd):
        pass

    def _err_code_inner(*args, **argd):
        if retrydata :
            retrydata['try'] += 1
            if retrydata['try'] > retrydata['max'] :
                TyContext.ftlog.error('_retry_report_http _err_code_inner', retrydata, targetUrl[0:30], args, argd)
            else:
                _retry_report_http(method, targetUrl, header, body, connect_timeout, retrydata)
        else:
            TyContext.ftlog.error('_retry_report_http _err_code_inner', retrydata, targetUrl[0:30], args, argd)

    d = client.getPage(targetUrl, method=method, headers=header, postdata=body)
    d.addCallback(_succ_code_inner)
    d.addErrback(_err_code_inner)


from tyframework._private_.bi import bireport_http
bireport_http.report_bi_http = report_bi_http_
