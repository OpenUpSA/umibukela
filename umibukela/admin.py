from django.contrib import admin

from .models import (
    Partner,
    Sector,
    Province,
)


class PartnerAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("short_name",)}

admin.site.register(Sector)
admin.site.register(Province)
admin.site.register(Partner, PartnerAdmin)
