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
    # programmes
    url('^programmes$', 'umibukela.views.programmes', name='programmes'),
    url('^programmes/(?P<programme_slug>[\w?-]+)$',
        'umibukela.views.programme_detail',
        name='programme_detail'),
    url('^programmes/survery/site/(?P<survey_name>.*)/download$',
        'umibukela.views.progamme_survey',
        name='programme_survey'),
    url('^programmes/survey/(?P<cycle_result_id>\d+)/site/download$',
        'umibukela.views.site_survey_download',
        name='site_survey_download'),
    url('^programme/survey/(?P<survey_name>.*)/download$',
        'umibukela.views.survey_download',
        name='survey_download'),
    url(r'^sites$', 'umibukela.views.sites', name='sites'),
    url(r'^sites/(?P<site_slug>[\w-]+)$', 'umibukela.views.site', name='site'),
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
    url(r'^sites/(?P<site_slug>[\w-]+)/results/(?P<result_id>\d+)/comments$',
        'umibukela.views.comments',
        name='site-result-comments'),
    url(r'^sites/(?P<site_slug>[\w-]+)/results/(?P<result_id>\d+)/comments.pdf$',
        'umibukela.views.comments_pdf',
        name='site-result-comments-pdf'),

    # survey types
    url(r'^survey-types$', 'umibukela.views.survey_types', name='survey-types'
        ),
    url(r'^survey-types/(?P<survey_type_slug>[\w-]+)$',
        'umibukela.views.survey_type',
        name='survey-type'),
    url(r'^survey-types/(?P<survey_type_slug>[\w-]+)/(?P<cycle_id>[\w-]+)$',
        'umibukela.views.survey_type_cycle',
        name='survey-type-cycle'),
    url(r'^partners$', 'umibukela.views.partners', name='partners'),
    url(r'^partners/(?P<partner_slug>[\w-]+)$',
        'umibukela.views.partner',
        name='partner'),

    # regional summary
    url(r'^survey-type/(?P<survey_type_slug>[\w-]+)/province/(?P<province_slug>[\w-]+)/cycle/(?P<cycle_id>\d+)/summary$',
        'umibukela.views.province_summary',
        name='province-summary'),
    url(r'^survey-type/(?P<survey_type_slug>[\w-]+)/province/(?P<province_slug>[\w-]+)/cycle/(?P<cycle_id>\d+)/summary.pdf$',
        'umibukela.views.province_summary_pdf',
        name='province-summary-pdf'),
    url(r'^survey-type/(?P<survey_type_slug>[\w-]+)/south-africa/cycle/(?P<cycle_id>\d+)/summary$',
        'umibukela.views.national_summary',
        name='national-summary'),
    url(r'^survey-type/(?P<survey_type_slug>[\w-]+)/south-africa/cycle/(?P<cycle_id>\d+)/summary.pdf$',
        'umibukela.views.national_summary_pdf',
        name='national-summary-pdf'),

    # regional poster
    url(r'^survey-type/(?P<survey_type_slug>[\w-]+)/province/(?P<province_slug>[\w-]+)/cycle/(?P<cycle_id>\d+)/poster$',
        'umibukela.views.province_poster',
        name='province-poster'),
    url(r'^survey-type/(?P<survey_type_slug>[\w-]+)/province/(?P<province_slug>[\w-]+)/cycle/(?P<cycle_id>\d+)/poster.pdf$',
        'umibukela.views.province_poster_pdf',
        name='province-poster-pdf'),
    url(r'^survey-type/(?P<survey_type_slug>[\w-]+)/south-africa/cycle/(?P<cycle_id>\d+)/poster$',
        'umibukela.views.national_poster',
        name='national-poster'),
    url(r'^survey-type/(?P<survey_type_slug>[\w-]+)/south-africa/cycle/(?P<cycle_id>\d+)/poster.pdf$',
        'umibukela.views.national_poster_pdf',
        name='national-poster-pdf'),

    # health-e
    url(r'^stockouts/$', 'umibukela.healthe.views.home', name='healthe-home'),
    url(r'^stockouts/download/$',
        'umibukela.healthe.views.report_download',
        name='healthe-report-download'),
    url(r'^stockouts/stats/$',
        'umibukela.healthe.views.stats',
        name='healthe-stats'),
    url(r'^stockouts/year/report$',
        'umibukela.healthe.views.year_report',
        name='healthe-year-report'),
    url(r'^login/$', 'django.contrib.auth.views.login', {
        'template_name': 'admin/login.html'
    }),
    url(r'^admin/kobo-oauth',
        'umibukela.views.kobo_oauth_return',
        name='kobo-oauth'),
    url(r'^admin/', include(admin_site.urls)),

    # For when images are hosted locally
) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
