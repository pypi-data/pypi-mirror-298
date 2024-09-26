#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2024-04-29 13:38:45
@Author  :   chakcy 
@Email   :   947105045@qq.com
@description   :   缓存模块
'''

class Cache:
    def __init__(self):
        self.cache = {}

    def set(self, key, value):
        self.cache.setdefault(key, value)

    def get(self, key):
        return self.cache.get(key, '')

    def delete(self, key):
        if key in self.cache:
            del self.cache[key]

cache = Cache()
