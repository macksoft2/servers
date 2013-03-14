# -*- coding: utf-8 -*-
from __future__ import with_statement
from fabric.api import *
from fabric.operations import run,local
from fabric.contrib.console import confirm
from fabtools.python_distribute import is_distribute_installed, install_distribute
from fabtools.require.python import *
import sys
#------------------------------------------variables globales -------------------------#
#env.hosts = ['192.168.1.45']
#code_dir = '/root/manga'
code_dir =  '/home/testdeploy'
vhost_dir = '/etc/apache2/sites-enabled'

PACKAGES_LIST = [
    'Django==1.4',
    'south',
    'curl',
    'apache2',
    'mysql-server',
    'python-setuptools',
    'python-mysqldb',
    'libapache2-mod-wsgi',
]
projet_directory =''
#--------------------------------------------debut fonctions config serveur -------------------------#
def upgrade():
    sudo("apt-get update")
    sudo("apt-get upgrade")

def install_python():
    if not  is_distribute_installed():
        install_distribute()

def install_pip():
    if not is_pip_installed():
        install_pip()

def install_packages():
    for package in PACKAGES_LIST:
        run('pip install %s' % package)

# on envoie une copie de la cle publique du client vers le serveur.
# notre cle publique est ajoutee au fichier  ~/.ssh/authorized_keys du serveur
def publi_key(ip_server):
    local('ssh-copy-id root@'+ip_server)

def creer_repertoire_projet():
    if code_dir not in sys.path:
        sys.path.append(code_dir)

#--------------------------------------------- End  fonctions config serveur-----------------------------------#

#------------------------------------- --------gestionnaire dépot git -----------------------------------------#

def commit():
    local("git add . && git commit")

def push(name_app):
    local("git push %s" %name_app)

#-------------------------------------------End gestionnaire dépot git ----------------------------------------#

def clone(name_app):
    local('git clone  -b master git://github.com/macksoft2/%s.git %s' % (code_dir,name_app))
#----------------------------------------- config apache-------------------------------------------------------#
def active_wsgi():
    local("cd %s && a2enmod wsgi " %vhost_dir)

def creer_wsgi_file(projet_name):
    wsgi_file = projet_name+'.wsgi'
    local("cd %s && echo 'import os, sys' >> %s" % (code_dir,wsgi_file))
    local("cd %s && echo path = %s >> %s" % (code_dir,code_dir,wsgi_file))
    local("cd %s && echo 'if path not in sys.path:' >> %s" %(code_dir,wsgi_file))
    local("cd %s && echo '    sys.path.append(path)' >> %s" %(code_dir,wsgi_file))
    local("cd %s && echo 'os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' ' >> %s" % (code_dir,projet_name,wsgi_file))
    local("cd %s && echo 'import django.core.handlers.wsgi' >> %s" % (code_dir,wsgi_file))
    local("cd %s && echo 'application = django.core.handlers.wsgi.WSGIHandler()' >> %s" % (code_dir,wsgi_file))

def ceer_vhost(projet_name,email_admin=None,server_name=None,serverAlias=None,user=None,user_group=None):
    vhost = projet_name
    local("cd %s && echo '<VirtualHost *:80 >' >> %s" % (vhost_dir,vhost))
    local("cd %s && echo 'ServerAdmin %s' >> %s" % (vhost_dir,vhost,email_admin))
    local("cd %s && echo 'ServerName  %s' >> %s" % (vhost_dir,vhost,server_name))
    local("cd %s && echo 'ServerAlias ' >> %s" % (vhost_dir,vhost,serverAlias))
    local("cd %s && echo 'DocumentRoot %s' >> %s" % (vhost_dir,vhost,code_dir))
    local("cd %s && echo 'WSGIDaemonProcess daemon-%s user=%s group=%s processes=1 maximum-requests=1 threads=1 inactivity-timeout=6' >> %s" % (vhost_dir,vhost,projet_name,user,user_group))
    local("cd %s && echo 'WSGIProcessGroup daemon-%s' >> %s" % (vhost_dir,vhost,projet_name))
    local("cd %s && echo 'WSGIScriptAlias / %s/%s.wsgi' >> %s" % (vhost_dir,vhost,code_dir,projet_name))

    local("cd %s && echo '<Directory %s/>' >> %s" % (vhost_dir,vhost,code_dir))
    local("cd %s && echo 'Options Indexes FollowSymLinks MultiViews' >> %s" % (vhost_dir,vhost))
    local("cd %s && echo 'AllowOverride All' >> %s" % (vhost_dir,vhost))
    local("cd %s && echo 'Order allow,deny' >> %s" % (vhost_dir,vhost))
    local("cd %s && echo 'allow from all' >> %s" % (vhost_dir,vhost))
    local("cd %s && echo '</Directory>' >> %s" % (vhost_dir,vhost))

    local("cd %s && echo 'ErrorLog /var/log/apache2/%s.error.log' >> %s" % (vhost_dir,vhost,projet_name))
    local("cd %s && echo 'LogLevel warn' >> %s" % (vhost_dir,vhost))
    local("cd %s && echo 'ServerSignature On' >> %s" % (vhost_dir,vhost))
    local("cd %s && echo '</VirtualHost>' >> %s" % (vhost_dir,vhost))

def active_site(nameVhost):
    local(" cd %s a2ensite %s " %(vhost_dir,nameVhost))
#----------------------------End config apache -------------------------------------------------------------------#
def test():
    with settings(warn_only=True):
        result = local('./manage.py test servers', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

@hosts('localhost:8000')
def prepare_deploy():
    commit()
    push()

def deploy():
    #local('git clone  -b master git://github.com/macksoft2/servers.git %s' % code_dir)
    local ("cd %s " % code_dir)
    #name = 'monprojet'
    #local("cd %s && echo 'import os, sys' >> gestionServer.wsgi" %code_dir)
    #local("cd %s && echo %s >> gestionServer.wsgi" % (code_dir,code_dir))
    #local("cd %s && echo 'if path not in sys.path:' >> gestionServer.wsgi" %code_dir)
    #local("cd %s && echo '    sys.path.append(path)' >> gestionServer.wsgi" %code_dir)
    #local("cd %s && echo 'os.environ['DJANGO_SETTINGS_MODULE'] = 'gestionServer.settings' ' >> gestionServer.wsgi" %code_dir)
    #local("cd %s && echo 'import django.core.handlers.wsgi' >> gestionServer.wsgi" %code_dir)
    #local("cd %s && echo 'application = django.core.handlers.wsgi.WSGIHandler()' >> gestionServer.wsgi" %code_dir)
    #local("cd %s && echo 'os.environ['DJANGO_SETTINGS_MODULE'] ='%s.settings'' >> gestionServer.wsgi" % (code_dir,name))