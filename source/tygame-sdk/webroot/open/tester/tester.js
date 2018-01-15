var testUrls = {
	901 : [ 1, 'open/s1/login/login.html' ], // 切换账号
	902 : [ 1, 'open/s1/pay/pay.html' ], // 支付
	2 : [ 1, 'dizhu/roomlist2.html' ], // 房间列表
	3 : [ 0, 'dizhu/wallet.html' ], // 钱袋
	4 : [ 0, 'dizhu/cross.html' ], // 交叉推广
	5 : [ 0, 'dizhu/task.html' ], // 任务
	6 : [ 0, 'dizhu/message.html' ], // 消息
	7 : [ 0, 'dizhu/shop.html' ], // 商城
	8 : [ 0, 'dizhu/bigprize.html' ], // 大奖
	9 : [ 0, 'dizhu/activity.html' ], // 活动
	10 : [ 0, 'dizhu/help.html' ], // 帮助
	11 : [ 0, 'dizhu/feedback.html' ], // 反馈
	12 : [
			2,
			'dizhu/dlg_loseneedbuy.html?'
					+ 'itemId=T20K&buyDesc=记牌器1天使用权&buyPic=T20K.png'
					+ '&buyName=20000金币&buyPrice=2' ], // 输光了购买
	13 : [ 2, 'dizhu/dlg_benefits.html?maxCount=3&sendCount=1&sendChip=1000' ], // 救济金领取
	14 : [ 2, 'dizhu/dlg_roomneedbuy.html?mycoin=52620&mincoin=200000&simpay=0' ], // 高级场购买
	15 : [ 2, 'dizhu/dlg_quit.html' ], // 退出游戏
	16 : [ 2, 'dizhu/dlg_toomuchcoin.html?roomId=602' ], // 高倍场引导
	17 : [ 3, 'dizhu/raffle.html' ], // 抽奖
	18 : [ 0, 'dizhu/rank.html' ], // 排行榜
	19 : [ 3, 'dizhu/public.html' ], // 公告
	20 : [ 3, 'dizhu/coupon.html' ], // 兑换券规则

	102 : [ 1, 't3card/roomlist.html' ], // 房间列表
	104 : [ 0, 't3card/cross.html' ], // 交叉推广
	105 : [ 0, 't3card/task.html' ], // 任务
	106 : [ 0, 't3card/message.html' ], // 消息
	107 : [ 0, 't3card/shop.html' ], // 商城
	108 : [ 0, 't3card/bigprize.html' ], // 大奖
	109 : [ 0, 't3card/activity.html' ], // 活动
	110 : [ 0, 't3card/help.html' ], // 帮助
	111 : [ 0, 't3card/feedback.html' ], // 反馈
	112 : [
			2,
			't3card/dlg_loseneedbuy.html?'
					+ 'itemId=T20K&buyDesc=记牌器1天使用权&buyPic=T20K.png'
					+ '&buyName=20000金币&buyPrice=2' ], // 输光了购买
	113 : [ 2, 't3card/dlg_benefits.html?maxCount=3&sendCount=1&sendChip=1000' ], // 救济金领取
	114 : [ 2,
			't3card/dlg_roomneedbuy.html?mycoin=52620&mincoin=200000&simpay=0' ], // 高级场购买
	115 : [ 2, 't3card/dlg_quit.html' ], // 退出游戏
	116 : [ 2, 't3card/dlg_toomuchcoin.html?roomId=602' ], // 高倍场引导
	117 : [ 3, 't3card/raffle.html' ], // 抽奖
	118 : [ 0, 't3card/rank.html' ], // 排行榜
	119 : [ 3, 't3card/public.html' ], // 公告
	120 : [ 3, 't3card/coupon.html' ], // 兑换券规则
    121 : [ 0, 't3card/friends.html' ], // 兑换券规则
	99 : []
}

function showManager() {
	window.open('/manager/manager.html', 'tuyou-manager');
}

function showWebPage(style, url) {
    if (url) {
        url = myglobal.domain + url;
        var datas = {
            modeule : 'common',
            callback : '',
            cmd : {
                action : 'OpenWindow',
                params : {
                    style : style,
                    url : url,
                    args : {}
                }
            }
        };
        NativeJava.OpenWindow(datas);
    } else {
        alert('测试代码错误');
    }
}

function showPage(index) {
	var list = testUrls['' + index];
	if (list) {
		var style = list[0];
		var url = myglobal.domain + list[1];
		var datas = {
			modeule : 'common',
			callback : '',
			cmd : {
				action : 'OpenWindow',
				params : {
					style : style,
					url : url,
					args : {}
				}
			}
		};

		if (index == 902) { // 支付
			datas.cmd.params.args['orderName'] = '记牌器';
			datas.cmd.params.args['orderId'] = 'GO00001';
			datas.cmd.params.args['orderDesc'] = '记牌器永久使用';
			datas.cmd.params.args['orderPicUrl'] = 'jipaiqi.png';
			datas.cmd.params.args['payChannel'] = undefined;
			datas.cmd.params.args['orderPrice'] = 10;
			datas.cmd.params.args['phonenum'] = '15313923896';
		}
		NativeJava.OpenWindow(datas);
	} else {
		alert('测试代码错误');
	}
}
