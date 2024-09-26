#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   task_item.py
@Time    :   2024-04-28 18:55:58
@Author  :   chakcy 
@Email   :   947105045@qq.com
@description   :   Task 父类
'''

from ..constants.task_status import TaskStatus  
import time
import logging


class TaskBase:
    def __init__(self, name, id, params=None):  
        self.id = id  # 任务ID  
        self.name = name  # 任务名称  
        self.status = TaskStatus.PENDING # 任务状态  
        # self.priority = 0  # 任务优先级  
        self.created_at = time.time()  # 任务创建时间  
        self.updated_at = self.created_at  # 任务更新时间  
        self.params = params if params is not None else {} # 任务参数  
        self.result = None  # 任务结果 

    def execute(self):
        # 执行任务  
        self.status = TaskStatus.RUNNING  # 任务状态  
        self.updated_at = time.time()  # 任务更新时间  
        try:
            # self.id = self.params.get('id', '')  # 任务ID  
            self.set_result(self.task(self.params))  # 任务结果  
            self.set_status(TaskStatus.SUCCEEDED)  # 任务状态 

        except Exception as e:  
            self.set_result(f"Task {self.name} failed: {str(e)}")  
            self.set_status(TaskStatus.FAILED)  # 任务状态  
            logging.error(f"{self.name} task error: \n{e}")
            raise ValueError(f"Task {self.name} failed: {str(e)}")

        finally:
            self.updated_at = time.time()  # 任务更新时间 

    def result_callback(self):
        self.execute()
        return self.get_result()

    def task(self, args):
        pass

    def set_status(self, status):  
        self.status = status  
        self.updated_at = time.time()  
  
    def get_status(self):  
        return self.status  
  
    def update_params(self, new_params):  
        self.params.update(new_params)  
        self.updated_at = time.time()  
  
    def get_params(self):  
        return self.params  
  
    def set_result(self, result):  
        self.result = result  
  
    def get_result(self):  
        return {
        "task_name": self.name,
        "id": self.id,
        "result": self.result,
        "status": self.get_status(),
        "created_at": self.created_at,
        "updated_at": self.updated_at
    }  
  
    def is_pending(self):  
        return self.status == TaskStatus.PENDING  
  
    def is_running(self):  
        return self.status == TaskStatus.RUNNING  
  
    def is_completed(self):  
        return self.status in [TaskStatus.SUCCEEDED, TaskStatus.FAILED]  
  
    def is_successful(self):  
        return self.status == TaskStatus.SUCCEEDED  
  
    def is_failed(self):  
        return self.status == TaskStatus.FAILED
