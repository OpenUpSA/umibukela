from django.contrib import admin
from django.contrib.admin import AdminSite
from django.http import HttpResponse
from umibukela import settings
from umibukela import views

from .models import (
    AttachmentNature,
    Cycle,
    CycleFrequency,
    CycleResultSet,
    CycleResultSetAttachment,
    Partner,
    Programme,
    Province,
    Sector,
    Site,
    Survey,
    SurveyType,
)

from .forms import (
    SiteForm,
    SurveyForm,
)


class AdminSite(AdminSite):

    def get_urls(self):
        from django.conf.urls import url
        urls = super(AdminSite, self).get_urls()
        urls = [
            url(r'^umibukela/survey/(?P<survey_id>\d+)/sources/$', self.admin_view(views.survey_sources))
        ] + urls
        return urls


class PartnerAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("short_name",)}


class SiteAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    form = SiteForm


class CycleResultSetAttachmentInline(admin.TabularInline):
    model = CycleResultSetAttachment


class CycleResultSetAdmin(admin.ModelAdmin):
    inlines = [
        CycleResultSetAttachmentInline,
    ]


class SurveyAdmin(admin.ModelAdmin):
    form = SurveyForm

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['path'] = request.path
        return super(SurveyAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)


admin_site = AdminSite()

admin_site.site_header = 'Umibukela administration'

admin_site.register(AttachmentNature)
admin_site.register(Cycle)
admin_site.register(CycleFrequency)
admin_site.register(CycleResultSet, CycleResultSetAdmin)
admin_site.register(Partner, PartnerAdmin)
admin_site.register(Programme)
admin_site.register(Province)
admin_site.register(Sector)
admin_site.register(Site, SiteAdmin)
admin_site.register(Survey, SurveyAdmin)
admin_site.register(SurveyType)
