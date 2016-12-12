from django.contrib import admin

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
