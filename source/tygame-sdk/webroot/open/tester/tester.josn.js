var jsonTestActions = {
	1 : [ 'userFriendInfo', {} ], // 我的好友信息
	2 : [ 'userFriendAdd', {
		'friend' : 10001,
		'giftId' : 'GIFT2',
		'sendCount' : 1
	} ], // 添加好友
	3 : [ 'userFriendDel', {
		'friend' : 10001
	} ], // 删除好友
	4 : [ 'userSendGift', {
		'friend' : 10001,
		'giftId' : 'GIFT2',
		'sendCount' : 2
	} ], // 赠送礼物
	5 : [ 'userPawnGift', {
		'giftId' : 'GIFT1',
		'pawnCount' : 2
	} ], // 典当礼物
	6 : [ 't3card/turntableInfo', {} ], // 转盘信息
	7 : [ 't3card/turntable', {} ], // 大转盘
	999 : []
}

function doJsonTest(index) {
	var actionDef = jsonTestActions[index];
	var params = actionDef[1];
	params['authInfo'] = NativeJava.user['authInfo'];
	params['gameId'] = NativeJava.user['gameId'];
	var action = {
		callback : doJsonTestDone,
		method : myglobal.JSONAPIVER + actionDef[0],
		params : params
	};
	myglobal.doRequest(action);
}

function doJsonTestDone(datas, action, ret) {
	log('doJsonTest->ret=' + ret + ' datas=' + JSON.stringify(datas));
}
