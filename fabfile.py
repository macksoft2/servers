# -*- coding: utf-8 -*-
from __future__ import with_statement
from checkbox.lib import input
from django.conf.urls import include
from fabric.api import * 
from fabric.operations import run,put

def install_pip_git():
    run('apt-get install python-pip')
    run('apt-get install git')
#END install pip and git

def install_Django():
    local('git clone git://github.com/django/django.git django-last-version')
    local('pip install -e django-last-version')
#END install Django

def install_SGBD():
    print("      1 - mysql")
    print("      2 - postgresql")
    print("      3 - oracle")
    choiDB = raw_input('Choisir un SGBD : ')

    if(choiDB=="1"):
        driver = "python-mysqldb"
        type_sgbd = "mysql-server"
        cmdConnectDB="mysql -u"
    elif(choiDB=="2"):
        driver = "Psycopg"
        type_sgbd = "postgrsql"
        cmdConnectDB=" "
    else:
        driver = "PyODBC"
        type_sgbd = "Oracle"
        cmdConnectDB = " "
    cmdDriver ="apt-get install "+driver
    cmdSgbd = "apt-get install "+type_sgbd
    local(cmdSgbd)
    print("Merci de fournir les  memes paramètres de la section DATABASES du fichier setting.y de votre application")
    username = raw_input("votre nom d'utilsateur svp !  ")
    cmdConnectDB = cmdConnectDB+username+" -p"
    local(cmdConnectDB)
#END install SGBD
env.hosts = ['192.168.1.45']

#install_pip_git()

def test():
    local("./manage.py test servers")
def commit():
    local("git add -p && git commit ")
    local("git push -f")
def deploy():
    sudo('aptitude install -y python-setuptools apache2 libapache2-mod-wsgi')
    sudo('easy_install pip')
    sudo('pip install virtualenv')
    sudo('pip install virtualenvwrapper')
    run('mkdir -p /home/env')

    test()
    commit()
    code_dir = '/home/env'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir):
            run("git clone git@github.com:macksoft2/servers.git %s" % code_dir)
    with cd(code_dir):
        run("git pull origin master")
        run("touch app.wsgi")