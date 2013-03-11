# -*- coding: utf-8 -*-
from __future__ import with_statement
from fabric.api import *
from fabric.operations import run,env,local,put
env.hosts = ['192.168.1.45']

def test():
    local("./manage.py test servers")
def commit():
    local("git init")
    local("git add && git commit -a")
    #local("git remote add origin git@github.com:macksoft2/servers.git")
    local("git push -f")
def deploy():
    sudo("apt-get install git ")
    #sudo("mkdir testdeploy")
    test()
    commit()
    code_dir = 'testdeploy'
    with settings(warn_only=True):
        if local("test -d %s" % code_dir):
            run("git clone git@github.com:macksoft2/servers.git %s" % code_dir)
    with cd(code_dir):
        run("git pull origin master")
        local("touch app.wsgi")