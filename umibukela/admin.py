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


admin_site = AdminSite()

admin_site.site_header = 'Umibukela administration'

admin_site.register(AttachmentNature)
admin_site.register(Cycle)
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
