from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.accounts.models import User, UserProfile
from apps.accounts.user_admin_form import UserCreationForm, UserChangeForm



@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['phone_number', 'username', 'role', 'is_admin', 'is_staff']
    list_filter = ['is_active', 'is_admin', 'is_staff']
    search_fields = ['phone_number', 'username']
    readonly_fields = ['last_login']
    ordering = ['phone_number', 'username']
    filter_horizontal = ['groups', 'user_permissions']
    list_per_page = 30

    fieldsets = (
        [_('Personal Information'),
            {
                'fields': ('phone_number', 'username', 'password')
            }
        ],
        [_('Permissions'),
            {
                'classes': ('collapse',),
                'fields': (
                    'is_active',
                    'is_admin',
                    'is_staff',
                    'is_superuser',
                    'last_login',
                    'groups',
                    'user_permissions'
                )
            }
        ],
        [_('Role'),
            {
                'classes': ('collapse',),
                'fields': ('role',)
            }
        ],
    )

    add_fieldsets = (
        [None,
            {
                'classes': ('wide',),
                'fields': ('phone_number', 'username', 'password1', 'password2')
            }
        ],
    )

    def get_form(self, request, obj=None, **kwargs):
        """
        Customizes the user form based on the user"s permissions.

        Checks if the logged-in user is a superuser. If the user is not a superuser,
        the "is_superuser" field in the form will be disabled, preventing any changes
        to this attribute.
        """
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True

        return form


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'fullname', 'address']
    list_filter = ['created_at', 'updated_at', 'is_active']
    search_fields = ['user', 'fullname', 'address']
    readonly_fields = ['created_at', 'updated_at']
