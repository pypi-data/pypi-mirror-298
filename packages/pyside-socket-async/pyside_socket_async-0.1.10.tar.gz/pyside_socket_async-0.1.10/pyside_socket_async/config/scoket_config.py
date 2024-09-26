#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   scoket_config.py
@Time    :   2024-04-28 19:02:52
@Author  :   chakcy 
@Email   :   947105045@qq.com
@description   :   socket配置
'''

import socket  


def find_available_port():  
    for port in range(5000, 6000):  # 假设我们检查5000到5999的端口范围  
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        sock.settimeout(1)  
        result = sock.connect_ex(('localhost', port))  
        sock.close()  
        # 如果连接失败（即端口未被占用），返回该端口  
        if result != 0:  
            return port  
    # 如果所有端口都被占用，抛出一个异常  
    raise Exception("No available port found in the specified range.") 

port = find_available_port()  

class SocketConfig:
    HOST = "127.0.0.1"
    PORT = port

    @classmethod
    def get_host_port(cls):
        return cls.HOST, cls.PORT
    