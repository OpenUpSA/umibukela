from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$', 'umibukela.views.home', name='home'),
    url(r'^contact$', 'umibukela.views.contact', name='contact'),
    url(r'^about$', 'umibukela.views.about', name='about'),

    url(r'^sites$', 'umibukela.views.sites', name='sites'),
    url(r'^sites/(?P<site_slug>[\w-]+)$', 'umibukela.views.site', name='site'),
    url(r'^sites/(?P<site_slug>[\w-]+)/results/(?P<result_id>\d+)$', 'umibukela.views.site_result', name='site-result'),

    url(r'^partners$', 'umibukela.views.partners', name='partners'),
    url(r'^partners/(?P<partner_slug>[\w-]+)$', 'umibukela.views.partner', name='partner'),

    url(r'^admin/', include(admin.site.urls)),

    # For when images are hosted locally
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
