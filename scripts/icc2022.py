#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
PT站www.icc2022.com每日登录
"""

import re
import time

from lib.apiHandler import ApiHandle
from lib.ocr import OCR


def run(username, password):
    # 初始化session
    api_handler = ApiHandle()
    ocr_handler = OCR()
    for i in range(10):
        # 初始化网页
        login_page_code = api_handler.get_url('https://www.icc2022.com/login.php').text
        # 获取imghash
        img_hash = re.findall('<input type="hidden" name="imagehash" value="(.*?)"', login_page_code)[0]
        img_url = f'https://www.icc2022.com/image.php?action=regimage&imagehash={img_hash}&secret='
        # 请求图片
        img_content = api_handler.get_url(img_url).content
        # ocr识别
        verify_code = ocr_handler.ocr(img_content)
        # 执行登录
        login_status = api_handler.post_url('https://www.icc2022.com/takelogin.php',
                                            data={
                                                'secret': '',
                                                'username': username,
                                                'password': password,
                                                'two_step_code': '',
                                                'imagestring': verify_code,
                                                'imagehash': img_hash
                                            })
        if login_status.status_code == 200:
            # 执行签到操作
            attendance_response = api_handler.get_url('https://www.icc2022.com/attendance.php')
            if attendance_response.status_code == 200:
                msg = f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) }签到成功'
            else:
                msg = '签到失败'
            break
        else:
            msg = '登录失败'

    return msg
