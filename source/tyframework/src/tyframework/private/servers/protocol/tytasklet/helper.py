# -*- coding=utf-8 -*-
'''
Created on 2014年5月22日

@author: ZQH
'''

import stackless
from twisted.internet import reactor


class TaskletHelper:
    @classmethod
    def getTasklet(cls):
        tasklet = stackless.getcurrent()._tyTasklet
        return tasklet

    @classmethod
    def asyncTasklet(cls, tasklet):
        if tasklet:
            stackless.tasklet(tasklet.tasklet)()
            reactor.callLater(0, stackless.schedule)
