#!/usr/bin/python3
# -*- coding: utf-8 -*-

from werkzeug.local import Local, LocalProxy, release_local
from threading import Thread


class LocalStack(object):
    """
    利用Local(), 值存储在Local().__storage__[线程/协程标识]['stack']中
    值为list类型, 通过操作此变量实现了栈
    """

    def __init__(self):
        self._local = Local()

    def __release_local__(self):
        """ 释放当前线程/协程存储的数据 """
        self._local.__release_local__()

    def _get__ident_func__(self):
        """ 获取生成生成线程/唯一标识的函数 """
        return self._local.__ident_func__

    # 利用特性, 设置self._local 中的 __ident_func__ , 如果正常赋值的话, 会存储到self.__storage__中
    def _set__ident_func__(self, value):
        object.__setattr__(self._local, '__ident_func__', value)

    __ident_func__ = property(_get__ident_func__, _set__ident_func__)
    # 还可以这样写....
    del _get__ident_func__, _set__ident_func__

    def __call__(self):
        """ LocalStack 实例还可以调用, 返回一个代理, 每次获取当前线程的栈顶元素 """
        def _lookup():
            rv = self.top
            if rv is None:
                raise RuntimeError('object unbound')
            return rv
        return LocalProxy(_lookup)

    def push(self, obj):
        """Pushes a new item to the stack"""
        # rv = self._local.__storage__[线程标识]['stack']
        # rv.append(obj)
        rv = getattr(self._local, 'stack', None)
        if rv is None:
            self._local.stack = rv = []
        rv.append(obj)
        return rv

    def pop(self):
        """Removes the topmost item from the stack, will return the
        old value or `None` if the stack was already empty.
        """
        stack = getattr(self._local, 'stack', None)
        if stack is None:
            return None
        elif len(stack) == 1:
            release_local(self._local)
            return stack[-1]
        else:
            return stack.pop()

    @property
    def top(self):
        """The topmost item on the stack.  If the stack is empty,
        `None` is returned.
        """
        try:
            return self._local.stack[-1]
        except (AttributeError, IndexError):
            return None

ls = LocalStack()


def job(n):
    for i in range(n):
        ls.push(i)

for n in range(3):
    Thread(target=job, args=(n + 10, )).start()

print(ls._local.__storage__)


