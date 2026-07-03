from django import forms
from django.utils.translation import gettext_lazy as _

from apps.technicians.models import Technician


class CreateTechnicianForm(forms.ModelForm):
    """
    Creation form for creating a new technician object.
    Only the admin-user be able to create a new technician.
    """
    class Meta:
        model = Technician
        fields = (
            "national_code", "experience_years", "skill_level"
        )

        labels = {
            'national_code': _('کدملی'),
            'experience_years': _('سالهای فعالیت'),
            'skill_level': _('سطح مهارت')
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
                "class": "form-control mb-4"
            })


class UpdateTechnicianForm(forms.ModelForm):

    is_active = forms.BooleanField(required=False, label=_('وضعیت فعالیت'))

    class Meta:
        model = Technician
        fields = ('national_code', 'experience_years', 'skill_level', 'is_active')

        labels = {
            'national_code': _('کد ملی'),
            'experience_years': _('سال‌های تجربه'),
            'skill_level': _('سطح مهارت'),
            'is_active': _('وضعیت فعالیت')
        }

        widgets = {
            'national_code': forms.TextInput(
                attrs={'class': 'mb-4 form-control', 'placeholder': _('کد ملی')}
            ),
            'experience_years': forms.NumberInput(
                attrs={'class': 'mb-4 form-control', 'placeholder': _('سالهای تجربه')}
            ),
            'skill_level': forms.Select(
                attrs={'class': 'mb-4 form-control', 'placeholder': _('سطح مهارت')}
            ),
            'is_active': forms.CheckboxInput(
                attrs={'type': 'checkbox', 'class': 'mb-4', 'placeholder': _('وضعیت فعالیت')}
            )
        }
