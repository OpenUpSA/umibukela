from django.contrib import admin

from .models import Partner


class PartnerAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("short_name",)}

admin.site.register(Partner, PartnerAdmin)
