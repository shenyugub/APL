#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/7 下午1:40
# @Author  : Rain
# @Desc    : 线上数据库备份脚本
# @File    : database_backup.py

import os
from os.path import basename
import time
import zipfile

db_host = "rm-2ze9uiue6mo09e0m9o.mysql.rds.aliyuncs.com"
db_user = "backup"
db_password = ""
db_name = "apl"

current_path = os.path.dirname(os.path.abspath(__file__))
backup_dir = os.path.join(current_path, 'db')

if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

zip_src = os.path.join(backup_dir, time.strftime("%Y%m%d%H%M%S") + '.sql')
zip_dest = zip_src + ".zip"


def zip_files():
    f = zipfile.ZipFile(zip_dest, 'w', zipfile.ZIP_DEFLATED)
    f.write(zip_src, basename(zip_src))
    f.close()


if __name__ == "__main__":
    print("begin to dump mysql database...")
    os.system("mysqldump -h%s -u%s -p%s --set-gtid-purged=OFF --triggers --routines --events %s > %s" % (db_host, db_user, db_password, db_name, zip_src))
    print("begin zip files...")
    zip_files()
    os.remove(zip_src)
    print("done!")
