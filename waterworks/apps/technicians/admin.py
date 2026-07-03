from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Technician


@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    list_display = (
        "user__phone_number",
        "national_code",
        "installer_code",
        "is_active"
    )
    list_filter = ("is_active", "created_at", "updated_at", "skill_level")
    search_fields = (
        "user__phone_number",
        "user__username",
        "user__userprofile__address",
        "national_code",
        "installer_code"
    )
    readonly_fields = ("created_at", "updated_at")
    ordering = ("user",)

    fieldsets = (
        (_("Technician Information"),
            {
                "fields": ("user", "national_code")
            }
        ),
        (_("Technician Job Information"),
            {
                "classes": ("wide",),
                "fields": ("installer_code", "experience_years", "skill_level")
            }
        ),
        (_("Status & Timestamps"),
            {
                "classes": ("collapse",),
                "fields": ("is_active", "created_at", "updated_at"),
            }
        ),
    )

    add_fieldsets = (
        (_("Technician Information"),
            {
                "fields": ("user", "national_code")
            }
        ),
        (_("Technician Job Information"),
            {
                "classes": ("wide",),
                "fields": ("installer_code", "experience_years", "skill_level")
            }
        ),
        (_("Status & Timestamps"),
            {
                "classes": ("collapse",),
                "fields": ("is_active", "created_at", "updated_at"),
            }
        ),
    )
