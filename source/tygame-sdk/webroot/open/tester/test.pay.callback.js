var testPayCallbackUrls = {
	'xiaomi' : [ 'v1/pay/xiaomi/callback', {
		appId : '12724',
		cpOrderId : 'PO20130529173052238',
		cpUserInfo : '不使用',
		orderId : '21136981985313661922',
		orderStatus : 'TRADE_SUCCESS',
		payFee : '200',
		payTime : '2013-05-29 17:30:54',
		productCode : '01',
		productCount : '2',
		productName : '途游币',
		uid : '192164',
		signature : '46a5f91a9e0a90342f1f3733e937395c412dcf0b'
	} ],
	'360' : [ 'v1/pay/360/callback', {
		mer_trade_code : '3ed16f18-aae9-45f9-ae58-2df2a4034fe3',
		input_cha : 'UTF-8',
		bank_pay_flag : 'failed:81007:无效的卡号密码',
		mer_code : '3337100050',
		gateway_trade_code : '1AA0000A94CA8',
		rec_amount : '10',
		inner_trade_code : '0830120419121239820',
		sign : '4c2ea11a263c9ec2ef9f545b85ec4186',
		sign_type : 'MD5',
		product_name : '360Coin'
	} ],
	'ali' : [
			'v1/pay/alipay/callback',
			{
				notify_data : '<notify>' + '<trade_status>TRADE_FINISHED</trade_status><total_fee>1000.9</total_fee>'
						+ '<subject>羽毛球拍</subject><out_trade_no>PO201303181945001</out_trade_no>'
						+ '<notify_reg_time>2012-11-18 14:02:43.000</notify_reg_time>' + '<trade_no>2010111800209965</trade_no></notify>',
				sign : 'ZPZULntRpJwFmGNIVKwjLEF2Tze7bqs60rxQ22CqT5J1UlvGo575QK9z/+p+7E9cO'
						+ 'oRoWzqR6xHZ6WVv3dloyGKDR0btvrdqPgUAoeaX/YOWzTh00vwcQ+HBtXE+vPTfAqjCTxiiSJEOY7ATCF1q7iP3sfQxhS0nDUug1LP3OLk:'
			} ],
	'msg.dx' : [ 'v1/pay/mh/callback', {
		Prim : 'qX/+kB8fHEam4s8eOu/giYvrI8/YxAS9/ymGl5cZ+TI:',
		ID : '679F2D36803048498CD71A0D1DC576C5'
	} ],
	'msg.yd' : [ 'v1/pay/yd/callback', {
		Prim : 'qX/+kB8fHEam4s8eOu/giYvrI8/YxAS9/ymGl5cZ+TI:',
		ID : '679F2D36803048498CD71A0D1DC576C5'
	} ],
	'caifutong' : [ '/v1/pay/caifutong/callback', {} ],
	'shenzhoufu' : [ '/v1/pay/card/callback', {} ],
	'ios' : [
			'v1/pay/ios/callback',
			{
				appId : '10003',
				// receipt :
				// 'ewoJIm9yaWdpbmFsLXB1cmNoYXNlLWRhdGUtcHN0IiA9ICIyMDEzLTA5LTEzIDAxOjI4OjQwIEFtZXJpY2EvTG9zX0FuZ2VsZXMiOwoJInVuaXF1ZS1pZGVudGlmaWVyIiA9ICJkOTQ1MmQ2YzI2MzJkMzcxNGEzZDMzOTVlM2MzMjRlODYxMTA1NDkxIjsKCSJvcmlnaW5hbC10cmFuc2FjdGlvbi1pZCIgPSAiMTAwMDAwMDA4NzE1MzE2MCI7CgkiYnZycyIgPSAiMS4wIjsKCSJ0cmFuc2FjdGlvbi1pZCIgPSAiMTAwMDAwMDA4NzE1MzE2MCI7CgkicXVhbnRpdHkiID0gIjEiOwoJIm9yaWdpbmFsLXB1cmNoYXNlLWRhdGUtbXMiID0gIjEzNzkwNjA5MjAwMDAiOwoJInVuaXF1ZS12ZW5kb3ItaWRlbnRpZmllciIgPSAiRDMzNzdFMzktNTlBNi00MERCLThDOTUtOUJFOEI3RTdBODMzIjsKCSJwcm9kdWN0LWlkIiA9ICIxMDAwMzAwNCI7CgkiaXRlbS1pZCIgPSAiNzA0MjU0ODg0IjsKCSJiaWQiID0gImNvbS5zaGVkaWFvLnhpeW91IjsKCSJwdXJjaGFzZS1kYXRlLW1zIiA9ICIxMzc5MDYwOTIwMDAwIjsKCSJwdXJjaGFzZS1kYXRlIiA9ICIyMDEzLTA5LTEzIDA4OjI4OjQwIEV0Yy9HTVQiOwoJInB1cmNoYXNlLWRhdGUtcHN0IiA9ICIyMDEzLTA5LTEzIDAxOjI4OjQwIEFtZXJpY2EvTG9zX0FuZ2VsZXMiOwoJIm9yaWdpbmFsLXB1cmNoYXNlLWRhdGUiID0gIjIwMTMtMDktMTMgMDg6Mjg6NDAgRXRjL0dNVCI7Cn0=',
				receipt : 'ewoJInNpZ25hdHVyZSIgPSAiQWtOZ095ZXdFTzg4RncvQXVLMUl1bnBLR1hkNEw1eXV3bXV3cFFRdWRSemEzODlQTWc2SDVHWU5ZRXkzc0EweTVFQVhQOVJoYWlOUTlMQnNyR2pzVkd1enNoY0llQWtiQVhJcnVzVmhoMGduMFJoZ3FoQ1pqTUNrdnhwSkNreXFBMmUwaVZUMGwrTklTaUlGU2E3NnJVU2dFYTVINlp2dmxSVjI3TWNtc1BBUEFBQURWekNDQTFNd2dnSTdvQU1DQVFJQ0NHVVVrVTNaV0FTMU1BMEdDU3FHU0liM0RRRUJCUVVBTUg4eEN6QUpCZ05WQkFZVEFsVlRNUk13RVFZRFZRUUtEQXBCY0hCc1pTQkpibU11TVNZd0pBWURWUVFMREIxQmNIQnNaU0JEWlhKMGFXWnBZMkYwYVc5dUlFRjFkR2h2Y21sMGVURXpNREVHQTFVRUF3d3FRWEJ3YkdVZ2FWUjFibVZ6SUZOMGIzSmxJRU5sY25ScFptbGpZWFJwYjI0Z1FYVjBhRzl5YVhSNU1CNFhEVEE1TURZeE5USXlNRFUxTmxvWERURTBNRFl4TkRJeU1EVTFObG93WkRFak1DRUdBMVVFQXd3YVVIVnlZMmhoYzJWU1pXTmxhWEIwUTJWeWRHbG1hV05oZEdVeEd6QVpCZ05WQkFzTUVrRndjR3hsSUdsVWRXNWxjeUJUZEc5eVpURVRNQkVHQTFVRUNnd0tRWEJ3YkdVZ1NXNWpMakVMTUFrR0ExVUVCaE1DVlZNd2daOHdEUVlKS29aSWh2Y05BUUVCQlFBRGdZMEFNSUdKQW9HQkFNclJqRjJjdDRJclNkaVRDaGFJMGc4cHd2L2NtSHM4cC9Sd1YvcnQvOTFYS1ZoTmw0WElCaW1LalFRTmZnSHNEczZ5anUrK0RyS0pFN3VLc3BoTWRkS1lmRkU1ckdYc0FkQkVqQndSSXhleFRldngzSExFRkdBdDFtb0t4NTA5ZGh4dGlJZERnSnYyWWFWczQ5QjB1SnZOZHk2U01xTk5MSHNETHpEUzlvWkhBZ01CQUFHamNqQndNQXdHQTFVZEV3RUIvd1FDTUFBd0h3WURWUjBqQkJnd0ZvQVVOaDNvNHAyQzBnRVl0VEpyRHRkREM1RllRem93RGdZRFZSMFBBUUgvQkFRREFnZUFNQjBHQTFVZERnUVdCQlNwZzRQeUdVakZQaEpYQ0JUTXphTittVjhrOVRBUUJnb3Foa2lHOTJOa0JnVUJCQUlGQURBTkJna3Foa2lHOXcwQkFRVUZBQU9DQVFFQUVhU2JQanRtTjRDL0lCM1FFcEszMlJ4YWNDRFhkVlhBZVZSZVM1RmFaeGMrdDg4cFFQOTNCaUF4dmRXLzNlVFNNR1k1RmJlQVlMM2V0cVA1Z204d3JGb2pYMGlreVZSU3RRKy9BUTBLRWp0cUIwN2tMczlRVWU4Y3pSOFVHZmRNMUV1bVYvVWd2RGQ0TndOWXhMUU1nNFdUUWZna1FRVnk4R1had1ZIZ2JFL1VDNlk3MDUzcEdYQms1MU5QTTN3b3hoZDNnU1JMdlhqK2xvSHNTdGNURXFlOXBCRHBtRzUrc2s0dHcrR0szR01lRU41LytlMVFUOW5wL0tsMW5qK2FCdzdDMHhzeTBiRm5hQWQxY1NTNnhkb3J5L0NVdk02Z3RLc21uT09kcVRlc2JwMGJzOHNuNldxczBDOWRnY3hSSHVPTVoydG04bnBMVW03YXJnT1N6UT09IjsKCSJwdXJjaGFzZS1pbmZvIiA9ICJld29KSW05eWFXZHBibUZzTFhCMWNtTm9ZWE5sTFdSaGRHVXRjSE4wSWlBOUlDSXlNREV6TFRBNUxURXpJREEwT2pNME9qTTFJRUZ0WlhKcFkyRXZURzl6WDBGdVoyVnNaWE1pT3dvSkluVnVhWEYxWlMxcFpHVnVkR2xtYVdWeUlpQTlJQ0prT1RRMU1tUTJZekkyTXpKa016Y3hOR0V6WkRNek9UVmxNMk16TWpSbE9EWXhNVEExTkRreElqc0tDU0p2Y21sbmFXNWhiQzEwY21GdWMyRmpkR2x2YmkxcFpDSWdQU0FpTVRBd01EQXdNREE0TnpFNE5ETTRPU0k3Q2draVluWnljeUlnUFNBaU1TNHdJanNLQ1NKMGNtRnVjMkZqZEdsdmJpMXBaQ0lnUFNBaU1UQXdNREF3TURBNE56RTRORE00T1NJN0Nna2ljWFZoYm5ScGRIa2lJRDBnSWpFaU93b0pJbTl5YVdkcGJtRnNMWEIxY21Ob1lYTmxMV1JoZEdVdGJYTWlJRDBnSWpFek56a3dOekl3TnpVNE56RWlPd29KSW5WdWFYRjFaUzEyWlc1a2IzSXRhV1JsYm5ScFptbGxjaUlnUFNBaVFrRXlOamxFUVRNdFJFUkNNUzAwTjBSQ0xVRTROVGN0UkVFeU5qYzNRamMwUXpneUlqc0tDU0p3Y205a2RXTjBMV2xrSWlBOUlDSXhNREF3TXpBd015STdDZ2tpYVhSbGJTMXBaQ0lnUFNBaU56QTBNalV4T0RnNUlqc0tDU0ppYVdRaUlEMGdJbU52YlM1emFHVmthV0Z2TG5ocGVXOTFJanNLQ1NKd2RYSmphR0Z6WlMxa1lYUmxMVzF6SWlBOUlDSXhNemM1TURjeU1EYzFPRGN4SWpzS0NTSndkWEpqYUdGelpTMWtZWFJsSWlBOUlDSXlNREV6TFRBNUxURXpJREV4T2pNME9qTTFJRVYwWXk5SFRWUWlPd29KSW5CMWNtTm9ZWE5sTFdSaGRHVXRjSE4wSWlBOUlDSXlNREV6TFRBNUxURXpJREEwT2pNME9qTTFJRUZ0WlhKcFkyRXZURzl6WDBGdVoyVnNaWE1pT3dvSkltOXlhV2RwYm1Gc0xYQjFjbU5vWVhObExXUmhkR1VpSUQwZ0lqSXdNVE10TURrdE1UTWdNVEU2TXpRNk16VWdSWFJqTDBkTlZDSTdDbjA9IjsKCSJlbnZpcm9ubWVudCIgPSAiU2FuZGJveCI7CgkicG9kIiA9ICIxMDAiOwoJInNpZ25pbmctc3RhdHVzIiA9ICIwIjsKfQ==',
				clientId : 'Android_2.07_ios',
				appInfo : 'XXXXXXXXXXXX'
			} ],
	'lenovo' : [
			'v1/pay/lenovo/callback',
			{
				transdata : '{"exorderno":"1","transid":"2","appid":"20017200000001200172","waresid":31,"feetype":4,"money":5,"count":6,"result":0,"transtype":0,"transtime":"2012-12-12 12:11:10","cpprivate":"7"}',
				sign : 'd91cbc584316b9d99919921a9',
				clientId : 'Android_2.07_ios',
				appInfo : 'XXXXXXXXXXXX'
			} ],
	'wandoujia' : [
			'v1/pay/wandoujia/callback',
			{
				content : '{"out_trade_no":"1","appKeyId":"100000293","money":5,"count":6}',
				sign : 'd91cbc584316b9d99919921a9',
				clientId : 'Android_2.07_ios',
				appInfo : 'XXXXXXXXXXXX'
			} ],
}

function doPayCallBack(payTag) {
	var data = testPayCallbackUrls[payTag];
	var url = myglobal.domain + data[0];
	log('===============' + payTag + '================================');
	log('url-->' + url + ' params=' + JSON.stringify(data[1]));
	var errorFun = function(jqXHR, textStatus, errorThrown) {
		log('doPayCallBack response error->' + errorThrown);
	};
	var successFun = function(data, textStatus, jqXHR) {
		hlog('doPayCallBack response ok->' + data);
	};
	data[1]['authInfo'] = NativeJava.user['authInfo'];
	var ajaxPro = {
		dataType : 'html',
		cache : false,
		type : 'POST',
		url : url,
		error : errorFun,
		success : successFun,
		data : data[1]
	};
	$.ajax(ajaxPro);
}
