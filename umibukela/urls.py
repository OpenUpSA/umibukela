from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'umibukela.views.home', name='home'),
    url(r'^contact$', 'umibukela.views.contact', name='contact'),
    url(r'^about$', 'umibukela.views.about', name='about'),

    url(r'^sites$', 'umibukela.views.sites', name='sites'),
    url(r'^sites/(?P<site_name>\w+)$', 'umibukela.views.site', name='site'),

    url(r'^admin/', include(admin.site.urls)),
)
