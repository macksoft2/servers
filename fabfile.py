# -*- coding: utf-8 -*-
from __future__ import with_statement
from fabric.api import *
from fabric.operations import run,env,local
from fabric.contrib.console import confirm
import fabtools.require
from fabtools.python_distribute import is_distribute_installed, install_distribute
from fabtools.require.python import  *
#--------------------------------------------debut fonctions -------------------------#

env.hosts = ['198.168.1.45']

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

def install_mysql(mdp="passer"):
    #installtion de mysql
    fabtools.require.mysql.server(password=mdp)

def commit():
    local("git add . && git commit")

def push():
    local("git push ")
#--------------------------------------------- End dev fonctions-----------------------------------#

@hosts('localhost:8000')
def prepare_deploy():
    commit()
    push()

def deploy():
    sudo("cd /home  & mkdir -p  mangatestdeploy")
    code_dir = '/home/mangatestdeploy'
    #local("chmod 600 .ssh/authorized_keys")
    run("git clone git@github.com:macksoft2/servers.git %s" % code_dir)

    with cd(code_dir):
        run("git pull origin master")
        run("touch myapp.wsgi")
