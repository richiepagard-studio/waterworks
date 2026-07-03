from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = (
        "user__phone_number",
        "shop_name",
        "contact_phone",
        "is_active"
    )
    list_filter = ("is_active", "created_at", "updated_at")
    search_fields = (
        "user__phone_number",
        "user__username",
        "shop_name",
        "contact_email",
    )
    readonly_fields = ("created_at", "updated_at")
    ordering = ("user",)


    fieldsets = (
        (_("Vendor Information"),
            {
                "fields": (
                    "user",
                    "shop_name",
                    "contact_email",
                    "contact_phone",
                    "banner"
                )
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
        (_("Vendor Information"),
            {
                "fields": (
                    "user",
                    "shop_name",
                    "contact_email",
                    "contact_phone",
                    "banner"
                )
            }
        ),
        (_("Status & Timestamps"),
            {
                "classes": ("collapse",),
                "fields": ("is_active", "created_at", "updated_at"),
            }
        ),
    )
