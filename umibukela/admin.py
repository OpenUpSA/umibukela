from django.contrib import admin

from .models import (
    Cycle,
    CycleFrequency,
    CycleResultSet,
    Partner,
    Programme,
    Province,
    Sector,
    Site,
    Survey,
    SurveyType,
)


class PartnerAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("short_name",)}


class SiteAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Cycle)
admin.site.register(CycleFrequency)
admin.site.register(CycleResultSet)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(Programme)
admin.site.register(Province)
admin.site.register(Sector)
admin.site.register(Site, SiteAdmin)
admin.site.register(Survey)
admin.site.register(SurveyType)
