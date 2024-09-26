#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   task.py
@Time    :   2024-09-21 22:07:12
@Author  :   chakcy 
@Email   :   947105045@qq.com
@description   :   Task 类
'''

import socket
import threading

from PySide6.QtCore import QRunnable, SignalInstance

from ..utils.b64 import base64_decode
from ..tasks_service.ts import Tasks
from ..model import Request


class Task(QRunnable):
    # 任务处理函数
    def __init__(self, 
                 client_socket:socket.socket, 
                 data: bytes, 
                 tasks: type[Tasks], 
                 client_connected:SignalInstance, 
                 stop_event:threading.Event):
        super().__init__()
        self.client_socket = client_socket
        self.data = data
        self.client_connected = client_connected
        self.stop_event = stop_event
        self.tasks = tasks

    # 任务执行函数
    def run(self):
        result = self.process_data(self.data)
        try:
            self.emit_result(result)
        except Exception as e:
            print(f"An error occurred in task processing: {e}")
        finally:
            if self.client_socket:
                self.client_socket.close()
    
    # 处理数据函数
    def process_data(self, data: bytes):        
        data = base64_decode(data.decode()) # type: ignore
        request = Request.model_validate_json(data)
        result = self.tasks.run_task(request)
        return result

    def emit_result(self, result):
        if self.client_connected:
            if not self.stop_event.is_set():
                self.client_connected.emit(result)
