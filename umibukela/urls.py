from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from umibukela.admin import admin_site


urlpatterns = patterns(
    '',
    url(r'^$', 'umibukela.views.home', name='home'),
    url(r'^about$', 'umibukela.views.about', name='about'),
    url(r'^learn-about-cbm$', 'umibukela.views.learn', name='learn'),
    url(r'^resources$', 'umibukela.views.resources', name='resources'),

    url(r'^sites$', 'umibukela.views.sites', name='sites'),
    url(r'^sites/(?P<site_slug>[\w-]+)$', 'umibukela.views.site', name='site'),
    url(r'^sites/(?P<site_slug>[\w-]+)/results/(?P<result_id>\d+)$', 'umibukela.views.site_result', name='site-result'),

    url(r'^poster/(?P<site_slug>[\w-]+)/results/(?P<result_id>\d+)$', 'umibukela.views.poster', name='poster'),
    url(r'^brochure/(?P<site_slug>[\w-]+)/results/(?P<result_id>\d+)$', 'umibukela.views.brochure', name='brochure'),


    url(r'^partners$', 'umibukela.views.partners', name='partners'),
    url(r'^partners/(?P<partner_slug>[\w-]+)$', 'umibukela.views.partner', name='partner'),

    # health-e
    url(r'^stockouts/$', 'umibukela.healthe.views.home', name='healthe-home'),
    url(r'^stockouts/download/$', 'umibukela.healthe.views.report_download', name='healthe-report-download'),
    url(r'^stockouts/stats/$', 'umibukela.healthe.views.stats', name='healthe-stats'),
    url(r'^stockouts/year/report$', 'umibukela.healthe.views.year_report', name='healthe-year-report'),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
    url(r'^admin/kobo-oauth', 'umibukela.views.kobo_oauth_return', name='kobo-oauth'),
    url(r'^admin/', include(admin_site.urls)),

    # For when images are hosted locally
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
