var curPage = 0;
var GDATA = {}
var curPwd = '';
var apiVer = 'open/v1/user/';
var autoActionFlg = 0;
var isAccountsShow = false;
var randomUserAccount = null;
var randomUserPwd = null;
var lastUserAccount = '';
var lastUserPwd = '';

$().ready(function() {
	myglobal.regAction('OnPageInit', OnPageInit);
	var args = {
		module : 'login',
		callback : 'OnPageInit',
		cmd : {
			action : 'PageInit',
			params : {}
		}
	};
	myglobal.jsCallNative(args);
});

function alertInner(title, msg, callback) {
	myglobal.showAlert(title, msg, callback, myglobal.viewWidth, myglobal.viewHeight);
}

function OnPageInit(params, isError, errInfo) {
	if (isError) {
		myglobal.showMessage(myglobal.getLocalMsg('syserr') + ' ' + errInfo);
		return;
	}
	var user = params['user'];
	GDATA['clientId'] = user['clientId'];
	GDATA['appId'] = (user['gameId'] == undefined) ? user['appId'] : user['gameId'];
	GDATA['deviceId'] = user['deviceId'];

	var accounts = user['accounts'];
//	 accounts = [ {
//	 "account" : "uuu1",
//	 "pwd" : "xxxx11"
//	 }, {
//	 "account" : "uuu2",
//	 "pwd" : "xxxx2"
//	 }];
	var ahtmls = [];
	if (accounts) {
		for ( var i = 0; i < accounts.length; i++) {
			var uname = accounts[i]['account'];
			var pwd = accounts[i]['pwd'];
			if (i == 0) {
				lastUserAccount = uname;
				lastUserPwd = pwd;
			}
			ahtmls.push('<a class="test_border accountitem" href="javascript:selectOldAccount(\'' + uname + '\', \'' + pwd + '\')">&nbsp;&nbsp;&nbsp;&nbsp;'
					+ uname + '</a>')
		}
	}
	GDATA['userAccount'] = lastUserAccount;
	GDATA['userPwd'] = $.md5(lastUserPwd);
	$('#userAccount').val(lastUserAccount);
	$('#userPwd').val(lastUserPwd);
	$('#accountlist').html(ahtmls.join(''));

	if (userAccount.length == 0) {
		doRandomUserAccount();
	}
}

myglobal.isPassword = function(idPassword) {
	var pwdReg = /^[\dA-Za-z(!@#$%&)]{6,14}$/;
	var objPwd = $("#" + idPassword);
	var value = objPwd.val();
	if (!pwdReg.test(value)) {
		return false;
	}
	return true;
}

myglobal.isUserAccount = function(idUserAccount) {
	var pwdReg = /^[0-9A-Za-z(@.)]{4,30}$/;
	var objPwd = $("#" + idUserAccount);
	var value = objPwd.val();
	if (!pwdReg.test(value)) {
		return false;
	}
	return true;
}

function doGotoBack() {
	doShowPage(curPage - 1);
}

function doShowRegister() {
	doShowPage(1);
	doRandomUserAccount();
}

//
function doShowPage(pIndex) {
	if (pIndex == 0) {
		$('#divreg').hide();
		$('#userAccount').val(lastUserAccount);
		$('#userPwd').val(lastUserPwd);
		isAccountsShow = false;
		$('#divaccounts').hide();
		$('#divlogin').show();
	}
	if (pIndex == 1) {
		$('#title_win').html('注册途游帐号');
		$('#regUserAccount').val('');
		$('#regUserPwd').val('');
		$('#divlogin').hide();
		isAccountsShow = false;
		$('#divaccounts').hide();
		$('#divreg').show();
		$('.finish').show();
		$('#imgmore').css('background-position', '0 -22px')
	}
	if (pIndex < 0) {
		doCloseWindow();
	}
	curPage = pIndex;
}

function doCloseWindow() {
	var args = {
		module : 'login',
		callback : '',
		cmd : {
			action : 'CloseWindow',
			params : {}
		}
	};
	myglobal.jsCallNative(args);
}

function doShowAccounts() {
	if (isAccountsShow) {
		$('#divaccounts').hide();
		$('#imgmore').css('background-position', '0 -22px')
	} else {
		$('#divaccounts').show();
		$('#imgmore').css('background-position', '0 0')
	}
	isAccountsShow = !isAccountsShow;
}

function selectOldAccount(uname, pwd) {
	$('#userAccount').val(uname);
	$('#userPwd').val(pwd);
	GDATA['userAccount'] = uname;
	GDATA['userPwd'] = pwd;
	doShowAccounts();
}

function doCheckInput(title) {
	var userAccountId = '';
	var passwordId = '';
	if (curPage == 0) {
		userAccountId = 'userAccount';
		passwordId = 'userPwd';
	} else {
		userAccountId = 'regUserAccount';
		passwordId = 'regUserPwd';
	}

	if (!myglobal.isUserAccount(userAccountId)) {
		alertInner(title, '请输入有效的用户ID')
		return false;
	}

	if (!myglobal.isPassword(passwordId)) {
		alertInner(title, '请输入有效的密码')
		return false;
	}
	curPwd = $('#' + passwordId).val();
	GDATA['userAccount'] = $('#' + userAccountId).val().toLowerCase();
	GDATA['userPwd'] = $.md5(curPwd);
	return GDATA
}

function doRandomUserAccount() {
	if (!randomUserAccount) {
		var action = {
			callback : doRandomUserAccountDone,
			method : apiVer + 'randomAccount'
		};
		myglobal.doRequest(action);
		$('#regUserAccount').attr('placeholder', '正在取得缺省账户，请稍后...')
		$('#regUserPwd').attr('placeholder', '')
	} else {
		setRandomAccount();
	}
}

function doRandomUserAccountDone(data, action) {
	if (data == null) {
		return;
	}
	var result = data['result'] ? data['result'] : {};
	var rAccount = result['account'];
	var rPwd = result['pwd'];
	if (rAccount && rPwd) {
		randomUserAccount = rAccount;
		randomUserPwd = rPwd;
		setRandomAccount();
	}
}

// 绑定输入框提示文字
function setRandomAccount() {
	$('#regUserAccount').val(randomUserAccount);
	$('#regUserPwd').val(randomUserPwd);
	$('#regUserAccount').attr('placeholder', '请输入有效帐号')
	$('#regUserPwd').attr('placeholder', '限6-12个字母数字')
}

function doLoginName() {
	params = doCheckInput('进入游戏');
	if (params == false) {
		return;
	}
	var action = {
		callback : doLoginNameDone,
		method : apiVer + 'loginByAccount',
		params : params
	};
	myglobal.doRequest(action);
}

function doLoginEmail() {
	params = doCheckInput('进入游戏');
	if (params == false) {
		return;
	}
	var action = {
		callback : doLoginNameDone,
		method : apiVer + 'loginByEmail',
		params : params
	};
	myglobal.doRequest(action);
}

function doRegister() {
	params = doCheckInput('完成注册');
	if (params == false) {
		return;
	}
	var action = {
		callback : doLoginNameDone,
		method : apiVer + 'registerByAccount',
		params : params
	};
	myglobal.doRequest(action);
}

function doRegisterEmail() {
	params = doCheckInput('完成注册');
	if (params == false) {
		return;
	}
	var action = {
		callback : doLoginNameDone,
		method : apiVer + 'registerByEmail',
		params : params
	};
	myglobal.doRequest(action);
}

function doLoginNameDone(data, action) {
	if (data == null) {
		return;
	}
	var result = data['result'] ? data['result'] : {};
	var code = (data['error'] == undefined) ? 0 : data['error']['code'];
	if (code == 1) {
		alertInner('进入游戏', '登录参数错误');
		return;
	}
	if (code == 2) {
		alertInner('进入游戏', 'SNS登录参数错误');
		return;
	}
	if (code == 3) {
		alertInner('进入游戏', '用户名密码错误');
		return;
	}
	if (code < 0) {
		alertInner('进入游戏', '系统错误');
		return;
	}

	data['result']['action'] = 'doLogin';
        data['result']['account'] = GDATA['userAccount'];
        data['result']['password'] = curPwd;
	data['result']['authInfo'] = JSON.stringify({
		'authcode' : result['authorCode'],
		'uid' : result['userId']
	});
	var args = {
		module : 'login',
		callback : '',
		cmd : {
			action : 'LoginDone',
			params : {
				user : data
			}
		}
	};
	myglobal.jsCallNative(args);
}

function doLoginOther360() {
	var args = {
		module : 'login',
		callback : '',
		cmd : {
			action : 'LoginOther',
			params : {
				type : '360'
			}
		}
	};
	myglobal.jsCallNative(args);
}
