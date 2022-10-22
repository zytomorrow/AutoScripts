#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
程序入口文件
"""

import os

import yaml

from lib.logger import logger

CONFIG_FILE_PATH = './config.yaml'
PUSH_SERVER_HANDLERS = []

if __name__ == '__main__':
    # 加载配置文件
    if not os.path.exists(CONFIG_FILE_PATH):
        msg = '配置文件不存在！'
    else:
        # 解析配置文件
        with open(CONFIG_FILE_PATH, encoding='utf8') as f:
            content = yaml.load(f.read(), Loader=yaml.SafeLoader)

        # todo: 通用配置

        # 执行脚本配置
        for script in content['scripts']:
            script_name, script_config = list(script.keys())[0], list(script.values())[0]
            if script_config['enable']:
                # 动态加载方法
                _run = __import__(f'scripts.{script_name}', fromlist=[script_name])
                # 遍历账号配置
                for conf in script_config['confs']:
                    logger.info(_run.__doc__)
                    # 进行重试
                    for _ in range(3):
                        try:
                            result = _run.run(**conf)
                            logger.info(f'{script_name}:{conf}:{result}')
                            break
                        except BaseException as err:
                            logger.error(f'{script_name}:{conf}:{err}')

        # 推送信息配置
        for push_service in content['push_notice']:
            push_service_name, push_service_config = list(push_service.keys())[0], list(push_service.values())[0]
            if push_service_config['enable']:
                # todo: 加载推送信息进队列
                pass
