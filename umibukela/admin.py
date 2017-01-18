from django.contrib import admin
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
)


class AdminSite(admin.AdminSite):
    index_template = 'admin/site_admin_index.html'

    def get_urls(self):
        from django.conf.urls import url
        urls = super(AdminSite, self).get_urls()
        urls = [
            url(r'^umibukela/kobo_forms$', self.admin_view(views.kobo_forms)),
            url(r'^umibukela/kobo_forms/(?P<kobo_form_id>\d+)/site/(?P<site_name>\w+)/preview$', self.admin_view(views.kobo_form_site_preview)),
            url(r'^umibukela/survey/(?P<survey_id>\d+)/kobo_submissions$', self.admin_view(views.survey_kobo_submissions)),
            url(r'^umibukela/survey_from_kobo$', self.admin_view(views.survey_from_kobo)),
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
admin_site.register(Survey)
admin_site.register(SurveyType)
