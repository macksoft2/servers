# -*- coding: utf-8 -*-
from __future__ import with_statement
from fabric.api import *
from fabric.operations import run,env,local,put
env.hosts = ['192.168.1.45']

def prepare_deploy():
    local("./manage.py test servers")
    local("git add -p && git commit")
    local("git push")