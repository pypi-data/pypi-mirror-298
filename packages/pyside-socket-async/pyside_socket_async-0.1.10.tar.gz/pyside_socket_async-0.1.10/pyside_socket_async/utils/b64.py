#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   B64.py
@Time    :   2024/03/11 23:27:53
@Author  :   chakcy 
@Email   :   947105045@qq.com
@description   :   base64
'''

import base64


def base64_decode(code:str) -> str:
    """
    Description:
        将Base64编码的字符串解码成原始字符串
   
    Aags:
        code (str): 待解码的Base64编码字符串
   
    Returns:
        解码后的原始字符串 (str)
    """
    decoded_bytes = base64.b64decode(code)
    json_string = decoded_bytes.decode('utf-8') 
    return json_string

def base64_encode(code:str) -> str:
    """
    Description:
        将字符串编码为Base64格式

    Args:
        code (str): 待编码的字符串
    
    Returns:
        编码后的Base64字符串 (str)
    """
    encoded_bytes = base64.b64encode(code.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string
