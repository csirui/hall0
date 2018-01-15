var NativeJava = new Object();

NativeJava.cache = {};
NativeJava.lastOpenArgs = {};
NativeJava.appId = 6;
NativeJava.clientId = 6;
NativeJava.deviceId = 6;
NativeJava.user = {};

NativeJava.init = function(screenId, dialogId, userIdId) {
	NativeJava.screenId = screenId;
	NativeJava.dialogId = dialogId;
	NativeJava.userIdId = userIdId;
}

NativeJava.reset = function(appId, clientId, deviceId) {
	NativeJava.appId = appId;
	NativeJava.clientId = clientId;
	NativeJava.deviceId = deviceId;
	NativeJava.cache = {};
	NativeJava.lastOpenArgs = {};
	NativeJava.resetWindow();
	NativeJava.resetDialog();
	NativeJava.user = {};
	$('#' + NativeJava.userIdId).val('');
}

NativeJava.resetWindow = function() {
	mscreen = $('#' + NativeJava.screenId);
	mscreen.attr('src', '');
	$('#' + NativeJava.screenId + '_close').hide();
}

NativeJava.resetDialog = function() {
	mdialog = $('#' + NativeJava.dialogId);
	mdialog.hide();
	mdialog.attr('src', '');
	$('#' + NativeJava.dialogId + '_close').hide();
}

NativeJava.callJs = function(args) {
	var isDialogShow = $('#' + NativeJava.dialogId).is(":visible");
	var mid = NativeJava.screenId;
	if (isDialogShow == true) {
		mid = NativeJava.dialogId;
	}
	var mframe = document.getElementById(mid);
	mframe.contentWindow.myglobal.nativeCallJs(args);
}

NativeJava.iframeLoaded = function(iframeEl) {
	var callback = function() {
		iframeEl.contentWindow._javascript_4_java_ = NativeJava
	}
//    setTimeout(callback,18)

//    $(iframeEl).ready(function(){
//        callback()
//        iframeEl.contentWindow.name='jack'
//        alert(iframeEl.contentWindow+'--'+iframeEl.contentWindow._javascript_4_java_+'--'+iframeEl.contentWindow.name)
//    })
    iframeEl.contentWindow.name='NativeJavaTest'
	if (iframeEl.attachEvent) {
		iframeEl.attachEvent("onload", function() {
			callback();
		});
	} else {
		iframeEl.onload = function() {
			callback();
		}
	}
}

NativeJava.checkStr = function(datas, key) {
	var val = datas[key];
	if (val) {
		val = $.trim('' + val);
	} else {
		val = '';
	}
	datas[key] = val;
	return val;
}

NativeJava.exec = function(args) {
	log('js call native args-->' + args);
	var datas = JSON.parse(args);
	NativeJava.checkStr(datas, 'modeule');
	var callback = NativeJava.checkStr(datas, 'callback');
	var cmd = datas['cmd'];
	var action = NativeJava.checkStr(cmd, 'action');
	var params = cmd['params'];
	fun = NativeJava[action];
	if (typeof (fun) == 'function') {
		var rets = fun(datas);
		var rparams = JSON.stringify(rets);
		log('action->[' + action + '] callback=[' + callback + '] return->'
				+ rparams);
		if (callback != '') {
			NativeJava.callJs(rparams);
		}
	} else {
		alert('NativeJava.exec [' + action + '] not defined !');
	}
}

NativeJava.OpenWindow = function(datas) {
	var params = datas['cmd']['params'];
	var style = params['style'];
	var url = NativeJava.checkStr(params, 'url');
	var html = NativeJava.checkStr(params, 'html');
	var args = params['args'];

	NativeJava.lastOpenArgs = args;
	var iframeId = '';
	if (style == 0) {
		iframeId = NativeJava.screenId;
	} else if (style == 1) {
		iframeId = NativeJava.screenId;
	} else if (style == 2) {
		iframeId = NativeJava.dialogId;
	} else if (style == 3) {
		iframeId = NativeJava.dialogId;
	} else {
		alert('Error, OpenWindow the style not in (0, 1, 2)');
		return;
	}

	var mscreenj = $('#' + iframeId)
	var mscreend = document.getElementById(iframeId);

	mscreenj.show();
	if (url.length > 0) {
		log('open url of ->' + url);
		mscreenj.attr('src', url);
	} else {
		log('open url of html ->' + html);
		mdoc = mscreend.contentDocument;
		mdoc.open();
		mdoc.write(html);
		mdoc.close();
	}
	NativeJava.iframeLoaded(mscreend);

	if (style == 1 || style == 3) {
		$('#' + iframeId + '_close').hide();
	} else {
		$('#' + iframeId + '_close').show();
	}

	if (style == 0 || style == 1) {
		NativeJava.resetDialog();
	}
}

NativeJava.CloseWindow = function(datas) {
	var isDialogShow = $('#' + NativeJava.dialogId).is(":visible");
	if (isDialogShow == true) {
		NativeJava.resetDialog();
	} else {
		NativeJava.resetWindow();
	}
}

NativeJava.PageInit = function(datas) {
	if (NativeJava.user['deviceId'] == undefined) {
		NativeJava.user['appId'] = NativeJava.appId;
		NativeJava.user['clientId'] = NativeJava.clientId;
		NativeJava.user['deviceId'] = NativeJava.deviceId;
	}

	var rets = {
		modeule : datas['modeule'],
		callback : '',
		cmd : {
			action : datas['callback'],
			params : {
				user : NativeJava.user,
				args : NativeJava.lastOpenArgs,
				cache : {},
				simonly : 'true',
				simpay : 'true',
				clientId : NativeJava.clientId
			}
		}
	};
	NativeJava.lastOpenArgs = {}

	var ckeys = datas['cmd']['params']['cache'];
	if (ckeys) {
		for ( var i in ckeys) {
			key = ckeys[i]
			rets['cmd']['params']['cache'][key] = NativeJava.cache[key];
		}
	}
	return rets;
}

NativeJava.SetCache = function(datas) {
	var caches = datas['cmd']['params'];
	if (caches) {
		$.each(caches, function(key, value) {
			NativeJava.cache[key] = value;
		});
	}
}

NativeJava.LoginDone = function(datas) {
	log('User Login Done -> ' + JSON.stringify(datas));
	var result = datas['cmd']['params']['user']['result'];
	NativeJava.user = {}
	NativeJava.user['userId'] = result['userId'];
	NativeJava.user['udata'] = result['udata'];
	NativeJava.user['gameId'] = NativeJava.appId;
	NativeJava.user['clientId'] = NativeJava.clientId;
	NativeJava.user['deviceId'] = NativeJava.deviceId;
	NativeJava.user['authInfo'] = JSON.stringify({
		'authcode' : result['authorCode'],
		'account' : result['userEmail'],
		'uid' : result['userId']
	});
	NativeJava._GetUserInfo();
	NativeJava.CloseWindow();
}

NativeJava._GetUserInfo = function() {
	var action = {
		callback : NativeJava._GetUserInfoDone,
		method : myglobal.JSONAPIVER + 'getuserinfo',
		params : {
			authInfo : NativeJava.user['authInfo'],
			udata : NativeJava.user['udata'],
			gameId : NativeJava.user['gameId'],
			clientId : NativeJava.user['clientId']
		}
	};
	myglobal.doRequest(action);
}

NativeJava._GetUserInfoDone = function(data, action) {
	if (data != null) {
		result = data['result'];
		var code = result['code'];
		if (code == 0) {
			NativeJava.user['info'] = result;
			NativeJava.user['gdata'] = result['gdata'];
			NativeJava.user['udata'] = result['udata'];
			log('doGetUserInfoDone user->' + JSON.stringify(NativeJava.user));
			$('#' + NativeJava.userIdId).val(NativeJava.user['userId']);
		} else {
			alert('Error, ' + action.method + '\n' + JSON.stringify(data));
		}
	}
}

NativeJava.LoginOther = function(datas) {
	var type = datas['cmd']['params']['type'];
	NativeJava.CloseWindow();
	alert('客户端调用其他平台的Login SDK ！！');
}

NativeJava.IsInstall = function(datas) {
	var apps = datas['cmd']['params']['apps'];
	var installs = [];
	for ( var i = 0; i < apps.length; i++) {
		var isi = ((i % 2) == 0 ? true : false);
		var app = {};
		app[apps[i]] = isi;
		installs.push(app);
	}

	var rets = {
		modeule : datas['modeule'],
		callback : '',
		cmd : {
			action : datas['callback'],
			params : {
				apps : installs
			}
		}
	};
	return rets;
}

NativeJava.DownApp = function(datas) {
	var url = datas['cmd']['params']['url'];
	alert('下载应用：' + url);
}

NativeJava.OpenApp = function(datas) {
	var app = datas['cmd']['params']['app'];
	alert('打开本地应用：' + app);
}

NativeJava.doPageShow = function(datas) {
}

NativeJava.Quit = function(datas) {
}

NativeJava.UpUserInfo = function(datas) {
}

NativeJava.PayOrder = function(datas) {
}

NativeJava.RoomListInit = function(datas) {
	var rets = {
		modeule : datas['modeule'],
		callback : '',
		cmd : {
			action : 'OnRoomChanged',
			params : 1
		}
	};
	return rets;
}
