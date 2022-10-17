#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import yaml
"""
程序入口文件
"""

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
                pass

        # 推送信息配置
        for push_service in content['pushnotice']:
            push_service_name, push_service_config = list(push_service.keys())[0], list(push_service.values())[0]
            if push_service_config['enable']:
                # todo: 加载推送信息进队列
                pass
