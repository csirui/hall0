function hlog(msg) {
	if (window.parent) {
		var plog = parent.window.log;
		if (plog) {
			plog(msg);
		}
	}
}

var TY = {}, myglobal = {};
var mydebug = true;

var user,clientId,simpay = 'false',phoneType = 'unknown'; // 交互公共变量

TY.nativeActions = {};
TY.JSONAPIVER = 'v1/';
TY.delaytime = -1;
TY.domain = document.location.protocol + "//" + document.location.host + '/'
//TY.domain = "http://125.39.220.82/";
//TY.domain = "http://192.168.1.42/"

TY.domainlocal = TY.domaincross = TY.domain;

TY.showWaiting = function(msg) {
	var dialog = "<div class='waiting'><span class='waiting_box'>" + msg + "</span></div>";
	$($("body")[0]).append(dialog);
	var width = ($('.waiting')[0].clientWidth - $('.waiting_box')[0].clientWidth) / 2
	$('.waiting_box').css('left', width + 'px');
}

TY.hideWaitting = function() {
	var waiting = $('.waiting')[0];
	if (waiting && waiting.parentNode) {
		waiting.parentNode.removeChild(waiting);
	}
}

TY.showMessage = function(msg, time) {
	var dialog = "<div class='message'><span class='message_box'>" + msg + "</span></div>";
	$($("body")[0]).append(dialog);
	var width = ($('.message')[0].clientWidth - $('.message_box')[0].clientWidth) / 2
	setTimeout("TY.hideMessage()", time == undefined ? 2000 : time);
}

TY.hideMessage = function() {
	var message = $('.message')[0];
	if (message && message.parentNode) {
		message.parentNode.removeChild(message)
	}
}

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
		//alert('jsCallNativeIOS-->' + e);
	}
}

TY.jsCallNative = function(params) {
	if (TY.delaytime < 0) {
		TY.delaytime = 1;
		var p = window.parent;
		if (p) {
			var plog = parent.window.log;
			if (plog) {
				TY.delaytime = 20;
                os_type = "unknown"
			}
		}
	}
	var timeout = 30
	var args = JSON.stringify(params);
	if (os_type == 'ios') {
		TY.iosArgList.push(encodeURIComponent(args));
		if (TY.iosCallTimer == 0) {
			TY.iosCallTimer = 1;
			setTimeout(TY.jsCallNativeIOS, timeout);
		}
		return;
	}

    function caller() {
        var obj = window._javascript_4_java_
        if (!obj && os_type == "unknown") {
            setTimeout(caller, timeout);
            return;
        }
        try {
            args = args.replace(/\\/g, '\\\\')
            args = args.replace(/\'/g, '\\\'')
            eval('window._javascript_4_java_.exec(\'' + args + '\')');
        } catch (e) {
            //alert('jsCallNativeAndroid->' + e)
        }
    }

	setTimeout(caller, timeout);
}

var AnonyJSFuncN = 0;
TY.callNative = function(module, act, params, callback) {
	var c = '';
	if (callback && typeof (callback) == 'function') {
		c = callback.name;
		if (c.length <= 0)
			c = '_AN_JS_F_' + AnonyJSFuncN++;
		if (act == 'PageInit') {
			TY.regAction(c, function(params, isError, errInfo) {
                var server = params['server']
				if (server) {
					TY.domaincross = params['server']
				}
				callback(params, isError, errInfo)
			});
		} else {
			TY.regAction(c, callback);
		}
	}
	var args = {
		module : module,
		callback : c,
		cmd : {
			action : act,
			params : params
		}
	};
	TY.jsCallNative(args);
}

TY.regAction = function(action, fun) {
	TY.nativeActions[action] = fun;
}

myglobal.nativeCallJs = function(jsonString) {
	var datas = null;
	try {
		datas = JSON.parse(jsonString);
		var cmd = datas['cmd'];
		action = cmd['action'];
		params = cmd['params'];
		error = cmd['error'];
		var isError = (error != undefined && error['code']) ? true : false;
		var errorInfo = (isError) ? error['info'] : '';
		fun = TY.nativeActions[action];
		if (typeof (fun) == 'function') {
            if(isError){
                TY.callNativeShow();
                TY.showMessage('系统错误！' + ' ' + errorInfo);
            }else if(action=='OnPageInit'){
                phoneType = params['phoneType'];
                clientId = params['clientId'];
                user = params['user'];
                simpay = params['simpay'];
                TY.callNativeShow();
            }
			fun(params, isError, errorInfo)
			return 'ok'
		} else {
			// throw action + ' not found';
			return 'error'
		}
	} catch (e) {
		TY.callNativeShow();
		//alert('java-> ' + e.name + e.message  + e.stack + jsonString);
		return 'exception'
	}
}

TY.getLocalMsg = function(key, paramList) {
	var str = local_msg_current['' + key];
	if (str) {
		if (paramList) {
			for ( var i = 0; i < paramList.length; i++) {
				var r = new RegExp('\\$\\{' + i + '\\}', 'g')
				str = str.replace(r, '' + paramList[i]);
			}
		}
		return str;
	}
	hlog('System Error, Message Key Bot Found ->' + key);
	return 'System Message Error';
}

TY.doRequest = function(action, dataType, method) {
	if (dataType == undefined) {
		dataType = 'json';
	}
	if (method == undefined) {
		method = 'POST';
	}
	if (action.cache == undefined) {
		action.cache = false;
	}
	hlog('JSON request ->type=' + dataType + ' method=' + method + ' action=' + JSON.stringify(action));
	var errorFun = function(jqXHR, textStatus, errorThrown) {
		hlog('JSON response error->' + action.method + ' error->' + errorThrown);
		TY.hideWaitting();
		data = {
			error : {
				code : -99,
				info : TY.getLocalMsg('neterr')
			}
		}
		action.callback(data, action, false);
	};
	var successFun = function(data, textStatus, jqXHR) {
		hlog('JSON response->' + action.method + JSON.stringify(data));
		TY.hideWaitting();
		result = true;
		if (data == null || data['error'] != undefined)
			result = false;
		action.callback(data, action, result);
	};
	if (action.method.indexOf('http://') < 0) {
		action.method = TY.domain + action.method;
	}
	var ajaxPro = {
		dataType : dataType,
		cache : action.cache,
		type : method,
		url : action.method,
		error : errorFun,
		success : successFun,
		data : action.params
	};
	$.ajax(ajaxPro);
}

TY.getUrlParam = function(name) {
	var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
	var r = window.location.search.substr(1).match(reg);
	if (r != null) {
		return decodeURIComponent(r[2]);
	}
	return null;
}

TY.intval = function(v) {
	v = parseInt(v);
	return isNaN(v) ? 0 : v;
}

TY.bindTouchClick = function(node, action, bubble) {
	var touched = false;
	if (document.ontouchstart === undefined) {
		node.click(function(evt) {
            if (bubble == false) {
                evt.stopPropagation();
            }
			action(this, evt);
		});
		return;
	}
	node.bind('touchstart', function(evt) {
		touched = true;
        if (bubble == false) {
            evt.stopPropagation();
        }
		if (evt.name == 'click')
			action(this, evt);
	});
	node.bind('touchmove', function(evt) {
		touched = false;
	});
	node.bind('touchend', function(evt) {
        if (bubble == false) {
            evt.stopPropagation();
        }
		if (touched) {
			action(this, evt)
		}
	});
}

TY.resetDivOuterHeight = function() {
	var height = document.documentElement.clientHeight;
	$(".div_outer").css("height", height + 'px');
}

TY.showAlertStyle = function(title, msg, styleClass, callback, width, height) {
    TY.showAlert(title, msg, callback, width, height,styleClass)
}
TY.showAlert = function(title, msg, callback, width, height, styleClass) {
    if(styleClass==undefined) styleClass = ''
	var strOk = TY.getLocalMsg('but_ok');
	var html = '<div class="alert '+styleClass+'"><div class="alert_box"><table border="0" cellspacing="0" cellpadding="0">'
			+ '<tr valign="bottom" class="alert_line1"><td align="center">' + title + '</td><tr valign="middle" class="alert_line2"><td align="center">' + msg
			+ '</td></tr><tr valign="top"><td align="center">' + '<a class="green_button alert_ok" href="javascript:;">' + strOk
			+ '</a></td></tr></table></div></div>'

	var div0 = $('body');
	$(div0).append(html);
	if (isNaN(width)) {
		width = div0.clientWidth;
	}
	if (isNaN(height)) {
		height = div0.clientHeight;
	}
	$('.alert').css({
		'width' : width,
		'height' : height
	});

	$('.alert_ok').bind('click', function() {
		$('.alert').remove();
		if (typeof (callback) == 'function') {
			callback();
		}
	});
}

TY.showChoiceYesNo = function(title, msg, callback) {
	var strOk = TY.getLocalMsg('but_ok');
	var strCancel = TY.getLocalMsg('but_cancel');
	var html = '<div class="alert"><div class="alert_box"><table border="1" cellspacing="0" cellpadding="0">'
			+ '<tr valign="bottom" class="alert_line1"><td colspan="2" align="center">' + title
			+ '</td><tr valign="middle" class="alert_line2"><td colspan="2" align="center">' + msg + '</td></tr><tr valign="top"><td align="center">'
			+ '<a class="green_button choice_yes" href="javascript:;">' + strOk + '</a></td><td align="center">'
			+ '<a class="gray_button choice_no" href="javascript:;">' + strCancel + '</a></td></tr></table></div></div>'

	var div0 = $('div')[0];
	$(div0).append(html);
	$('.alert').css({
		'width' : div0.clientWidth + 'px',
		'height' : div0.clientHeight + 'px'
	});

	$('.choice_yes').bind('click', function() {
		$('.alert').remove();
		if (typeof (callback) == 'function') {
			callback(true);
		}
	});
	$('.choice_no').bind('click', function() {
		$('.alert').remove();
		if (typeof (callback) == 'function') {
			callback(false);
		}
	});
}

TY.updateTabLayout = function() {
	var height = document.documentElement.clientHeight;
	var headHeight = $('.header')[0].clientHeight;
	var cheight = height - headHeight - 30;
	if ($(".content").length <= 0) {
		return;
	}
	$(".content").css("height", cheight + 'px');
}

TY.bindUiTab = function(node_class, action) {
	node_class = node_class + '>li';
	var node = $(node_class);
	TY.bindTouchClick(node, function(node, evt) {
		if (node.className == 'current')
			return;
		var curTab = $(node_class + '.current');
		curTab.removeClass('current');
		node.className = 'current';
		action(node)
	})
}

TY.switchSelectItem = function(node_tag, index, canRid) {
	var node = $(node_tag).eq(index);
	if ($(node).hasClass('cur')) {
		if (canRid) {
			$(node).removeClass('cur');
			return false;
		}
		return true;
	}
	var curTab = $(node_tag + '.cur');
	curTab.removeClass('cur');
	$(node).addClass('cur');
	return true;
}

TY.showDialog = function(dlgId) {
	console.log(dlgId)
	$("#" + dlgId).css('display', 'block');
	var dlg_box = $("#" + dlgId)[0].children[0];
	dlg_box.style.height = dlg_box.clientHeight + 'px';
}

TY.closeDialog = function(obj) {
	$(obj).parents('.dialog').css('display', 'none');
}

TY.isCallNativeShow = false;
TY.callNativeShow = function() {
	if (TY.isCallNativeShow == false) {
		TY.isCallNativeShow = true
        TY.callNative('common', 'doPageShow', {});
	}
}

TY.callNativeClose = function() {
	TY.callNative('common', 'CloseWindow', {});
}

TY.callNativeUpdateUser = function() {
	TY.callNative('user', 'UpUserInfo', {});
}

var os_type = "unknown" // android,ios,unknown
checkSystemInit();
var is_android_2x = false;

function checkSystemInit() {
	protocol = document.location.protocol
	if (navigator.userAgent.match(/android/i)) {
		os_type = "android"
		if (protocol.indexOf('file') == 0) {
			TY.domainlocal = 'file:///android_asset/'
		}
	} else if (navigator.userAgent.match(/iPhone|iPod|iPad/i)) {
		os_type = "ios"
	}
}

function isAndroid2x() {
	if (is_android_2x || navigator.userAgent.match(/android.2\./i)) {
		is_android_2x = true
		return true;
	}
	return false
}

$().ready(function() {
//    checkScreenDpi();
    TY.regAction('backClick', backclick);
})

function checkScreenDpi(){
    var vp = document.getElementsByName('viewport')[0]
    if(window.screen.availWidth < 500 || window.screen.availWidth < 1000){
        if(os_type=='android'){
            vp.setAttribute( 'content', 'target-densitydpi=195, width=device-width, user-scalable=no' );
        }
        if(os_type=='ios'){
            vp.setAttribute( 'content', 'initial-scale=0.75,maximum-scale=1.0,minimum-scale=0.5,user-scalable=1,width=640' );
        }
    }
    if(window.screen.availWidth < 860){
        if(os_type=='android'){
            vp.setAttribute( 'content', 'target-densitydpi=195, width=device-width, user-scalable=no' );
        }
        if(os_type=='ios'){
            vp.setAttribute( 'content', 'initial-scale=0.75,maximum-scale=1.0,minimum-scale=0.5,user-scalable=1,width=640' );
        }
    }
}

backclick=function(params, isError, errInfo){
    TY.callNativeClose();
}

TY.regAction('OnUserInfoChanged', OnUserInfoChanged);
function OnUserInfoChanged(params, isError, errInfo) {
	if (!isError) {
		user = params['user'];
	}
}

TY.getClientId = function(params) {
	var clientId = params['clientId'];
	if (clientId == undefined) {
		var user = params['user'];
		if (user != undefined) {
			clientId = user['clientId'];
		}
	}
	if (clientId == undefined) {
		clientId = ''
	}
	return clientId;
}

TY.getClientVersion = function(params) {
	var clientId = TY.getClientId(params);
	var strs = clientId.split('_');
	var ver = parseFloat(strs[1]);
	if (isNaN(ver)) {
		return 0;
	}
	return ver;
}