from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import localdate

from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget

from apps.installations.models import Installation


class InstallationCreateForm(forms.ModelForm):
    """
    Creation form for creating a new Installation object.
    Only the admin-user and technician-user be able to
    create a new Installation.
    """
    installation_date = JalaliDateField(
        label=_("تاریخ نصب"),
        required=False,
        widget=AdminJalaliDateWidget(attrs={
            "class": "form-control jalali_date-date",
            "autocomplete": "off",
        })
    )

    class Meta:
        model = Installation
        fields = (
            'vendor', 'technician', 'device',
            'description', 'installation_date'
        )
        labels = {
            'vendor': _('فروشنده'),
            'technician': _('نصاب'),
            'device': _('دستگاه'),
            'description': _('توضیحات'),
        }
        widgets = {
            'vendor': forms.Select(attrs={'class': 'form-control mb-2'}),
            'technician': forms.Select(attrs={'class': 'form-control mb-2'}),
            'device': forms.Select(attrs={'class': 'form-control mb-2'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-2'}),
        }

    def save(self, commit=True):
        """
        Override the save workflow for installation date,
        saves installation date to the current date if nothing sent
        by the client.
        """
        installation_date = self.cleaned_data.get('installation_date')
        instance = super().save(commit=False)

        if not installation_date:
            instance.installation_date = localdate()

        if commit:
            instance.save()

        return instance


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
