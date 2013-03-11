from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover()
from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gestionServer.views.home', name='home'),
    # url(r'^gestionServer/', include('gestionServer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^$' , 'django.contrib.auth.views.login'),
    (r'^accounts/', include('registration.urls')),
    url(r'^servers/', include('servers.urls')),
    #url(r'', 'servers.views.default'),
    url(r'^index$', 'servers.views.index'),
    (r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    # url(r'^admin/', include(admin.site.urls)),
)
