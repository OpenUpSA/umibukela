from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns(
    '',
    url(r'^$', 'umibukela.views.home', name='home'),
    url(r'^about$', 'umibukela.views.about', name='about'),
    url(r'^learn-about-cbm$', 'umibukela.views.learn', name='learn'),
    url(r'^resources$', 'umibukela.views.resources', name='resources'),

    url(r'^sites$', 'umibukela.views.sites', name='sites'),
    url(r'^sites/(?P<site_slug>[\w-]+)$', 'umibukela.views.site', name='site'),
    url(r'^sites/(?P<site_slug>[\w-]+)/results/(?P<result_id>\d+)$', 'umibukela.views.site_result', name='site-result'),

    url(r'^partners$', 'umibukela.views.partners', name='partners'),
    url(r'^partners/(?P<partner_slug>[\w-]+)$', 'umibukela.views.partner', name='partner'),

    # health-e
    url(r'^stockouts/$', 'umibukela.healthe.views.home', name='healthe-home'),
    url(r'^stockouts/download/$', 'umibukela.healthe.views.report_download', name='healthe-report-download'),

    url(r'^admin/', include(admin.site.urls)),

    # For when images are hosted locally
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
