var user = {}

function doLogin() {
	$('#muserid').val('');
	var deviceId = $('#mdeviceid').val();
	var clientId = $('#mclientid').val();
	var appId = $('#mgameid').val();
	var action = {
		callback : doLoginDone,
		method : myglobal.JSONAPIVER + 'loginByDevId',
		params : {
			deviceId : deviceId,
			clientId : clientId,
			appId : appId
		}
	};
	myglobal.doRequest(action);
}

function doLoginDone(data, action) {
	if (data != null) {
		result = data['result']
		var code = result['code']
		if (code == 0) {
			user = {}
			user['userId'] = result['userId'];
			user['clientId'] = action['params']['clientId'];
			user['deviceId'] = action['params']['deviceId'];
			user['gameId'] = action['params']['appId'];
			user['authInfo'] = JSON.stringify({
				'authcode' : result['authorCode'],
				'account' : result['userEmail'],
				'uid' : result['userId']
			});
			doGetUserInfo();
		} else {
			alert('Error, ' + action.method + '\n' + JSON.stringify(data));
		}
	}
}

function doGetUserInfo() {
	var action = {
		callback : doGetUserInfoDone,
		method : myglobal.JSONAPIVER + 'getuserinfo',
		params : {
			authInfo : user['authInfo'],
			gameId : user['gameId'],
			clientId : user['clientId']
		}
	};
	myglobal.doRequest(action);
}

function doGetUserInfoDone(data, action) {
	if (data != null) {
		result = data['result']
		var code = result['code']
		if (code == 0) {
			user['info'] = result;
            user['gdata'] = result['gdata'];
			log('doGetUserInfoDone->' + JSON.stringify(user));
			$('#muserid').val('userId=' + user['userId']);
		} else {
			alert('Error, ' + action.method + '\n' + JSON.stringify(data));
		}
	}
}
