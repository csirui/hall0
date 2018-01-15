# -*- coding=utf-8 -*-

class TuyouPayRequestConf(object):
    REQUEST_DATA = {
        '360.ali': 'tysdk.entity.paythird.pay360.TuYouPay360.doPayRequestAli',
        '360.card.dx': 'tysdk.entity.paythird.pay360.TuYouPay360.doPayRequestCardDx',
        '360.card.yd': 'tysdk.entity.paythird.pay360.TuYouPay360.doPayRequestCardYd',
        '360.card.lt': 'tysdk.entity.paythird.pay360.TuYouPay360.doPayRequestCardLt',
        'tuyou.ali': 'tysdk.entity.paythird.paytuyou_ali.TuyouPayTuyouAli.doPayRequestAli',
        'tuyou.card.dx': 'tysdk.entity.paythird.paytuyou_card.TuyouPayTuyouCard.doPayRequestCardDx',
        'tuyou.card.yd': 'tysdk.entity.paythird.paytuyou_card.TuyouPayTuyouCard.doPayRequestCardYd',
        'tuyou.card.lt': 'tysdk.entity.paythird.paytuyou_card.TuyouPayTuyouCard.doPayRequestCardLt',
        'yee2.card1': 'tysdk.entity.paythird.payyee2.TuYouPayYee2.doPayRequestCard1',
        'yee2.card2': 'tysdk.entity.paythird.payyee2.TuYouPayYee2.doPayRequestCard2',
        'palm.card': 'tysdk.entity.paythird.paypalm.TuYouPayPalm.doPayRequestCard',

        #         'tuyou.caifutong'       : 'tysdk.entity.paythird.paytuyou_card.TuyouPayTuyou.doPayRequestCaiFuTong',
        #        'tuyou.msgyd'           : 'tysdk.entity.paythird.paymsgyd.TuYouPayMsgYd.doMsgYdRequest',
        'yee.card': 'tysdk.entity.paythird.payyee.TuYouPayYee.doPayRequestCard',
        'wxpay': 'tysdk.entity.paythird.paywx.TuYouPayWXpay.doPayRequestWx',
        'h5.youku': 'tysdk.entity.paythird.payyoukuh5.TuYouPayYouKuH5.doPayRequest',

        'shediao.ali': 'tysdk.entity.paythird.payshediao_ali.TuyouPayShediaoAli.doPayRequestAli',
        'shediao.card.dx': 'tysdk.entity.paythird.payshediao_card.TuyouPayShediaoCard.doPayRequestCardDx',
        'shediao.card.yd': 'tysdk.entity.paythird.payshediao_card.TuyouPayShediaoCard.doPayRequestCardYd',
        'shediao.card.lt': 'tysdk.entity.paythird.payshediao_card.TuyouPayShediaoCard.doPayRequestCardLt',
        'shediao.yee.card': 'tysdk.entity.paythird.payyee.TuYouPayYee.doPayRequestCard',
    }
