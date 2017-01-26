from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from umibukela.admin import admin_site


urlpatterns = patterns(
    '',
    url(r'^$',
      'umibukela.views.home',
        name='home'),
    url(r'^about$',
      'umibukela.views.about',
        name='about'),
    url(r'^learn-about-cbm$',
      'umibukela.views.learn',
        name='learn'),
    url(r'^resources$',
      'umibukela.views.resources',
        name='resources'),

    url(r'^sites$',
        'umibukela.views.sites',
        name='sites'),
    url(r'^sites/(?P<site_slug>[\w-]+)$',
        'umibukela.views.site',
        name='site'),
    url(r'^sites/(?P<site_slug>[\w-]+)/results/(?P<result_id>\d+)$',
        'umibukela.views.site_result',
        name='site-result'),
    url(r'^sites/(?P<site_slug>[\w-]+)/results/(?P<result_id>\d+)/poster$',
        'umibukela.views.poster',
        name='site-result-poster'),
    url(r'^sites/(?P<site_slug>[\w-]+)/results/(?P<result_id>\d+)/poster.pdf$',
        'umibukela.views.poster_pdf',
        name='site-result-poster-pdf'),
    url(r'^sites/(?P<site_slug>[\w-]+)/results/(?P<result_id>\d+)/handout$',
        'umibukela.views.handout',
        name='site-result-handout'),
    url(r'^sites/(?P<site_slug>[\w-]+)/results/(?P<result_id>\d+)/handout.pdf$',
        'umibukela.views.handout_pdf',
        name='site-result-handout-pdf'),
    url(r'^sites/(?P<site_slug>[\w-]+)/results/(?P<result_id>\d+)/summary$',
        'umibukela.views.summary',
        name='site-result-summary'),
    url(r'^sites/(?P<site_slug>[\w-]+)/results/(?P<result_id>\d+)/summary.pdf$',
        'umibukela.views.summary_pdf',
        name='site-result-summary-pdf'),

    url(r'^partners$',
        'umibukela.views.partners',
        name='partners'),
    url(r'^partners/(?P<partner_slug>[\w-]+)$',
        'umibukela.views.partner',
        name='partner'),

    # health-e
    url(r'^stockouts/$',
        'umibukela.healthe.views.home',
        name='healthe-home'),
    url(r'^stockouts/download/$',
        'umibukela.healthe.views.report_download',
        name='healthe-report-download'),
    url(r'^stockouts/stats/$',
        'umibukela.healthe.views.stats',
        name='healthe-stats'),
    url(r'^stockouts/year/report$',
        'umibukela.healthe.views.year_report',
        name='healthe-year-report'),

    url(r'^login/$',
        'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
    url(r'^admin/kobo-oauth',
        'umibukela.views.kobo_oauth_return',
        name='kobo-oauth'),
    url(r'^admin/', include(admin_site.urls)),

    # For when images are hosted locally
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
