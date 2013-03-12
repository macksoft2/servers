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
# on envoie une copie de la cle publique du client vers le serveur.
# notre cle publique est ajoutee au fichier  ~/.ssh/authorized_keys du serveur
def publi_key(ip_server):
    local('ssh-copy-id root@'+ip_server)

#--------------------------------------------- End dev fonctions-----------------------------------#

@hosts('localhost:8000')
def prepare_deploy():
    commit()
    push()

def deploy():
    run('git clone  -b master git://github.com/macksoft2/servers.git %s' % code_dir)
    run ("cd %s " % code_dir)
    run("touch gestionServer.wsgi")