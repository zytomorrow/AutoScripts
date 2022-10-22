#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
PT站 hdtime.org每日登录
"""

import re
import time

from bs4 import BeautifulSoup

from lib.apiHandler import ApiHandle
from lib.logger import logger
from lib.ocr import OCR

DOMAIN = 'https://hdtime.org'


def run(username, password):
    # 初始化session
    api_handler = ApiHandle()
    ocr_handler = OCR()
    for i in range(10):
        logger.info(f'尝试第{i + 1}次登录')
        # 初始化网页
        login_page_code = api_handler.get_url(f'{DOMAIN}/login.php').text
        # 执行登录
        login_response = api_handler.post_url(f'{DOMAIN}/takelogin.php',
                                              data={
                                                  'secret': '',
                                                  'username': username,
                                                  'password': password,
                                                  'two_step_code': ''
                                              })
        if login_response.url.split('/')[-1] == 'index.php':
            # 执行签到操作
            logger.info('执行签到...')
            api_handler.get_url(f'{DOMAIN}/attendance.php')
            # 获取当前信息
            doc = BeautifulSoup(login_response.content.decode(), "html.parser")
            basic_info = doc.findAll('span')[0].text.replace('\r\n', '').replace('                ', '').split('[收藏]')[-1]
            return basic_info
        else:
            logger.info(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}登录失败,重新登录')
