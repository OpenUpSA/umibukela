from django.contrib import admin
from umibukela import settings

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
        extra_context['kobo_access_token'] = request.session.get('kobo_access_token', None)
        extra_context['kobo_client_id'] = settings.KOBO_CLIENT_ID
        extra_context['path'] = request.path
        return super(SurveyAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)


admin.site.site_header = 'Umibukela administration'

admin.site.register(AttachmentNature)
admin.site.register(Cycle)
admin.site.register(CycleFrequency)
admin.site.register(CycleResultSet, CycleResultSetAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(Programme)
admin.site.register(Province)
admin.site.register(Sector)
admin.site.register(Site, SiteAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(SurveyType)
