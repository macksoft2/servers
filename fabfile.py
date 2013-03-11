# -*- coding: utf-8 -*-
from __future__ import with_statement
from fabric.api import *
from fabric.operations import run,env,local
from fabric.contrib.console import confirm
import fabtools.require
from fabtools.python_distribute import is_distribute_installed, install_distribute
from fabtools.require.python import  *
#env.hosts = ['192.168.1.45']
#--------------------------------------------debut fonctions -------------------------#
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


code_dir = "/home/manga/myapp/"


def commit(m=None):
    local("git add . && git commit -m \"%s\"" % m)

def push():
    local("git push origin master")
#--------------------------------------------- End dev fonctions-----------------------------------#

@hosts('localhost:8000')
def prepare_deploy():
    message = raw_input("Enter a git commit message:  ")
    commit(message)
    push()

@hosts('192.168.1.45')
def deploy():
    with cd(code_dir):
        run("git pull origin master")
        run("touch myapp.wsgi")





