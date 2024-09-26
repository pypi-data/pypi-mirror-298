#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   task_status.py
@Time    :   2024-04-28 18:56:18
@Author  :   chakcy 
@Email   :   947105045@qq.com
@description   :   Task 状态
'''
from enum import Enum

class TaskStatus(Enum):  
    PENDING = 'PENDING'  
    RUNNING = 'RUNNING'  
    SUCCEEDED = 'SUCCEEDED'  
    FAILED = 'FAILED'
    