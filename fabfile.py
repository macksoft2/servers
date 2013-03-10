from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

def deploy():
    #sudo('aptitude install -y python-setuptools apache2 libapache2-mod-wsgi')
    #sudo ('aptitude install git')
    #sudo('easy_install pip')
    #sudo('pip install virtualenv')
    #sudo('pip install virtualenvwrapper')
    #run('mkdir -p /home/env')
    local("git add .")
    local(" git commit ")
    local("git push origin master")
    code_dir = '/home/manga/deplyapp'
    with settings(warn_only=True):
        if local("test -d %s" % code_dir):
            local("git clone git@github.com:macksoft2/servers.git %s" % code_dir)
    with cd(code_dir):
        local("git pull origin master")
        local("touch app.wsgi")