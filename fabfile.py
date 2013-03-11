# -*- coding: utf-8 -*-
from __future__ import with_statement
from fabric.api import *
from fabric.operations import run,env,local
from fabric.contrib.console import confirm
import fabtools.require
from fabtools.python_distribute import is_distribute_installed, install_distribute
from fabtools.require.python import  *
env.hosts = ['192.168.1.45']
def test():
    with settings(warn_only=True):
        result = local('./manage.py test servers', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

def install_packages():

    fabtools.require.deb.packages([
                                      'python-dev',
                                      'curl'
                                  ], update=False
    )
    # installation de python
    if not  is_distribute_installed():
        install_distribute()
    # installation de pip
    if not is_pip_installed():
        install_pip()

def install_mysql():
    #installtion de mysql
    fabtools.require.mysql.server(password='passer12')

def commit():
    local("git add -p && git commit")

def push():
    local("git push")

def prepare_deploy():
    test()
    commit()
    push()

def deploy():
    code_dir = '/home/manga/deplyapp'
    #sudo("mkdir -p deploymanga")
    #cd("deploymanga")
    with settings(warn_only=True):
        if local("test -d %s" % code_dir).failed:
            local("git clone git@github.com:macksoft2/servers.git %s" % code_dir)
    with cd(code_dir):
        local("git pull origin master")
        local("touch app.wsgi")