#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
PT站www.icc2022.com每日登录
"""

from lib.apiHandler import ApiHandle
from pyquery import PyQuery as pq


def run(username, passwd):
    # 初始化session
    api_handler = ApiHandle()
    # 初始化网页
    login_page_code = api_handler.get_url('https://www.icc2022.com/login.php').text
    # 获取验证码图片地址
    doc = pq(login_page_code)
    print(doc('#nav_block > form:nth-child(4) > table > tbody > tr:nth-child(4) > td:nth-child(2) > img'))

    # 获取

#
# class Client(object):
#     def __init__(self, username, password):
#         self.username = username
#         self.password = password
#         self.api_handle = ApiHandle()
#
#     def init_login_page(self):
#         self.api_handle.ge

if __name__ == '__main__':
    run(111, 111)