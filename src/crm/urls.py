# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from core.views import *
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'crm.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'', include('social_auth.urls')),
	url(r'^', include('crm.landing.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ofertas/', include('core.urls')),
    url(r'^perfil/(\d+)$', perfil, name="perfil"),
    url(r'^perfil/cuentas$', manejo_cuentas, name="enlazar perfiles"),
    url(r'^signup', 'core.views.registro', name='registro'),
)

urlpatterns += patterns('core.views',
    url(r'^login/$', 'login_user', name='crm_login'),
    url(r'^logout/$', 'logout_user', name='crm_logout'),
)
