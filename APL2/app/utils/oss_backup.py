#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/7 上午10:45
# @Author  : Rain
# @Desc    : OSS 文件备份脚本
# @File    : oss_backup.py

import os
import oss2
import time

access_key_id = 'LTAIbbmhcmSDUjc9'
access_key_secret = 'WDRrv4AVtnRVPtDMOdWE3SkEIUaR5S'
bucket_name = 'apl-docs'
endpoint = 'oss-cn-beijing.aliyuncs.com'

bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

current_path = os.path.dirname(os.path.abspath(__file__))
log_name = os.path.join(current_path, 'log.txt')
backup_dir = os.path.join(current_path, 'docs')

if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

with open(log_name, 'a') as f:

    # 打印分隔符
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    separator = '*' * 20 + ' ' + now + ' ' + '*' * 20 + '\n'
    f.write(separator)

    for i, obj_info in enumerate(oss2.ObjectIterator(bucket)):
        file_name = obj_info.key
        if '/' not in file_name:  # 不处理目录
            local_file = os.path.join(backup_dir, file_name)
            if not os.path.exists(local_file):
                f.write(file_name + '\n')
                bucket.get_object_to_file(file_name, local_file)
