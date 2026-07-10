from django import forms
from django.utils.translation import gettext_lazy as _

from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
from django_jalali.forms.widgets import jDateInput
from django_jalali.forms import jDateField

from apps.installations.models import Installation


class InstallationCreateForm(forms.ModelForm):
    """
    Creation form for creating a new Installation object.
    Only the admin-user and technician-user be able to
    create a new Installation.
    """
    class Meta:
        model = Installation
        fields = (
            "vendor", "technician", "device",
            "description", "installation_date"
        )
        labels = {
            'vendor': _('فروشنده'),
            'technician': _('نصاب'),
            'device': _('دستگاه'),
            'description': _('توضیحات'),
            'installation_date': _('تاریخ نصب')
        }
        widgets = {
            "installation_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control mb-2"
                }
            ),
            "next_inspection_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control mb-2"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialized the form class.

        Add some same widgets such as 'CSS class' to the all fields,
        or any other same properties.
        """
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control mb-2"
            })


class InstallationUpdateForm(forms.ModelForm):
    """
    Updating form to update a Installation profile,
    only the admin user and superuser are be able to
    update a profile.
    """
    # Overriding installation and replacement dates fields
    installation_date = JalaliDateField(
        label=_("تاریخ نصب"),
        widget=AdminJalaliDateWidget(attrs={
            "class": "form-control jalali_date-date",
            "autocomplete": "off",
        })
    )
    first_replacement_date = JalaliDateField(
        label=_("اولین تعویض فیلتر"),
        required=False,
        widget=AdminJalaliDateWidget(attrs={
            "class": "form-control jalali_date-date",
            "autocomplete": "off",
        })
    )
    second_replacement_date = JalaliDateField(
        label=_("دومین تعویض فیلتر"),
        required=False,
        widget=AdminJalaliDateWidget(attrs={
            "class": "form-control jalali_date-date",
            "autocomplete": "off",
        })
    )
    third_replacement_date = JalaliDateField(
        label=_("سومین تعویض فیلتر"),
        required=False,
        widget=AdminJalaliDateWidget(attrs={
            "class": "form-control jalali_date-date",
            "autocomplete": "off",
        })
    )
    forth_replacement_date = JalaliDateField(
        label=_("چهارمین تعویض فیلتر"),
        required=False,
        widget=AdminJalaliDateWidget(attrs={
            "class": "form-control jalali_date-date",
            "autocomplete": "off",
        })
    )

    is_active = forms.BooleanField(required=False, label=_('وضعیت فعالیت'))
    first_replacement_status = forms.BooleanField(required=False, label=_('وضعیت'))
    second_replacement_status = forms.BooleanField(required=False, label=_('وضعیت'))
    third_replacement_status = forms.BooleanField(required=False, label=_('وضعیت'))
    forth_replacement_status = forms.BooleanField(required=False, label=_('وضعیت'))

    class Meta:
        model = Installation
        fields = (
            "vendor", "technician", "description",
            "device", "installation_date", "is_active",
            # Replacement dates
            "first_replacement_date", "second_replacement_date",
            "third_replacement_date", "forth_replacement_date",
            # Replacement dates status
            "first_replacement_status", "second_replacement_status",
            "third_replacement_status", "forth_replacement_status"
        )

        labels = {
            "vendor": _("فروشنده"),
            "technician": _("نصاب"),
            "description": _("توضیحات"),
            "device": _("دستگاه"),
        }

        widgets = {
            "vendor": forms.Select(attrs={"class": "mb-4"}),
            "device": forms.Select(attrs={"class": "mb-4"}),
            "technician": forms.Select(attrs={"class": "mb-4"}),
            "is_active": forms.CheckboxInput(attrs={"type": "checkbox", "class": "mb-4"}),
            # Replacement dates status
            "first_replacement_status": forms.CheckboxInput(
                attrs={"type": "checkbox", "class": "mb-4"}
            ),
            "second_replacement_status": forms.CheckboxInput(
                attrs={"type": "checkbox", "class": "mb-4"}
            ),
            "third_replacement_status": forms.CheckboxInput(
                attrs={"type": "checkbox", "class": "mb-4"}
            ),
            "forth_replacement_status": forms.CheckboxInput(
                attrs={"type": "checkbox", "class": "mb-4"}
            ),
        }
