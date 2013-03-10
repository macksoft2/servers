from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['192.168.1.3']

def test():
    with settings(warn_only=True):
        result = local('./manage.py test servers', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

def commit():
    local("git add -p && git commit")

def push():
    local("git push")

def prepare_deploy():
    test()
    commit()
    push()

def deploy():
    test()
    code_dir = '/home/manga/deplyapp'
    with settings(warn_only=True):
        if local("test -d %s" % code_dir).failed:
            local("git clone git@github.com:macksoft2/.git %s" % code_dir)
    with cd(code_dir):
        local("git pull origin master ")
        local("touch app.wsgi")