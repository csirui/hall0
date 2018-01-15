# -*- coding=utf-8 -*-

def __lock_obj_attr__(*args, **kwargs):
    raise Exception('Can Not Modify Lock Object !!')


class LockAttr(object):
    def __init__(self):
        self.lock(self)

    def lock(self, obj):
        object.__setattr__(obj, '__setattr__', __lock_obj_attr__)

    def unlock(self, obj):
        if isinstance(obj, object):
            funset = getattr(obj, '__setattr__', None)
            if funset == __lock_obj_attr__:
                delattr(obj, '__setattr__')


LockAttr = LockAttr()
