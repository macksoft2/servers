# -*- coding: utf-8 -*-
from __future__ import with_statement
from fabric.api import *
from fabric.operations import run,env,local
from fabric.contrib.console import confirm
import fabtools.require
from fabtools.python_distribute import is_distribute_installed, install_distribute
from fabtools.require.python import  *
#--------------------------------------------debut fonctions -------------------------#

env.hosts = ['192.168.1.45']
code_dir = '/root/manga'

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
    local("git push servers ")
#--------------------------------------------- End dev fonctions-----------------------------------#

@hosts('localhost:8000')
def prepare_deploy():
    commit()
    push()

def deploy():
    #local('ssh-copy-id root@192.168.1.45')
    sudo('cd /root & mkdir manga')
    run("git clone git//github.com:macksoft2/servers %s" % code_dir)
    with cd(code_dir):
        run("git pull origin master")
        run("touch myapp.wsgi")
