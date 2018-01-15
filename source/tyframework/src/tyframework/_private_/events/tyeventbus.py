# -*- coding=utf-8 -*-

'''
Created on 2014年2月20日

@author: zjgzzz@126.com
'''
import time


class TYEventBus(object):
    def __init__(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext
        # key=eventName, value=set<TYEventHandler>
        self.__handlersMap = {}
        # value=TYEventHandler
        self.__allEventHandlers = set()
        # 当前等待处理的events
        self.__events = []
        # 正在处理消息
        self.__processing = False

    def subscribe(self, eventType, handler):
        '''订阅eventType的event, 由handler处理, 如果channel为None则表示订阅所有频道'''
        assert (handler)
        if eventType is None:
            self.__allEventHandlers.add(handler)
        else:
            if eventType in self.__handlersMap:
                self.__handlersMap[eventType].add(handler)
            else:
                self.__handlersMap[eventType] = set([handler])

    def unsubscribe(self, eventType, handler):
        '''取消订阅eventType的event, 由handler处理, 如果channel为None则表示订阅所有频道'''
        assert (callable(handler))
        if eventType is None:
            self.__allEventHandlers.discard(handler)
        elif eventType in self.__handlersMap:
            self.__handlersMap[eventType].discard(handler)

    def publishEvent(self, event):
        '''发布一个event'''
        assert (isinstance(event, self.__ctx__.TYEvent))
        if event.timestamp is None:
            event.timestamp = time.time()
        self.__events.append(event)
        if not self.__processing:
            self.__processing = True
            while (len(self.__events) > 0):
                curEvent = self.__events[0]
                del self.__events[0]
                self._processEvent(curEvent)
            self.__processing = False

    def _processEvent(self, event):
        try:
            eventType = type(event)
            handlers = set(self.__allEventHandlers)
            for handler in handlers:
                try:
                    handler(event)
                except:
                    self.__ctx__.ftlog.exception()
            if eventType in self.__handlersMap:
                handlers = set(self.__handlersMap[eventType])
                for handler in handlers:
                    try:
                        handler(event)
                    except:
                        self.__ctx__.ftlog.exception()
        except:
            self.__ctx__.ftlog.exception()
