# -*- coding=utf-8 -*-

class PayConst():
    CHARGE_STATE_BEGIN = 0  # 初始的状态，开始进行交易
    CHARGE_STATE_CLIENT_PAY_DONE = 5  # 用户客户端充值动作完成
    CHARGE_STATE_REQUEST = 10  # 进行了REQUEST请求， 轮训
    CHARGE_STATE_REQUEST_RETRY = 11  # 需要用户重新输入，并再次请求，弹框
    CHARGE_STATE_REQUEST_IGNORE = 12  # 需要用户重新输入，并再次请求，弹框
    CHARGE_STATE_CALLBACK_OK = 20  # 第三方callback通知，充值成功， 轮训
    CHARGE_STATE_CONSUME = 30  # 开始进行附带的消费， 轮训

    CHARGE_STATE_DONE = 40  # 单纯的充值操作完毕， 结束状态，成功
    CHARGE_STATE_DONE_CONSUME = 41  # 带有消费的充值操作完毕， 结束状态，成功

    CHARGE_STATE_ERROR_CONSUME = 42  # 带有消费的充值操作成功,但是消费购买道具失败， 结束状态，失败
    CHARGE_STATE_ERROR_REQUEST = 90  # REQUEST请求错误， 结束状态，失败
    CHARGE_STATE_ERROR_CALLBACK = 91  # 回调通知为失败， 结束状态，失败
    CHARGE_STATE_ERROR_CANCELED = 93  # 客户端取消订单， 结束状态，失败
