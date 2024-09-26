#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   socket_thread.py
@Time    :   2024-04-28 19:00:00
@Author  :   chakcy 
@Email   :   947105045@qq.com
@description   :   socket服务端线程
'''


import socket
import threading

from PySide6 import QtWidgets
from PySide6.QtCore import QObject, QThread, Slot, Signal, QThreadPool

from ..config import SocketConfig
from .task import Task
from ..tasks_service.ts import TS, Tasks


host, port = SocketConfig.get_host_port()

# 服务器线程类
class SocketServerThread(QObject):
    # 信号定义
    client_connected = Signal(dict)
    finished = Signal()
    
    _stop_event = threading.Event()  # 线程停止事件
    # 构造函数
    def __init__(self, tasks: type[Tasks]):
        super().__init__()
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False  # 添加运行标志
        self.pool = QThreadPool.globalInstance()
        self.tasks = tasks
  
    # 线程执行函数
    @Slot()
    def run(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.server_socket.settimeout(0.5)
            print(f"Server listening on port {self.port}")
            self.running = True
            while not self._stop_event.is_set() and self.running:  # 使用运行标志来控制循环
                if self.server_socket is None:
                    break
                try:
                    client_socket, address = self.server_socket.accept()
                except socket.timeout:
                    continue
                except socket.error as e:
                    if  e.errno == 9:
                        print("Server socket closed, exiting loop.")
                        break
                    else:
                        raise
                print(f"Connection from {address}")
  
                # 启动任务处理客户端请求，但不关闭socket
                data = b''
                while not self._stop_event.is_set() and self.running:
                    if client_socket is None:
                        break
                    try:
                        received = client_socket.recv(1024)
                    except socket.timeout:
                        continue
                    except socket.error as e:
                        if e.errno == 9:
                            print("Client socket closed, exiting loop.")
                            break
                        else:
                            raise
                    if not received:
                        break
                    data += received
                if data and not self._stop_event.is_set() and self.running:
                    task = Task(client_socket, data, self.tasks, self.client_connected, self._stop_event)
                    self.pool.start(task)

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            self.finished.emit()  # 发送完成信号


    # 停止线程函数
    @Slot()
    def stop(self):
            self._stop_event.set()  # 设置停止事件
            if self.server_socket:
                self.server_socket.close()
            self.pool.clear()  # 清空线程池
            self.running = False  # 设置运行标志为False来退出循环
            self.finished.emit()  # 发送完成信号


def create_socket_server_thread(task_service: type[TS], app: QtWidgets.QApplication):
    thread = QThread()
    socket_server_thread = SocketServerThread(task_service.tasks)
    socket_server_thread.moveToThread(thread)
    thread.started.connect(socket_server_thread.run)
    socket_server_thread.client_connected.connect(task_service.on_client_connected)
    socket_server_thread.finished.connect(thread.quit)
    thread.finished.connect(app.quit)
    def stop_socket_server_thread():
        if thread.isRunning():
            socket_server_thread.stop()
            thread.quit()
        if not thread.wait():
            print("线程无法正常退出，强制退出")
            thread.terminate()
    app.aboutToQuit.connect(stop_socket_server_thread)
    thread.start()
