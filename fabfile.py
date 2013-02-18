# -*- coding: utf-8 -*-
from __future__ import with_statement
from fabric.api import * 
from fabric.operations import run,put

env.hosts = ['my_server']
def test():
    local("./manage.py test servers")

def commit():
    local("git add -p && git commit ")
    local("git push origin master")    




