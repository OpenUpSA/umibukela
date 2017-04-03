from django.contrib import admin
from umibukela import views

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
    SurveyKoboProject,
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
                r'^umibukela/cycle/(?P<cycle_id>\d+)/create_zip$',
                'umibukela.views.create_materials_zip',
                name='cycle-create-zip'
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
                r'^umibukela/programme/(?P<programme_id>\d+)/kobo_grant$',
                self.admin_view(views.programme_kobo_grant),
                name='programme-kobo-grant'
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
    list_filter = (
        'survey__cycle__programme',
        'survey__type',
        'site__province',
        'funder',
        'survey__cycle'
    )

    def cycle(instance):
        return instance.survey.cycle

    list_display = ('id', 'survey', cycle, 'site', 'partner')


class CycleAdmin(admin.ModelAdmin):

    def change_view(self, request, id, extra_context=None):
        extra_context = extra_context or {}

        cycle_result_sets = CycleResultSet.objects.filter(survey__cycle__id=id)\
                                .order_by('site__province', 'partner', 'site', 'survey__type')
        extra_context['cycle_result_sets'] = cycle_result_sets
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
admin_site.register(SurveyKoboProject)
admin_site.register(SurveyType, SurveyTypeAdmin)
admin_site.register(Funder)
