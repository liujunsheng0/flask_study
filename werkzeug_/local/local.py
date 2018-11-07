#!/usr/bin/python3
# -*- coding: utf-8 -*-


from werkzeug.local import LocalProxy, get_ident
from threading import Thread


class Local(object):
    __slots__ = ('__storage__', '__ident_func__')

    def __init__(self):
        # 不能直接赋值, 会造成栈溢出, 因为__getattr__. https://github.com/liujunsheng0/study_py3/tree/master/magic_method
        # self.__storage__ = {k, v}, k = 线程/协程标识, v = {name: value...}, 由__setattr__所知
        object.__setattr__(self, '__storage__', {})
        # self.__ident_func__ = get_ident 生成唯一的线程/协程标识
        object.__setattr__(self, '__ident_func__', get_ident)

    def __iter__(self):
        return iter(self.__storage__.items())

    def __call__(self, proxy):
        """Create a proxy for a name."""
        return LocalProxy(self, proxy)

    def __release_local__(self):
        # 释放当前线程/线程存储的数据
        self.__storage__.pop(self.__ident_func__(), None)

    def __getattr__(self, name):
        """ 取值时都会调用此方法, 会先获取当前线程/协程的唯一标识, 找到其对应的dict, 取dict中的值 """
        try:
            # dict = self.__storage__[self.__ident_func__()], 当前线程/线程对应的存储数据的字典
            # return dict[name]
            return self.__storage__[self.__ident_func__()][name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        """ 赋值操作都会调用此方法 """
        ident = self.__ident_func__()  # 当前线程/协程id
        storage = self.__storage__
        try:
            storage[ident][name] = value
        except KeyError:
            # 线程 -> dict
            storage[ident] = {name: value}

    def __delattr__(self, name):
        try:
            del self.__storage__[self.__ident_func__()][name]
        except KeyError:
            raise AttributeError(name)


def test_local():
    l = Local()
    l.curren = '11'

    def job(key, value):
        setattr(l, key, value)

    print('init', l.__storage__)

    for i in range(3):
        Thread(target=job, args=('i%s' % i, i * 10)).start()

    for k, v in iter(l):
        print(k, v)


if __name__ == '__main__':
    test_local()
