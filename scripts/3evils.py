#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
PT站3evils.net每日登录
"""

import re
import time

from bs4 import BeautifulSoup

from lib.apiHandler import ApiHandle
from lib.logger import logger
from lib.ocr import OCR

DOMAIN = 'https://3evils.net'


def run(username, password):
    # 初始化session
    api_handler = ApiHandle()
    ocr_handler = OCR()
    for i in range(10):
        logger.info(f'尝试第{i + 1}次登录')
        # 初始化网页
        login_page_init = api_handler.get_url(f'{DOMAIN}/login')
        # 获取token
        xsrf_token = login_page_init.cookies['XSRF-TOKEN']
        # 获取_token、时间等
        doc = BeautifulSoup(login_page_init.content.decode(), "html.parser")

        # 执行登录
        login_response = api_handler.post_url(f'{DOMAIN}/login',
                                              data={
                                                  '_token': doc('input')[0].attrs['value'],
                                                  'username': username,
                                                  'password': password,
                                                  '_captcha': doc('input')[-3].attrs['value'],
                                                  '_username': '',
                                                  f"{doc('input')[-1].attrs['name']}": doc('input')[-1].attrs['value'],
                                              })
        if login_response.url:
            # 执行签到操作
            logger.info('执行签到...')
            api_handler.get_url(f'{DOMAIN}/attendance.php')
            # 获取当前信息
            doc = BeautifulSoup(login_response.content.decode(), "html.parser")
            basic_info = doc.findAll('span')[0].text.replace('\n', '').split('[收藏]                ')[-1].replace(
                '                ', '')
            return basic_info
        else:
            logger.info(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}登录失败,重新登录')
