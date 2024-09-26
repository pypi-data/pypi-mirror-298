#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2024-04-28 19:01:34
@Author  :   chakcy 
@Email   :   947105045@qq.com
@description   :   任务服务模块
'''

import logging
from typing import Callable
import pkgutil
from importlib import import_module
import uuid

from PySide6.QtCore import Slot

from .tasks import Tasks
from .task_base import TaskBase
from ..model import Result, Request
from ..utils import client_send_request  


class TS:
    tasks = Tasks
    services = {}

    @classmethod
    def add(cls, task_name: str, task_class: type[TaskBase]):
        cls.tasks.append_Task(task_name, task_class)

    @classmethod
    def get_all_task_names(cls) -> list:
        task_names_list = []
        for task_name, task_class in cls.tasks.TaskClasses.items():
            task_names_list.append(task_name)
        return task_names_list
    
    @classmethod
    def append_callback(cls, id, func):
        cls.services[id] = func

    @classmethod
    def delete_callback(cls, id):
        try:
            del cls.services[id]

        except KeyError:
            raise ValueError(f"Callback with id {id} not found.")
            
    @classmethod
    def send_data(cls, task_name:str, args:dict, callback=None):
        try:
            id = str(uuid.uuid4())
            request = Request(id=id, task_name=task_name, args=args)
            cls.append_callback(request.id, callback)
            client_send_request(request)
        except Exception as e:
            raise ValueError(f"Task {task_name} not found. {e}")

    @Slot(dict)
    @classmethod
    def on_client_connected(cls, response_data_dict: dict):
        if "task_name" not in response_data_dict or "id" not in response_data_dict:
            raise ValueError("Response data must contain 'task_name' and 'id'.")
        try:
            response = Result.model_validate(response_data_dict)
        except Exception as e:
            raise ValueError(response_data_dict)
        try:
            logging.info(f"{response.task_name} callback result: \n{response}")
            cls.services.get(response.id)(response) # type: ignore
        except Exception as e:
            logging.error(f"{response.task_name} callback error: \n{e}")
            raise ValueError(f"{response.task_name} callback error: {e}")
        cls.delete_callback(response.id)


def create_ts_item(task_func: Callable):

    class DynamicTask(TaskBase):
        TASK_NAME = "{task_func.__name__}"
        def __init__(self, id: str, params: dict):
            super(DynamicTask, self).__init__(task_func.__name__, id, params)
            self.task = task_func
    return task_func.__name__, DynamicTask


def task_function(func: Callable):
    func.is_task = True
    return func


def discover_and_mount_ts_item(base_package: str):
    package = import_module(base_package)
    for _, module_name, _ in pkgutil.iter_modules(package.__path__, package.__name__ + '.'):
        module = import_module(module_name)
        for name, obj in vars(module).items():
            if callable(obj) and hasattr(obj, 'is_task'):
                task_name, task_class = create_ts_item(obj)
                TS.add(task_name, task_class)
    return TS

send_data = TS.send_data
