#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from datetime import datetime
from fabric.api import *
import getpass


env.user = 'root'
env.sudo_user = 'root'
env.hosts = ['apl.apluslabs.com']

db_user = 'apl'

_TAR_FILE = 'apl.tar.gz'
_REMOTE_TMP_TAR = '/tmp/%s' % _TAR_FILE

_ENV_FILE = 'env.tar.gz'
_REMOTE_ENV_TAR = '/tmp/%s' % _ENV_FILE

_REMOTE_ROOT_DIR = '/root'
_REMOTE_BASE_DIR = '/root/Repository'
_REMOTE_ENV_DIR = '/root/Repository/venv'


def _current_path():
    return os.path.abspath('.')


def _now():
    return datetime.now().strftime('%y-%m-%d_%H.%M.%S')


# 已废弃，utils下有专门的备份脚本
def backup():

    db_password = getpass.getpass('MySql Password:')

    dt = _now()
    f = 'backup-apl-%s.sql' % dt
    with cd('/tmp'):
        run('mysqldump --user=%s --password=%s --skip-opt --add-drop-table --default-character-set=utf8 --quick apl > %s' % (db_user, db_password, f))
        run('tar -czf %s.tar.gz %s' % (f, f))
        get('%s.tar.gz' % f, '%s/backup/' % _current_path())
        run('rm -f %s' % f)
        run('rm -f %s.tar.gz' % f)


def build():

    includes = ['app', 'config', 'migrations', '*.py', '*.txt']
    excludes = ['backup', 'docs', 'release', 'venv', '__pycache__', 'fabfile.py', 'README.md', 'development.py', 'options.txt', 'server_config']
    local('mkdir -p release')
    local('rm -f release/%s' % _TAR_FILE)
    with lcd(os.path.join(_current_path())):
        cmd = ['tar', '--dereference', '-czf', './release/%s' % _TAR_FILE]
        cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
        cmd.extend(includes)
        local(' '.join(cmd))


def deploy():

    newdir = 'www-%s' % _now()
    run('rm -f %s' % _REMOTE_TMP_TAR)
    put('release/%s' % _TAR_FILE, _REMOTE_TMP_TAR)
    with cd(_REMOTE_BASE_DIR):
        sudo('mkdir %s' % newdir)
    with cd('%s/%s' % (_REMOTE_BASE_DIR, newdir)):
        sudo('tar -xzf %s' % _REMOTE_TMP_TAR)
    with cd(_REMOTE_ROOT_DIR):
        sudo('rm -rf apl')
        sudo('ln -s %s/%s apl' % (_REMOTE_BASE_DIR, newdir))
        sudo('ln -s %s apl/venv' % _REMOTE_ENV_DIR)
        sudo('sudo supervisorctl restart apl')


def reboot():
    with cd(_REMOTE_ROOT_DIR):
        sudo('sudo supervisorctl restart apl')


def deploy_font():
    fontdir = '/usr/share/fonts/apl/'
    fontfile = 'Arial.ttf'
    sudo('mkdir -p %s' % fontdir)
    put(fontfile, fontdir)
    sudo('chmod 644 %s' % fontdir + fontfile)

    with cd(fontdir):
        sudo('mkfontscale')
        sudo('mkfontdir')
        sudo('fc-cache -fv')
