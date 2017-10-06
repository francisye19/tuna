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

# Use instance package to store secrets
try:
    from instance.fabenv import *
except ImportError:
    from fabenv import *

# The user to use for the remote commands
env.user = USER
env.password = PASSWORD
# The servers where the commands are executed
env.hosts = HOSTS
env.roledefs = {
    'local': ['localhost'],
    'remote': [h[1] for h in HOSTS]
}
# Project folder
project_folder = '/usr/local/tuna'


@roles('remote')
def publish():
    """
    Publish latest version.
    """
    print('----- Publishing on %s -----' % env.host_string)
    with cd(project_folder):
        run('git pull')
        run('make')


@roles('remote')
def config_server():
    """
    Generate server config files and upload.
    """
    print('----- Generating config on %s -----' % env.host_string)
    params = {
        'secret': SECRET
    }
    gen = 'gen/config.json'
    Environment(loader=FileSystemLoader('./templates')).get_template('server.json').stream(**params).dump(gen)
    with cd(project_folder):
        put(gen, 'bin')


@roles('remote')
def restart():
    """
    Restart service.
    """
    print('----- Restarting service on %s -----' % env.host_string)
    with cd('~'):
        run('killall -9 tuna')
        cmd = 'tuna'
        run('set -m; (nohup %s &) && sleep 1' % cmd)


@roles('local')
def config_client():
    """
    Generate client config files and copy to bin folder.
    """
    print('----- Generating config to %s -----' % env.host_string)
    params = {
        'secret': SECRET,
        'hosts': HOSTS
    }
    gen = '../bin/config.json'
    Environment(loader=FileSystemLoader('./templates')).get_template('client.json').stream(**params).dump(gen)
