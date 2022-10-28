#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
PT站www.icc2022.com每日登录
"""

import re
import time

from bs4 import BeautifulSoup

from lib.apiHandler import ApiHandle
from lib.logger import logger

DOMAIN = 'http://www.dyhrsc.cn'


def run(username, password):
    # 初始化session
    api_handler = ApiHandle()
    for i in range(10):
        logger.info(f'尝试第{i + 1}次登录')
        # 初始化网页
        login_page_code = api_handler.get_url(f'{DOMAIN}/dypx/Main/Logon.aspx').text
        # 获取隐藏参数
        __VIEWSTATE = re.findall('<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)" />', login_page_code)[0]
        __VIEWSTATEGENERATOR = re.findall('<input type="hidden" name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="(.*?)" />', login_page_code)[0]
        __EVENTVALIDATION = re.findall('<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.*?)" />', login_page_code)[0]
        # 执行登录
        login_response = api_handler.post_url(f'{DOMAIN}/dypx/Main/Logon.aspx',
                                              data={
                                                  '__VIEWSTATE': __VIEWSTATE,
                                                  '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
                                                  '__EVENTVALIDATION': __EVENTVALIDATION,
                                                  'txtUser': username,
                                                  'txtPwd': password,
                                                  'btnLogin': ''
                                              })
        if '学员登录' not in login_response.content.decode():
            # 获取课程列表
            course_data = api_handler.post_url(f'{DOMAIN}/dypx/OnlineLearning/Service.ashx?Action=GetCourseListAll',
                                 data={
                                     'needResultField': False,
                                     'startRowIndex': 0,
                                     'pageSize': 50,
                                     'recordCount': 0,
                                     'sortField': '',
                                     'sortType': 'asc'
                                 })
            # 获取子课程
            for course in course_data.json()['datas']:

                chpter_data = api_handler.post_url(f'{DOMAIN}/dypx/OnlineLearning/Service.ashx?Action=GetCourse_Chapter_ListAll',
                                     data={
                                         'needResultField': False,
                                         'startRowIndex': 0,
                                         'pageSize': 50,
                                         'recordCount': 0,
                                         'sortField': '',
                                         'sortType': 'asc',
                                         'KeyID': course[1]
                                     }).json()['datas']
                for chapter in chpter_data:
                    chapter_keyid = chapter[1]
                    chapter_name = chapter[6]
                    chapter_status = chapter[-1]
                    if chapter_status == '1':
                        logger.info(f'{chapter_name}已完成')
                    else:
                        logger.info(f'{chapter_name}未完成,开始学习')
                        api_handler.get_url(f'{DOMAIN}/dypx/OnlineLearning/Service.ashx?Action=GetARRCount&KeyID={chapter_keyid}')
                        api_handler.post_url(f'{DOMAIN}/dypx/OnlineLearning/Service.ashx?Action=UpdateStatr',
                                             data={
                                                 'zjid': chapter_keyid
                                             })




            # 检查学习状态

            # 开始学习

            # 循环请求

            # 结束学习

            #


        else:
            logger.info(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}登录失败,重新登录')
