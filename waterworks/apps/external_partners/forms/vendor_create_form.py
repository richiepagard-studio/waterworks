from django import forms
from django.utils.translation import gettext_lazy as _

from apps.external_partners.models import Vendor


class VendorCreateForm(forms.ModelForm):
    """
    Creation form for creating a new vendor object.
    Only the admin-user is be able to create a new vendor.
    """
    class Meta:
        model = Vendor
        fields = ("shop_name", "contact_phone", "banner")

        labels = {
            'shop_name': _('نام فروشگاه'),
            'contact_phone': _('شماره تماس کسب'),
            'banner': _('بنر فروشگاه')
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
