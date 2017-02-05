from django.contrib import admin
from umibukela import views
from itertools import groupby

from .models import (
    AttachmentNature,
    Cycle,
    CycleFrequency,
    CycleResultSet,
    CycleResultSetAttachment,
    Funder,
    Monitor,
    Partner,
    Programme,
    Province,
    Sector,
    Site,
    Survey,
    SurveyType,
)

from .forms import (
    CycleResultSetForm,
    SiteForm,
)


class AdminSite(admin.AdminSite):
    index_template = 'admin/site_admin_index.html'

    def get_urls(self):
        from django.conf.urls import url
        urls = super(AdminSite, self).get_urls()
        urls = [
            url(
                r'^umibukela/cycleresultset/(?P<result_id>\d+)/comments$',
                'umibukela.views.comments',
                name='site-result-comments'
            ),
            url(
                r'^umibukela/cycleresultset/(?P<result_id>\d+)/comments.pdf$',
                'umibukela.views.comments_pdf'
            ),
            url(
                r'^umibukela/kobo_forms/(?P<kobo_form_id>\d+)/site/(?P<site_name>\w+)/preview$',
                self.admin_view(views.kobo_form_site_preview)
            ),
            url(
                r'^umibukela/survey/(?P<survey_id>\d+)/kobo_submissions$',
                self.admin_view(views.survey_kobo_submissions)
            ),
            url(
                r'^umibukela/survey_from_kobo$',
                self.admin_view(views.survey_from_kobo)
            ),
            url(
                r'^umibukela/kobo_forms$',
                self.admin_view(views.kobo_forms)
            ),
        ] + urls
        return urls


class PartnerAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("short_name",)}


class ProvinceAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class SurveyTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

    def change_view(self, request, id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['provinces'] = Province.objects.all()
        extra_context['cycles'] = Cycle.objects.all()
        return super(SurveyTypeAdmin, self).change_view(request, id, extra_context=extra_context)


class SiteAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    form = SiteForm
    list_filter = ('province', 'sector')
    list_display = ('name', 'province', 'sector')


class CycleResultSetAttachmentInline(admin.TabularInline):
    model = CycleResultSetAttachment


class CycleResultSetAdmin(admin.ModelAdmin):
    inlines = [
        CycleResultSetAttachmentInline,
    ]
    form = CycleResultSetForm
    list_filter = ('cycle__programme', 'survey_type', 'site__province', 'funder', 'cycle')
    list_display = ('id', 'survey', 'cycle', 'site', 'partner')


class CycleAdmin(admin.ModelAdmin):

    def change_view(self, request, id, extra_context=None):
        extra_context = extra_context or {}

        def crs_province(x): return str(x.site.province)

        def crs_partner(x): return str(x.partner)

        def crs_site(x): return str(x.site)

        def crs_survey_type(x): return str(x.survey_type)

        provinces = []
        cycle_result_sets = sorted(CycleResultSet.objects.filter(cycle__id=id), key=crs_province)
        for province, prov_group in groupby(cycle_result_sets, crs_province):
            partners = []
            for partner, partner_group in groupby(sorted(prov_group, key=crs_partner), crs_partner):
                sites = []
                for site, site_group in groupby(sorted(partner_group, key=crs_site), crs_site):
                    survey_types = []
                    for survey_type, survey_type_group in groupby(sorted(site_group, key=crs_survey_type), crs_survey_type):
                        print province, partner, site, survey_type

                        survey_types.append({'name': survey_type, 'cycle_result_sets': survey_type_group})
                    sites.append({'name': site, 'survey_types': survey_types})
                partners.append({'name': partner, 'sites': sites})
            provinces.append({'name': province, 'partners': partners})
        extra_context['provinces'] = provinces
        return super(CycleAdmin, self).change_view(request, id, extra_context=extra_context)


admin_site = AdminSite()

admin_site.site_header = 'Umibukela administration'

admin_site.register(AttachmentNature)
admin_site.register(Cycle, CycleAdmin)
admin_site.register(CycleFrequency)
admin_site.register(CycleResultSet, CycleResultSetAdmin)
admin_site.register(Monitor)
admin_site.register(Partner, PartnerAdmin)
admin_site.register(Programme)
admin_site.register(Province)
admin_site.register(Sector)
admin_site.register(Site, SiteAdmin)
admin_site.register(Survey)
admin_site.register(SurveyType, SurveyTypeAdmin)
admin_site.register(Funder)
