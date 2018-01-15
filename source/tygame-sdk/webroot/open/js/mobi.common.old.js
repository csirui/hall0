function hlog(msg) {
	var p = window.parent;
	if (p) {
		var plog = parent.window.log;
		if (plog) {
			plog(msg);
		}
	}
}

var myglobal = new Object();
var mydebug = true;

myglobal.nativeActions = new Object();
myglobal.JSONAPIVER = 'v1/';
myglobal.delaytime = -1;
myglobal.domain = document.location.protocol + "//" + document.location.host + '/'
myglobal.domainlocal = myglobal.domaincross = myglobal.domain;

myglobal.showWaiting = function(msg) {
	var dialog = "<div class='waiting'><span class='waiting_box'>" + msg + "</span></div>";
	$($("div")[0]).append(dialog);
	var width = ($('.waiting')[0].clientWidth - $('.waiting_box')[0].clientWidth) / 2
	$('.waiting_box').css('left', width + 'px');
}

myglobal.hideWaitting = function() {
	var waiting = $('.waiting')[0];
	if (waiting && waiting.parentNode) {
		waiting.parentNode.removeChild(waiting);
	}
}

myglobal.showMessage = function(msg, time) {
	var dialog = "<div class='message'><span class='message_box'>" + msg + "</span></div>";
	$($("body")[0]).append(dialog);
	var width = ($('.message')[0].clientWidth - $('.message_box')[0].clientWidth) / 2
	setTimeout("myglobal.hideMessage()", time == undefined ? 2000 : time);
}

myglobal.hideMessage = function() {
	var message = $('.message')[0];
	if (message && message.parentNode) {
		message.parentNode.removeChild(message)
	}
}

myglobal.iosArgList = [];
myglobal.iosCallTimer = 0;

myglobal.jsCallNativeIOS = function() {
	try {
		var iosargs = myglobal.iosArgList.shift();
		if (iosargs) {
			document.location = 'http://javascript.call.ios.native?' + iosargs;
		}
		if (myglobal.iosArgList.length > 0) {
			setTimeout(myglobal.jsCallNativeIOS, 30);
		} else {
			myglobal.iosCallTimer = 0;
		}
	} catch (e) {
		alert('jsCallNativeIOS-->' + e);
	}
}

myglobal.jsCallNative = function(params) {
	if (myglobal.delaytime < 0) {
		myglobal.delaytime = 1;
		var p = window.parent;
		if (p) {
			var plog = parent.window.log;
			if (plog) {
				myglobal.delaytime = 20;
			}
		}
	}

	var timeout = 30
	var args = JSON.stringify(params);
	if (tuyoo_os_type == 'ios') {
		myglobal.iosArgList.push(encodeURIComponent(args));
		if (myglobal.iosCallTimer == 0) {
			myglobal.iosCallTimer = 1;
			setTimeout(myglobal.jsCallNativeIOS, timeout);
		}
		return;
	}

	function caller() {
		var obj = window._javascript_4_java_
		if (!obj && tuyoo_os_type == "unknown") {
			setTimeout(caller, timeout);
			return;
		}
		try {
			args = args.replace(/\\/g, '\\\\')
			args = args.replace(/\'/g, '\\\'')
			eval('window._javascript_4_java_.exec(\'' + args + '\')');
		} catch (e) {
			alert('jsCallNativeAndroid->' + e)
		}
	}
	setTimeout(caller, timeout);
}

var AnonyJSFuncN = 0;
myglobal.callNative = function(module, act, params, callback) {
	var c = '';
	if (callback && typeof (callback) == 'function') {
		c = callback.name;
		if (c.length <= 0)
			c = '_AN_JS_F_' + AnonyJSFuncN++;
		if (act == 'PageInit') {
			myglobal.regAction(c, function(params, isError, errInfo) {
				if (params['server']) {
					myglobal.domaincross = params['server'] + '/'
				}
				callback(params, isError, errInfo)
			});
		} else {
			myglobal.regAction(c, callback);
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
	myglobal.jsCallNative(args);
}

myglobal.regAction = function(action, fun) {
	myglobal.nativeActions[action] = fun;
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
		fun = myglobal.nativeActions[action];
		if (typeof (fun) == 'function') {
			fun(params, isError, errorInfo)
		} else {
			// throw action + ' not found';
		}
	} catch (e) {
		myglobal.callNativeShow();
		alert('java-> ' + e.name + e.message + jsonString);
	}
}

myglobal.getLocalMsg = function(key, paramList) {
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

myglobal.doRequest = function(action, dataType, method) {
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
		myglobal.hideWaitting();
		data = {
			error : {
				code : -99,
				info : myglobal.getLocalMsg('neterr')
			}
		}
		action.callback(data, action, false);
	};
	var successFun = function(data, textStatus, jqXHR) {
		hlog('JSON response->' + action.method + JSON.stringify(data));
		myglobal.hideWaitting();
		result = true;
		if (data == null || data['error'] != undefined)
			result = false;
		action.callback(data, action, result);
	};
	if (action.method.indexOf('http://') < 0) {
		action.method = myglobal.domain + action.method;
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

myglobal.getUrlParam = function(name) {
	var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
	var r = window.location.search.substr(1).match(reg);
	if (r != null) {
		return decodeURIComponent(r[2]);
	}
	return null;
}

myglobal.intval = function(v) {
	v = parseInt(v);
	return isNaN(v) ? 0 : v;
}

myglobal.bindUiBtnEffectTheme = function(theme, node, bubble) {
	myglobal.bindUiBtnEffect(theme + '-up', theme + '-down', node, bubble);
}

myglobal.bindUiBtnEffect = function(uptheme, downtheme, node, bubble) {
	if (node == undefined || node == null) {
		node = $('.ui-btn-' + uptheme);
	}
	var touched = true;
	node.unbind('touchstart').unbind('touchmove').unbind('touchend');
	node.bind('touchstart', function(evt) {
		touched = true;
		var nodethis = $(this);
		setTimeout(function() {
			if (!touched) {
				return;
			}
			nodethis.addClass('ui-btn-' + downtheme);
			nodethis.removeClass('ui-btn-' + uptheme);
		}, 100);
		if (bubble == false) {
			evt.stopPropagation();
		}
	});
	node.bind('touchend touchmove', function(evt) {
		if (evt.type == 'touchmove') {
			touched = false;
		}
		var nodethis = $(this);
		setTimeout(function() {
			nodethis.removeClass('ui-btn-' + downtheme);
			nodethis.addClass('ui-btn-' + uptheme);
		}, 100);
	})
}

myglobal.bindTouchClick = function(node, action, bubble) {
	var touched = false;
	if (document.ontouchstart === undefined) {
		node.bind('click', function(evt) {
			action(this, evt);
		});
		return;
	}
	node.bind('touchstart', function(evt) {
		touched = true;
		if (evtname == 'click')
			action(this, evt);
		if (bubble == false) {
			evt.stopPropagation();
		}
	});
	node.bind('touchmove', function(evt) {
		touched = false;
	});
	node.bind('touchend', function(evt) {
		if (touched) {
			action(this, evt)
		}
	});
}

myglobal.resetDivOuterHeight = function() {
	var height = document.documentElement.clientHeight;
	$(".div_outer").css("height", height + 'px');
}

myglobal.showAlert = function(title, msg, callback, width, height) {
	var strOk = myglobal.getLocalMsg('but_ok');
	var html = '<div class="alert"><div class="alert_box"><table border="0" cellspacing="0" cellpadding="0">'
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

myglobal.showChoiceYesNo = function(title, msg, callback) {
	var strOk = myglobal.getLocalMsg('but_ok');
	var strCancel = myglobal.getLocalMsg('but_cancel');
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

myglobal.updateTabLayout = function() {
	var height = document.documentElement.clientHeight;
	var headHeight = $('.header')[0].clientHeight;
	var cheight = height - headHeight - 30;
	if ($(".content").length <= 0) {
		return;
	}
	$(".content").css("height", cheight + 'px');
}

myglobal.bindUiTab = function(node_class, action) {
	node_class = node_class + '>li';
	var node = $(node_class);
	myglobal.bindTouchClick(node, function(node, evt) {
		if (node.className == 'current')
			return;
		var curTab = $(node_class + '.current');
		curTab.removeClass('current');
		node.className = 'current';
		action(node)
	})
}

myglobal.switchSelectItem = function(node_tag, index, canRid) {
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

myglobal.showDialog = function(dlgId) {
	$("#" + dlgId).css('display', 'block');
	var dlg_box = $("#" + dlgId)[0].children[0];
	dlg_box.style.height = dlg_box.clientHeight + 'px';
}

myglobal.closeDialog = function(htmlObj) {
	$(htmlObj).parents('.dialog').css('display', 'none');
}

myglobal.isCallNativeShow = false;
myglobal.callNativeShow = function() {
	if (myglobal.isCallNativeShow == false) {
		myglobal.isCallNativeShow = true
		myglobal.callNative('common', 'doPageShow', {});
	}
}

myglobal.callNativeClose = function() {
	myglobal.callNative('common', 'CloseWindow', {});
}

myglobal.callNativeUpdateUser = function() {
	myglobal.callNative('user', 'UpUserInfo', {});
}

var tuyoo_os_type = "unknown" // android,ios,unknown
checkSystemInit();
// checkDivScrollOnLoad();
var is_android_2x = false;

function checkSystemInit() {
	protocol = document.location.protocol
	if (navigator.userAgent.match(/android/i)) {
		tuyoo_os_type = "android"
		if (protocol.indexOf('file') == 0) {
			myglobal.domainlocal = 'file:///android_asset/'
		}
	} else if (navigator.userAgent.match(/iPhone|iPod|iPad/i)) {
		tuyoo_os_type = "ios"
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
	checkDivScrollOnLoad();
})

function checkDivScrollOnLoad() {
	if (!isAndroid2x())
		return;
	// document.addEventListener('DOMContentLoaded', function() {
	// setTimeout(checkDivScroll, 150);
	// }, false);
	setTimeout(checkDivScroll, 100);
}

function checkDivScroll(scrollJqTag) {
	if (!scrollJqTag)
		scrollJqTag = '.scroll';
	if (!isAndroid2x() || $(scrollJqTag).length <= 0)
		return;
	var wrapper = $(scrollJqTag)[0]
	if (wrapper.children.length > 1) {
		var children = wrapper.childNodes;
		var len = children.length;
		var div = document.createElement("div");
		for ( var i = 0; i < len; i++) {
			div.appendChild(children[0])
		}
		wrapper.appendChild(div)
	}
	var scr = wrapper.children[0];
	wrapper.scrollTop = 1
	setTimeout(function() {
		myScroll = new iScroll(wrapper);
		// alert(wrapper.clientHeight)
	}, 500)
}

myglobal.regAction('OnUserInfoChanged', OnUserInfoChanged);
function OnUserInfoChanged(params, isError, errInfo) {
	if (!isError) {
		user = params['user'];
	}
}

function XLayerOut() {
	this.dw = document.documentElement.clientWidth;
	this.dh = document.documentElement.clientHeight;
	var agent = navigator.userAgent.toLowerCase();
	var divBig = 1;
	if (agent.indexOf('iphone') > 0 || agent.indexOf('ipod') > 0) {
		if (this.dw > 480 && this.dw != 568) {
			divBig = 2;
		}
	}
	if (agent.indexOf('ipad') > 0) {
		if (this.dw > 1024) {
			divBig = 2;
			var ds = this.dw;
			this.dw = this.dh;
			this.dh = ds;
		}
	}
	this.dw = this.dw / divBig;
	this.dh = this.dh / divBig;
	myglobal.viewWidth = this.dw;
	myglobal.viewHeight = this.dh;
	this.plist = this.initDisplayList();
}

XLayerOut.prototype.initDisplayList = function() {
	return [];
}

XLayerOut.prototype.nextReset = function(w, h, x, y, mx, my, m) {
	this.w = w;
	this.h = h;
	this.x = x;
	this.y = y;
	this.mx = mx;
	this.my = my;
	this.i = 0;
	this.j = 0;
	this.m = m;
}
XLayerOut.prototype.nextYY = function() {
	return this.y + (parseInt(this.j++ / this.m) * (this.h + this.my));
}
XLayerOut.prototype.nextXX = function() {
	return this.x + (this.i++ % this.m * (this.w + this.mx));
}
XLayerOut.prototype.setObjectCss = function(jqkey, csss) {
	var obj = $(jqkey);
	for ( var k in csss) {
		obj.css(k, csss[k]);
	}
}
XLayerOut.prototype.doLayoutList = function(plist) {
	for ( var i = 0; i < plist.length; i++) {
		var pitem = plist[i];

		var w = pitem[3];
		if (w < 0) {
			w = this.bw;
		} else {
			w = parseInt(this.rate * w);
		}

		var h = pitem[4];
		if (h < 0) {
			h = this.bh;
		} else {
			h = parseInt(this.rate * h);
		}

		var x = this.bx + parseInt(this.rate * pitem[1])
		var y = this.by + parseInt(this.rate * pitem[2])

		var csss = {
			'position' : 'absolute',
			'left' : x + 'px',
			'top' : y + 'px',
			'width' : w + 'px',
			'height' : h + 'px'
		};
		var fontsize = pitem[5];
		if (typeof (fontsize) == 'number' && fontsize > 0) {
			csss['font-size'] = parseInt(this.rate * pitem[5]) + 'px';
		}
		var bgimg = pitem[6];
		if (typeof (bgimg) == 'string' && bgimg.length > 0) {
			csss['background-image'] = 'url(' + bgimg + ')';
			csss['background-size'] = '100% 100%';
			csss['background-position'] = 'center';
			csss['background-repeat'] = 'no-repeat';
		}
		this.setObjectCss(pitem[0], csss);
	}
}
XLayerOut.prototype.doLayout = function(bgimg) {
	this.bw = bgimg.width;
	this.bh = bgimg.height;
	var rx = this.dw / this.bw;
	var ry = this.dh / this.bh;
	this.rate = rx < ry ? rx : ry;
	// alert(this.bw + ' ' + this.bh);
	this.bw = parseInt(this.rate * this.bw);
	this.bh = parseInt(this.rate * this.bh);
	this.bx = parseInt((this.dw - this.bw) / 2);
	this.by = 0;// parseInt((this.dh - this.bh) / 2);
	if (bgimg.isfack != true) {
		this.setObjectCss(bgimg, {
			"height" : this.bh + 'px',
			'width' : this.bw + 'px',
			'top' : this.by + 'px',
			'left' : this.bx + 'px',
			'position' : 'absolute',
			'display' : 'block'
		});
		var html = '<div style="top:' + this.dh + 'px;left:0px;height:' + (this.dh / 2) + 'px; width:' + this.dw + 'px;position:absolute"></div>';
		$('body').append(html);
	}
	this.doLayoutList(this.plist);
}

myglobal.getClientId = function(params) {
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

myglobal.getClientVersion = function(params) {
	var clientId = myglobal.getClientId(params);
	var strs = clientId.split('_');
	var ver = parseFloat(strs[1]);
	if (isNaN(ver)) {
		return 0;
	}
	return ver;
}