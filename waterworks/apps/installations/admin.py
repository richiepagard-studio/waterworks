from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Installation


@admin.register(Installation)
class InstallationAdmin(admin.ModelAdmin):
    list_display = (
        "user__phone_number",
        "vendor__shop_name",
        "technician",
        "is_active"
    )
    list_filter = ("is_active", "created_at", "updated_at")
    search_fields = (
        "user__phone_number",
        "user__username",
        "user__userprofile__address",
        "user__userprofile__last_name"
    )
    readonly_fields = ("created_at", "updated_at")


    fieldsets = (
        (_("Installation Customer Information"),
            {
                "fields": ("user", "installation_code")
            }
        ),
        (_("Installation Information"),
            {
                "classes": ("collapse",),
                "fields": ("vendor", "technician", "description", "device")
            }
        ),
        (_("Service Dates"),
            {
                "classes": ("collapse",),
                "fields": (
                    "installation_date",
                    # Replacement dates
                    "first_replacement_date",
                    "second_replacement_date",
                    "third_replacement_date",
                    "forth_replacement_date",
                    # Replacement dates status
                    "first_replacement_status",
                    "second_replacement_status",
                    "third_replacement_status",
                    "forth_replacement_status"
                )
            }
        ),
        (_("Default Dates & Status"),
            {
                "classes": ("collapse",),
                "fields": ("is_active", "created_at", "updated_at"),
            }
        ),
    )

    add_fieldsets = (
        (_("Installation Customer Information"),
            {
                "fields": ("user", "installation_code")
            }
        ),
        (_("Installation Information"),
            {
                "classes": ("collapse",),
                "fields": ("vendor", "technician", "description", "device")
            }
        ),
        (_("Service Dates"),
            {
                "classes": ("collapse",),
                "fields": (
                    "installation_date",
                )
            }
        ),
        (_("Default Date & Status"),
            {
                "classes": ("collapse",),
                "fields": ("is_active", "created_at", "updated_at"),
            }
        ),
    )
