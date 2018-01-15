# -*- coding=utf-8 -*-

class CloseWebView:
    __close_html__ = '''
<!DOCTYPE HTML><html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<script>
var os_type = "unknown"
function checkSystemInit() {
    if (navigator.userAgent.match(/android/i)) {
        os_type = "android";
    } else if (navigator.userAgent.match(/iPhone|iPod|iPad/i)) {
        os_type = "ios";
    }else{
        os_type = "unknown";
    }
}
checkSystemInit();
var TY = new Object();
TY.delaytime = 1;
TY.AnonyJSFuncN = 0;
TY.iosArgList = [];
TY.iosCallTimer = 0;
TY.jsCallNativeIOS = function() {
    try {
        var iosargs = TY.iosArgList.shift();
        if (iosargs) {
            document.location = 'http://javascript.call.ios.native?' + iosargs;
        }
        if (TY.iosArgList.length > 0) {
            setTimeout(TY.jsCallNativeIOS, 30);
        } else {
            TY.iosCallTimer = 0;
        }
    } catch (e) {
        alert('jsCallNativeIOS-->' + e);
    }
}
TY.jsCallNative = function(params) {
    if (TY.delaytime < 0) {
        TY.delaytime = 30;
    }
    var args = JSON.stringify(params);
    if (os_type == 'ios') {
        TY.iosArgList.push(encodeURIComponent(args));
        if (TY.iosCallTimer == 0) {
            TY.iosCallTimer = 1;
            setTimeout(TY.jsCallNativeIOS, TY.delaytime);
        }
        return;
    }
    function caller() {
        var obj = window._javascript_4_java_
        if (!obj && os_type == "unknown") {
            setTimeout(caller, TY.delaytime);
            return;
        }
        try {
            args = args.replace(/\\\\/g, '\\\\\\\\')
            args = args.replace(/\'/g, '\\\\\\'')
            eval('window._javascript_4_java_.exec(\\'' + args + '\\')');
        } catch (e) {
            alert('jsCallNativeAndroid->' + e)
        }
    }
    setTimeout(caller, TY.delaytime);
}
TY.callNative = function(module, act, params) {
    var args = {
        module : module,
        cmd : {
            action : act,
            params : params
        }
    };
    TY.jsCallNative(args);
}
try{
    TY.callNative('common', 'CloseWindow', {});
}catch(e){
    alert('close->' + e)
}
</script></head><body></body></html>
'''

    def getCloseHtml(self):
        return self.__close_html__


CloseWebView = CloseWebView()
