# -*- coding: utf-8 -*-
"""
    fabfile
    ~~~~~~~~~~~~~~

    Fab.

    :copyright: (c) 2016 by fengweimin.
    :date: 16/7/21
"""

from fabric.api import *
from jinja2 import Environment, FileSystemLoader

from fabenv import *

# The user to use for the remote commands
env.user = USER
env.password = PASSWORD
# The servers where the commands are executed
env.hosts = HOSTS
# Project folder
project_folder = '/usr/local/tuna'


def publish():
    """
    Publish latest version.
    """
    print('----- Publishing on server %s -----' % env.host_string)
    with cd(project_folder):
        run('git pull')
        run('make')


def config():
    """
    Generate config files.
    """
    print('----- Generating config to server %s -----' % env.host_string)
    params = {
        'secret': SECRET
    }
    gen = 'gen/config.json'
    Environment(loader=FileSystemLoader('.')).get_template('server.json').stream(**params).dump(gen)
    with cd(project_folder):
        put(gen, 'bin')


def restart():
    """
    Restart service.
    """
    print('----- Restarting service on server %s -----' % env.host_string)
    with cd('~'):
        run('killall -9 tuna')
        cmd = 'tuna'
        run('set -m; (nohup %s &) && sleep 1' % cmd)
