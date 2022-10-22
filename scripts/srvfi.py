#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
PT站 srvfi.top每日登录
"""

import re
import time

from bs4 import BeautifulSoup

from lib.apiHandler import ApiHandle
from lib.logger import logger
from lib.ocr import OCR

DOMAIN = 'https://srvfi.top'


def run(username, password):
    # 初始化session
    api_handler = ApiHandle()
    ocr_handler = OCR()
    for i in range(10):
        # 初始化网页
        login_page_code = api_handler.get_url(f'{DOMAIN}/login.php').text
        # 获取imghash
        img_hash = re.findall('<input type="hidden" name="imagehash" value="(.*?)"', login_page_code)[0]
        img_url = f'{DOMAIN}/image.php?action=regimage&imagehash={img_hash}&secret='
        # 请求图片
        img_content = api_handler.get_url(img_url).content
        # ocr识别
        verify_code = ocr_handler.ocr(img_content)
        # 执行登录
        login_response = api_handler.post_url(f'{DOMAIN}/takelogin.php',
                                              data={
                                                  'secret': '',
                                                  'username': username,
                                                  'password': password,
                                                  'two_step_code': '',
                                                  'imagestring': verify_code,
                                                  'imagehash': img_hash
                                              })
        if login_response.url.split('/')[-1] == 'index.php':
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
