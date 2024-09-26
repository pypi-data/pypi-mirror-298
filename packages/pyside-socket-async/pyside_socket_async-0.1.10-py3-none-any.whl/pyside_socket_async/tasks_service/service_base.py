#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   serice_base.py
@Time    :   2024-09-26 01:17:43
@Author  :   chakcy 
@Email   :   947105045@qq.com
@description   :   ServiceBase
'''

from .ts import send_data
from abc import ABC, abstractmethod
import json


class ServiceBase(ABC):
    @classmethod
    @abstractmethod
    def request(cls, task_name: str, data):
        try:
            json.dumps(data)
        except Exception as e:
            raise ValueError(f"Invalid data format. Error :{str(e)}")
        send_data(task_name, data, cls.callback)

    @classmethod
    @abstractmethod
    def callback(cls, response):
        pass
    